from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

class DESCipher:
    """
    Clase que implementa el cifrado y descifrado DES (Data Encryption Standard).
    Esta clase proporciona métodos estáticos para cifrar y descifrar texto utilizando el algoritmo DES
    en modo CBC (Cipher Block Chaining).
    Métodos:
        encrypt_des(text: str, key: bytes) -> bytes:
            Cifra el texto proporcionado usando DES en modo CBC.
            Args:
                text (str): El texto a cifrar
                key (bytes): La clave de cifrado (se ajustará a 8 bytes)
            Returns:
                bytes: Vector de inicialización (IV) concatenado con el texto cifrado
        decrypt_des(encrypted_text: bytes, key: bytes) -> str:
            Descifra el texto cifrado usando DES en modo CBC.
            Args:
                encrypted_text (bytes): IV + texto cifrado en formato bytes
                key (bytes): La clave de descifrado (se ajustará a 8 bytes)
            Returns:
                str: El texto descifrado
    """
    @staticmethod
    def encrypt_des(text: str, key: bytes) -> bytes:
        key = key.ljust(8, b'\0')[:8]
        cipher = DES.new(key, DES.MODE_CBC)
        padded_text = pad(text.encode(), DES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return cipher.iv + encrypted_text

    @staticmethod
    def decrypt_des(encrypted_text: bytes, key: bytes) -> str:
        key = key.ljust(8, b'\0')[:8]
        iv = encrypted_text[:8]
        encrypted_text = encrypted_text[8:]
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted_text = unpad(cipher.decrypt(encrypted_text), DES.block_size)
        return decrypted_text.decode()
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_data = DESCipher.encrypt_des(text, key)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            DESCipher.encrypt_file(file_path, key, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_text = DESCipher.decrypt_des(encrypted_data, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")