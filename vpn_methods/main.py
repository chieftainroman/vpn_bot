import base64
import random
import re
import string
from uuid import uuid4 as generate_id

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

from app.database import ConfigInbound, ConfigClient

DEFAULT_HEADERS = {
    'Accept': 'application/json'
}

# def main():
#     with requests.Session() as s:
#         data = {
#             'username': ADMIN_LOGIN,
#             'password': ADMIN_PASSWORD,
#         }
#
#         login_resp = s.post(SERVER_URL + "/login", data=data)
#         print(login_resp.json())
#
#         """
#         Inbound создается только при добавлении сервера в админке, сервер добавляется посредством ввода url'a сервера. Далее Inbound сохраняется в базу,
#         он нам будет нужен для генерации конфигов для клиента этого сервера. Тут стоит обратить внимание что этот созданный Inbound представление того что создано на VPN сервере.
#         Но так как апи писали долбоебы, там нет метода получения этих настроек, из-за чего хранить эти настройки мы будем у себя в базе. Стоит создать отдельный class Inbound,
#         который ссылается на ConfigInbound, но хранит в себе инфу и методы нужные для логики телеграм бота. Все тоже самое с ConfigClient, нужно создать отдельный Client,
#         с которым будет происходить много манипуляций, включая отключение/подключение подписки.
#         """
#
#         inbound_resp = add_inbound(s)
#         if inbound_resp.get('success'):
#             inbound = ConfigInbound(inbound_resp.get('obj'))
#             client_resp, client_args = add_client(s, 0, inbound.id)
#             if client_resp.get('success'):
#                 client = ConfigClient(*client_args)
#                 print(client)
#                 print(generate_config(client, inbound))
#             else:
#                 return "Возникла ошибка, пожалуйста, обратитесь к тех. поддержке"
#
#         else:
#             return "Возникла ошибка, пожалуйста, проконсультируйтесь с техническими специалистами"


def add_client(session, expiry_time, inbound_id, server_url):
    flow = "xtls-rprx-vision"
    alter_id = generate_id()
    email = random_lower_and_num(8)
    sub_id = random_lower_and_num(16)

    data = {
        'id': inbound_id,
        'settings': '{{"clients": [{{\n  "id": "{alter_id}",\n  "flow": "{flow}",\n  "email": "{email}",\n  "limitIp": 1,\n  "totalGB": 0,\n  "expiryTime": {expiry_time},\n  "enable": true,\n  "tgId": "",\n  "subId": "{sub_id}",\n  "reset": 0\n}}]}}'.format(
            flow=flow, expiry_time=expiry_time, alter_id=alter_id, email=email, sub_id=sub_id
        ),
    }

    response = session.post(server_url + "/panel/api/inbounds/addClient", headers=DEFAULT_HEADERS, data=data)
    # print(response.json())

    return response.json(), [str(alter_id), sub_id, flow, email, inbound_id]


def add_inbound(session, server_url):
    alter_id = generate_id()
    email = random_lower_and_num(8)
    sub_id = random_lower_and_num(16)
    short_id = random_short_id()
    private_key, public_key = generate_cert()

    data = {
        'up': '0',
        'down': '0',
        'total': '0',
        'remark': 'server2',
        'enable': 'true',
        'expiryTime': '0',
        'listen': '',
        'port': '443',
        'protocol': 'vless',
        'settings': '{{\n  "clients": [\n    {{\n      "id": "{alter_id}",\n      "flow": "xtls-rprx-vision",\n      "email": "{email}",\n      "limitIp": 0,\n      "totalGB": 0,\n      "expiryTime": 0,\n      "enable": true,\n      "tgId": "",\n      "subId": "{sub_id}",\n      "reset": 0\n    }}\n  ],\n  "decryption": "none",\n  "fallbacks": []\n}}'.format(
            alter_id=alter_id, email=email, sub_id=sub_id),
        'streamSettings': '{{\n  "network": "tcp",\n  "security": "reality",\n  "externalProxy": [],\n  "realitySettings": {{\n    "show": false,\n    "xver": 0,\n    "dest": "google.com:443",\n    "serverNames": [\n      "google.com",\n      "www.google.com"\n    ],\n    "privateKey": "{private_key}",\n    "minClient": "",\n    "maxClient": "",\n    "maxTimediff": 0,\n    "shortIds": [\n      "{short_id}"\n    ],\n    "settings": {{\n      "publicKey": "{public_key}",\n      "fingerprint": "firefox",\n      "spiderX": "/"\n    }}\n  }},\n  "tcpSettings": {{\n    "acceptProxyProtocol": false,\n    "header": {{\n      "type": "none"\n    }}\n  }}\n}}'.format(
            short_id=short_id, private_key=private_key, public_key=public_key),
        'sniffing': '{\n  "enabled": true,\n  "destOverride": [\n    "http",\n    "tls",\n    "quic",\n    "fakedns"\n  ]\n}',
    }
    response = session.post(server_url + "/panel/api/inbounds/add", headers=DEFAULT_HEADERS, data=data)
    print(response.json())

    return response.json()


def random_short_id(length=8):
    characters = '0123456789abcdef'
    return ''.join(random.choice(characters) for _ in range(length))


def random_lower_and_num(length):
    characters = string.digits + string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))


def generate_cert():
    private_key = x25519.X25519PrivateKey.generate()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').rstrip("=")

    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip("=")

    return private_key_b64, public_key_b64


def format_domain(url):
    new_url = re.sub(r'^https?://', '', url)
    return re.sub(r':\d+$', '', new_url)


def generate_config(client: ConfigClient, inbound: ConfigInbound):
    return "vless://{client_id}@{inbound_domain}:{port}?type={inbound_transmission}&security={inbound_security}&pbk={public_key}&fp={inbound_fingerprint}&sni={inbound_server_name}&sid={inbound_short_id}&spx=%2F&flow={client_flow}#{inbound_remark}-{client_email}".format(
        client_id=client.id, inbound_domain=format_domain(inbound.url), port=inbound.port, inbound_transmission=inbound.transmission, inbound_security=inbound.security, public_key=inbound.public_key,
        inbound_fingerprint=inbound.fingerprint, inbound_server_name=inbound.server_name, inbound_short_id=inbound.short_id, client_flow=client.flow, inbound_remark=inbound.remark,
        client_email=client.email
    )
