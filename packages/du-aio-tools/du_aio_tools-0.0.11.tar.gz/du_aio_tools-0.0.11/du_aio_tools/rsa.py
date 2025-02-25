import json
import os
from hashlib import md5

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64


def make_md5(s: str, encoding='utf-8') -> str:
    """加密"""
    return md5(s.encode(encoding)).hexdigest()


class RsaCrypto:
    def __init__(self, b=1024, dir='./'):
        random_generator = Random.new().read
        self.rsa = RSA.generate(b, random_generator)
        self.dir = dir

    def create_rsa_key(self):
        """生成RSA秘钥对"""
        public_key = self.rsa.publickey().exportKey()  # 公钥
        private_key = self.rsa.exportKey()  # 私钥
        with open(os.path.join(self.dir, "id_rsa.pub"), 'wb') as f2:
            f2.write(public_key)
        with open(os.path.join(self.dir, "id_rsa"), 'wb') as f:
            f.write(private_key)

    def encrypt(self, text, public_key=None):
        """加密"""
        if not public_key:
            with open(os.path.join(self.dir, 'id_rsa.pub')) as f:
                public_key = f.read()
        pub_key = RSA.importKey(str(public_key))
        cipher = PKCS1_cipher.new(pub_key)
        rsa_text = base64.b64encode(cipher.encrypt(bytes(text.encode("utf8"))))
        # print(rsa_text.decode('utf-8'))
        return rsa_text.decode('utf-8')

    def decrypt(self, text_data, private_key=None):
        """解密"""
        if not private_key:
            with open(os.path.join(self.dir, 'id_rsa')) as f:
                private_key = f.read()
        pri_key = RSA.importKey(private_key)
        cipher = PKCS1_cipher.new(pri_key)
        back_text = cipher.decrypt(base64.b64decode(text_data), 0)
        # print(back_text.decode('utf-8'))
        return back_text.decode('utf-8')


r = RsaCrypto()


def create_rsa_key():
    """加密"""
    return r.create_rsa_key()


def encrypt(text):
    """加密"""
    return r.encrypt(text)


def decrypt(text):
    """解密"""
    return r.decrypt(text)


if __name__ == "__main__":
    data = {"user": "1959474", "name": "H, DJ"}
    a = create_rsa_key()
    a = encrypt(json.dumps(data))
    b = decrypt(a)
    print(a)
    print(json.loads(b))
