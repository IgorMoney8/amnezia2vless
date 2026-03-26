import json
import urllib.parse
import os

def convert_json_to_vless(json_file, custom_name):
    if not os.path.exists(json_file):
        raise FileNotFoundError({
    "dns": {
        "queryStrategy": "UseIP",
        "servers": [
            "8.8.8.8",
            "8.8.4.4"
        ]
    },
    "inbounds": [
        {
            "listen": "127.0.0.1",
            "port": 10808,
            "protocol": "socks",
            "settings": {
                "auth": "noauth",
                "udp": true
            },
            "sniffing": {
                "destOverride": [
                    "http",
                    "tls",
                    "quic"
                ],
                "enabled": true,
                "routeOnly": false
            },
            "tag": "socks"
        },
        {
            "listen": "127.0.0.1",
            "port": 10809,
            "protocol": "http",
            "settings": {
                "allowTransparent": false
            },
            "sniffing": {
                "destOverride": [
                    "http",
                    "tls",
                    "quic"
                ],
                "enabled": true,
                "routeOnly": false
            },
            "tag": "http"
        }
    ],
    "meta": null,
    "outbounds": [
        {
            "fragment": {
                "interval": "10-20",
                "length": "50-100",
                "packets": "tlshello"
            },
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": "universal1.unitedbeavers.com",
                        "port": 443,
                        "users": [
                            {
                                "encryption": "none",
                                "flow": "xtls-rprx-vision",
                                "id": "940b3509-0f9d-4a1e-b8a9-c31b33a5374c"
                            }
                        ]
                    }
                ]
            },
            "streamSettings": {
                "network": "tcp",
                "realitySettings": {
                    "fingerprint": "qq",
                    "publicKey": "V6FabatADtcX7aO9KMjGCadJC4LuQ_5nRViab-z-nFQ",
                    "serverName": "eh.vk.com",
                    "shortId": "37",
                    "show": false
                },
                "security": "reality"
            },
            "tag": "proxy"
        },
        {
            "protocol": "freedom",
            "tag": "direct"
        },
        {
            "protocol": "blackhole",
            "tag": "block"
        }
    ],
    "remarks": "🇳🇱 LTE Универсальный №1 🏳️",
    "routing": {
        "domainMatcher": "hybrid",
        "domainStrategy": "IPIfNonMatch",
        "rules": [
            {
                "outboundTag": "direct",
                "protocol": [
                    "bittorrent"
                ],
                "type": "field"
            },
            {
                "domain": [
                    "full:universal1.unitedbeavers.com"
                ],
                "outboundTag": "direct",
                "type": "field"
            }
        ]
    }
}
)
    with open(json_file, 'r') as f:
        config = json.load(f)
    outbound = config['outbounds'][0]
    vnext = outbound['settings']['vnext'][0]
    user = vnext['users'][0]
    reality = outbound['streamSettings']['realitySettings']
    vless_params = {
        'id': user['id'],
        'address': vnext['address'],
        'port': vnext['port'],
        'security': outbound['streamSettings']['security'],
        'sni': reality['serverName'],
        'fp': reality['fingerprint'],
        'pbk': reality['publicKey'],
        'sid': reality['shortId'],
        'type': outbound['streamSettings']['network'],
        'flow': user['flow'],
        'encryption': user['encryption']
    }
    vless_url = (f"vless://{vless_params['id']}@{vless_params['address']}:{vless_params['port']}"
                 f"?security={vless_params['security']}"
                 f"&sni={urllib.parse.quote(vless_params['sni'])}"
                 f"&fp={vless_params['fp']}"
                 f"&pbk={urllib.parse.quote(vless_params['pbk'])}"
                 f"&sid={vless_params['sid']}"
                 f"&type={vless_params['type']}"
                 f"&flow={vless_params['flow']}"
                 f"&encryption={vless_params['encryption']}"
                 f"#{urllib.parse.quote(custom_name)}")
    
    return vless_url

def save_to_file(vless_url, custom_name):
    safe_name = "".join(c for c in custom_name if c.isalnum() or c in ('-', '_')).rstrip()
    if not safe_name:
        safe_name = "VLESS-Default"
    output_file = f"{safe_name}.txt"
    with open(output_file, 'w') as f:
        f.write(vless_url)
    print(f"Ключ сохранен в файл: {output_file}")
if __name__ == "__main__":
    json_file = input("Введите имя JSON-файла (например, User-XRay.json): ").strip()
    if not json_file:
        json_file = "Xray.json"
    custom_name = input("Введите имя для ключа VLESS (например, User-VLESS): ").strip()
    if not custom_name:
        custom_name = "VLESS-Default"
    try:
        vless_key = convert_json_to_vless(json_file, custom_name)
        print("Сгенерированный ключ VLESS:")
        print(vless_key)
        save_to_file(vless_key, custom_name)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")
