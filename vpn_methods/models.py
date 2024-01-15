import json


class ConfigInbound:
    def __init__(self, server_url, create_info):
        stream_settings = json.loads(create_info.get('streamSettings'))
        reality_settings = stream_settings.get('realitySettings')

        self.id = create_info.get('id')
        self.url = server_url
        self.port = create_info.get('port')
        self.transmission = stream_settings.get('network')
        self.security = stream_settings.get('security')
        self.public_key = reality_settings.get('settings').get('publicKey')
        self.private_key = reality_settings.get('privateKey')
        self.fingerprint = reality_settings.get('settings').get('fingerprint')
        self.server_name = reality_settings.get('serverNames')[0]
        self.short_id = reality_settings.get('shortIds')[0]
        self.remark = create_info.get('remark')


class ConfigClient:
    def __init__(self, server_url, client_id, sub_id, flow, email, inbound_id):
        self.url = server_url
        self.id = client_id
        self.sub_id = sub_id
        self.flow = flow
        self.email = email
        self.inbound_id = inbound_id
        self.active = True
