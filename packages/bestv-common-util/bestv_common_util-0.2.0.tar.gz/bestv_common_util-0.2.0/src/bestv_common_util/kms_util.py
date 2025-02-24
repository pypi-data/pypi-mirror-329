# -*- coding: UTF-8 -*-

import os
import base64
import logging
import requests
import json
import re


from aliyun_encryption_sdk.cache.local import LocalDataKeyMaterialCache
from aliyun_encryption_sdk.ckm.cache import CachingCryptoKeyManager
from aliyun_encryption_sdk.client import AliyunCrypto
from aliyun_encryption_sdk.kms import AliyunConfig
from aliyun_encryption_sdk.kms.kms import AliyunKms
from aliyun_encryption_sdk.provider.default import DefaultDataKeyProvider

from aliyun_encryption_sdk import to_bytes, to_str
from aliyun_encryption_sdk.provider import EncryptedDataKey

from aliyunsdkkms.request.v20160120 import GenerateDataKeyRequest, EncryptRequest, ReEncryptRequest, DecryptRequest, \
    GetSecretValueRequest, CreateSecretRequest, AsymmetricSignRequest, AsymmetricVerifyRequest
from aliyun_encryption_sdk.provider import EncryptedDataKey, str_to_cmk


class KMSUtil:
    ENCRYPTED_PROPERTY_PREFIX = "{cipher}"
    ENCRYPTED_PATTERN = "^(\\((?P<context>.*)\\)|\\[(?P<options>.*)]){0,2}(?P<cipher>.*)$"
    UTF_8 = "utf-8"
    ACCESS_KEY_ID = None
    ACCESS_KEY_SECRET = None
    AES_KEY_ARN = "acs:kms:cn-shanghai:1196615123820121:key/9900c848-5626-4f64-9eb3-ec91493852d3"
    ENCRYPTION_CONTEXT = {"ValidKey": "@@JL*%$DF@VS"}
    client: AliyunCrypto = None
    aliyun_kms: AliyunKms = None

    def __init__(self, access_key_id=None, access_key_secret=None, ram_role_name=None, aes_key_arn=None, encryption_context=None):
        if not (access_key_id and access_key_secret) and not ram_role_name:
            raise Exception("RamRoleName or AK/SK cannot be null")
        if ram_role_name and len(ram_role_name) > 0:
            self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET = KMSUtil.sts_aksk(ram_role_name)
        if access_key_id and access_key_secret and len(access_key_id) > 0 and len(access_key_secret) > 0:
            self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET = access_key_id, access_key_secret

        if aes_key_arn and len(aes_key_arn) > 0:
            self.AES_KEY_ARN = aes_key_arn
        if encryption_context and len(encryption_context) > 0:
            self.ENCRYPTION_CONTEXT = encryption_context
        config = AliyunConfig(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET)
        self.client = AliyunCrypto(config)
        self.aliyun_kms = AliyunKms(config)

    @staticmethod
    def parse_encrypted_token(cipher_text: str):
        temp = cipher_text.strip()
        if len(temp) > 0:
            if temp.startswith(KMSUtil.ENCRYPTED_PROPERTY_PREFIX):
                temp = temp[len(KMSUtil.ENCRYPTED_PROPERTY_PREFIX):]
            match_group = re.search(KMSUtil.ENCRYPTED_PATTERN, temp).groupdict()
            return KMSUtil.parse_encryption_context(match_group.get("context")), match_group.get("cipher")

    @staticmethod
    def parse_encryption_context(context: str):
        temp = context.strip()
        if temp and len(temp) > 0:
            dict = {}
            for pair in temp.split(","):
                kv = pair.split("=")
                if len(kv) > 1:
                    dict[kv[0]] = str(base64.b64decode(kv[1]), KMSUtil.UTF_8)
            return dict


    @staticmethod
    def sts_aksk(ram_role_name):
        if ram_role_name and len(ram_role_name) > 0:
            url = 'http://100.100.100.200/latest/meta-data/ram/security-credentials/%s'
            logging.info(url)
            headers = {
                "Content-Type": "application/json; charset=UTF-8"
            }

            res = requests.get(url % ram_role_name, headers=headers)
            if res.ok:
                result_json = json.dumps(res.text)
                if result_json:
                    return result_json['AccessKeyId'], result_json['AccessKeySecret']
            logging.error("sts failed!")

    def encrypt(self, plain_text):
        key = str_to_cmk(to_str(self.AES_KEY_ARN))
        request = EncryptRequest.EncryptRequest()
        request.set_accept_format('JSON')
        request.set_KeyId(key.raw_key_id)
        request.set_Plaintext(base64.b64encode(plain_text.encode(self.UTF_8)))
        if len(self.ENCRYPTION_CONTEXT) != 0:
            request.set_EncryptionContext(json.dumps(self.ENCRYPTION_CONTEXT))
        response = self.aliyun_kms._get_result(request, key)
        return response.get('CiphertextBlob')

    def decrypt(self, cipher_text, encryption_context=ENCRYPTION_CONTEXT):
        encrypted_data_key = EncryptedDataKey(
            to_bytes(self.AES_KEY_ARN),
            to_bytes(cipher_text)
        )
        return str(base64.b64decode(self.aliyun_kms.decrypt_data_key(encrypted_data_key, encryption_context)), self.UTF_8)

    def decrypt_envelope(self, data_id: str, cipher_text):
        encrypted_data_key = EncryptedDataKey(
            to_bytes(self.AES_KEY_ARN),
            to_bytes(cipher_text)
        )
        config_str = self.aliyun_kms.decrypt_data_key(encrypted_data_key, "")
        if config_str:
            if data_id.endswith(".properties"):
                import util.properties_util as props_util
                cipher_props = props_util.parse_properties(config_str.split("\n"))
                plain_props = {}
                if cipher_props:
                    for key, value in cipher_props.items():
                        if str(value).startswith(self.ENCRYPTED_PROPERTY_PREFIX):
                            plain_props[key] = self.decrypt(str(value)[str(value).rfind(')') + 1:])
                        else:
                            plain_props[key] = value
                return plain_props
            elif data_id.endswith(".yaml"):
                import yaml
                cipher_yaml = yaml.load(config_str, Loader=yaml.FullLoader)
                KMSUtil.decrypt_dict(cipher_yaml, self.decrypt)
                return cipher_yaml

    @staticmethod
    def decrypt_dict(data, _func):
        if data and isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    KMSUtil.decrypt_dict(value, _func)
                elif isinstance(value, str) and str(value).startswith(KMSUtil.ENCRYPTED_PROPERTY_PREFIX):
                    context, cipher = KMSUtil.parse_encrypted_token(value)
                    data[key] = _func(cipher, context)
                else:
                    data[key] = value

    # def build_client(cache=False):
    #     client = AliyunCrypto(aliyun_config)
    #     if cache:
    #         client.crypto_key_manager = CachingCryptoKeyManager(LocalDataKeyMaterialCache(), 5)
    #     return client

    # def encrypt(self, plain_text, encryption_context):
    #     print("原文: " + plain_text)
    #     provider = DefaultDataKeyProvider(AES_KEY_ARN)
    #     cipher_text, enc_material = self.client.encrypt(provider, base64.b64encode(plain_text.encode('utf-8')), encryption_context)
    #     cipher_text_str = base64.standard_b64encode(cipher_text).decode("utf-8")
    #     print(u"加密密文: " + cipher_text_str)
    #     return cipher_text_str
    #
    #
    # def decrypt(self, cipher_text):
    #     cipher_text_bytes = base64.standard_b64decode(cipher_text.encode("utf-8"))
    #     provider = DefaultDataKeyProvider(AES_KEY_ARN)
    #     plain_text, dec_material = self.client.decrypt(provider, cipher_text_bytes)
    #     print(u"解密结果: " + bytes.decode(plain_text))
    #     return plain_text


# def decrypt(key_arn, cipher_text, encryption_context):
#     aliyun_kms = AliyunKms(aliyun_config)
#     request = DecryptRequest.DecryptRequest()
#     request.set_accept_format('JSON')
#     request.set_CiphertextBlob(cipher_text.encode("utf-8"))
#     if encryption_context and len(encryption_context) != 0:
#         request.set_EncryptionContext(json.dumps(encryption_context))
#     response = aliyun_kms._get_result(request, str_to_cmk(to_str(key_arn)))
#     return str(base64.b64decode(response.get("Plaintext")), 'utf-8')

