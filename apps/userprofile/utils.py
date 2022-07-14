import hashlib


def encrypt_password(password):
    # 加盐方式，使用md5算法对密码进行加密
    md5 = hashlib.md5()
    sign_str = password + '#@%^&*'
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')

    md5.update(sign_bytes_utf8)
    encrypted_password = md5.hexdigest()

    return encrypted_password
