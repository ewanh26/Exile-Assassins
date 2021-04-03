import base64

with open('clanBannerEncrypted.txt', 'r') as b64:
    b64_string = b64.read()
    b64_bytes = b64_string.encode('ascii')
    with open('clanBanner.png', 'wb') as img:
        img.write(base64.b64decode(b64_bytes))
