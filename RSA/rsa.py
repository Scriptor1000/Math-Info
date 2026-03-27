import sympy, secrets
from euclidean_alg import get_modular_inverse
from dataclasses import dataclass
from square_multiply import sam

@dataclass
class PrivateKey:
    n: int # PUBLIC
    e: int # PUBLIC

    m: int # PRIVATE
    d: int # PRIVATE

    def __init__(self):
        p = sympy.nextprime(secrets.randbits(256))
        q = sympy.nextprime(secrets.randbits(256))

        self.n = p * q
        self.m = (p - 1) * (q - 1)

        self.e = 65537
        self.d = get_modular_inverse(self.e, self.m)

    def to_public(self):
        return PublicKey(self.n, self.e)

    def _decrypt(self, message: int):
        return sam(message, self.d, self.n)

    def decrypt(self, message: list[int]):
        decrypted_message = ""
        for c in message:
            decrypted_message += self._decrypt(c).to_bytes().decode('UTF-8')
        return decrypted_message

@dataclass
class PublicKey:
    n: int
    e: int

    def _encrypt(self, message: int):
        return sam(message, self.e, self.n)

    def encrypt(self, message: str):
        encrypted_message = []
        for c in message:
            encrypted_message.append(self._encrypt(int.from_bytes(c.encode('UTF-8'))))
        return encrypted_message


if __name__ == '__main__':
    print("Create Public Key")
    private_key = PrivateKey()
    public_key = private_key.to_public()
    print("Encrypting")
    m = "Hallo Welt!"
    encrypted = public_key.encrypt(m)
    print("Decrypting")
    decrypted = private_key.decrypt(encrypted)
    if decrypted == m:
       print("Success!")
    else:
       print("Fail!")