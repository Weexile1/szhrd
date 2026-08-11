# -*- coding: utf-8 -*-
"""把 szhrd/index.html 发布到网上，打印可分享链接。"""
import json
import ssl
import urllib.request
from pathlib import Path

HTML = Path(__file__).resolve().parent / "index.html"
API = "https://brewpage.app/api/html?ns=szhrd&ttl=30"


def main():
    data = HTML.read_bytes()
    ctx = ssl.create_default_context()
    # 部分环境缺证书时也能上传
    try:
        ssl.get_default_verify_paths()
    except Exception:
        pass
    req = urllib.request.Request(
        API,
        data=data,
        headers={"Content-Type": "text/html; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.URLError:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            body = json.loads(resp.read().decode())

    print("游戏链接：", body.get("link"))
    print("过期时间：", body.get("expiresAt"))
    print("管理令牌：", body.get("ownerToken"), "(删页时用，请自行保存)")


if __name__ == "__main__":
    main()
