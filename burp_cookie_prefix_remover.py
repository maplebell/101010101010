import base64
from urllib.parse import unquote, quote

cookie_value = input("粘贴 notification Cookie 的值：").strip()

# 如果复制时连 Cookie 名称也带上了，一并处理
if cookie_value.startswith("notification="):
    cookie_value = cookie_value.split("=", 1)[1]

# 1. URL 解码
url_decoded = unquote(cookie_value)

# 2. Base64 解码
raw = base64.b64decode(url_decoded, validate=True)

print("\nURL 解码后：")
print(url_decoded)

print("\nBase64 解码后的长度：")
print(f"{len(raw)} 字节")

if len(raw) % 16 != 0:
    raise ValueError("密文长度不是 16 的倍数，可能没有正确解码")

if len(raw) < 32:
    raise ValueError("密文不足 32 字节，无法删除两个完整加密块")

print("\n按 16 字节分块：")
for index in range(0, len(raw), 16):
    block = raw[index:index + 16]
    print(f"块 {index // 16 + 1}: {block.hex()}")

# 3. 删除前面的 32 个二进制字节
trimmed = raw[32:]

print("\n删除前 32 字节后的长度：")
print(f"{len(trimmed)} 字节")

# 4. Base64 编码
new_base64 = base64.b64encode(trimmed).decode("ascii")

# 5. URL 编码
new_cookie = quote(new_base64, safe="")

print("\n新的 Base64 值：")
print(new_base64)

print("\n放入 Cookie 的值：")
print(new_cookie)
