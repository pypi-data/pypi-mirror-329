import os
import base64
import hashlib

def xor_bytes(data, key):
    return bytes(a ^ b for a, b in zip(data, key))

def pad(data, block_size):
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    return data[:-data[-1]]

def crypto(action: str, data: str, key: bytes, algorithm: str) -> str:
    if action == "hash":
        if algorithm == "SHA-256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "SHA-512":
            return hashlib.sha512(data.encode()).hexdigest()
        elif algorithm == "MD5":
            return hashlib.md5(data.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hashing algorithm.")

    elif action in ["encrypt", "decrypt"]:
        if algorithm in ["AES", "DES", "3DES", "Blowfish"]:
            if algorithm == "AES":
                key = hashlib.sha256(key).digest()
                iv_size = 16
                block_size = 16
            elif algorithm == "DES":
                key = hashlib.md5(key).digest()[:8]
                iv_size = 8
                block_size = 8
            elif algorithm == "3DES":
                key = hashlib.sha256(key).digest()[:24]
                iv_size = 8
                block_size = 8
            elif algorithm == "Blowfish":
                key = hashlib.sha256(key).digest()[:16]
                iv_size = 8
                block_size = 8

            if action == "encrypt":
                iv = os.urandom(iv_size)
                padded_text = pad(data.encode(), block_size)
                ciphertext = xor_bytes(padded_text, key[:block_size])
                return base64.b64encode(iv + ciphertext).decode()

            elif action == "decrypt":
                raw_data = base64.b64decode(data)
                iv, ciphertext = raw_data[:iv_size], raw_data[iv_size:]
                decrypted = xor_bytes(ciphertext, key[:block_size])
                return unpad(decrypted).decode()

        elif algorithm == "RC4":
            key = hashlib.md5(key).digest()
            S = list(range(256))
            j = 0
            out = bytearray()

            for i in range(256):
                j = (j + S[i] + key[i % len(key)]) % 256
                S[i], S[j] = S[j], S[i]

            i = j = 0
            for char in data.encode() if action == "encrypt" else base64.b64decode(data):
                i = (i + 1) % 256
                j = (j + S[i]) % 256
                S[i], S[j] = S[j], S[i]
                out.append(char ^ S[(S[i] + S[j]) % 256])

            return base64.b64encode(bytes(out)).decode() if action == "encrypt" else bytes(out).decode()

        else:
            raise ValueError("Unsupported algorithm.")

    else:
        raise ValueError("Invalid action.")
