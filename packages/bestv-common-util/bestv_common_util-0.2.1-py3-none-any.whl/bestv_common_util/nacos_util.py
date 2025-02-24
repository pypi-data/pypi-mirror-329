import logging
import json
import nacos
from .kms_util import KMSUtil


class NacosUtil:
    ACCESS_KEY_ID = None
    ACCESS_KEY_SECRET = None
    nacos_client = None
    kms_util: KMSUtil = None
    data_id = None

    def __init__(self, **kwargs):
        """
        :param kwargs:
        : server_addresses
        : namespace
        : access_key_id
        : access_key_secret
        : ram_role_name
        : aes_key_arn
        : encryption_context
        : kms_util
        """
        server_addresses = kwargs.get('server_addresses')
        namespace = kwargs.get('namespace')
        access_key_id = kwargs.get('access_key_id')
        access_key_secret = kwargs.get('access_key_secret')
        ram_role_name = kwargs.get('ram_role_name')
        aes_key_arn = kwargs.get('aes_key_arn')
        encryption_context = kwargs.get('encryption_context')
        kms_util = kwargs.get('kms_util')
        self.data_id = kwargs.get('data_id')

        if not (access_key_id and access_key_secret) and not ram_role_name:
            raise Exception("RamRoleName or AK/SK cannot be null")
        if ram_role_name and len(ram_role_name) > 0:
            self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET = KMSUtil.sts_aksk(ram_role_name)
        if access_key_id and access_key_secret and len(access_key_id) > 0 and len(access_key_secret) > 0:
            self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET = access_key_id, access_key_secret
        self.nacos_client = nacos.NacosClient(server_addresses, namespace=namespace,
                                         ak=self.ACCESS_KEY_ID, sk=self.ACCESS_KEY_SECRET)
        if kms_util:
            self.kms_util = kms_util
        else:
            self.kms_util = KMSUtil(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, aes_key_arn=aes_key_arn, encryption_context=encryption_context)

    def get_config(self, data_id=None, group='DEFAULT_GROUP'):
        if data_id and len(data_id) > 0:
            self.data_id = data_id
        if self.data_id and len(self.data_id) > 0:
            cipher_props = self.nacos_client.get_config(self.data_id, group)
            nacos_props = self.kms_util.decrypt_envelope(self.data_id, cipher_props)

            if self.data_id.endswith('.properties'):
                return json.dumps(props_util.properties_to_dict(nacos_props))
            return json.dumps(nacos_props)
        raise Exception("data_id cannot be null without a default value")
