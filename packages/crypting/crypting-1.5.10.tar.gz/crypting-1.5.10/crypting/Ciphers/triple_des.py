from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class TripleDESCipher:
    """
    Clase que implementa cifrado y descifrado usando Triple DES (3DES).
    Esta clase proporciona métodos estáticos para realizar operaciones criptográficas
    usando el algoritmo Triple DES en modo CBC (Cipher Block Chaining).
    El Triple DES aplica el algoritmo DES tres veces a cada bloque de datos
    usando dos o tres claves diferentes, proporcionando un nivel de seguridad
    mayor que el DES simple.
    Métodos:
        generate_key() -> bytes:
            Genera una clave aleatoria válida de 24 bytes para Triple DES.
        encrypt_des3(text: str, key: bytes) -> bytes:
            Cifra un texto usando Triple DES en modo CBC.
        decrypt_des3(encrypted_data: bytes, key: bytes) -> str:
            Descifra datos previamente cifrados con Triple DES.
        validate_key(key: bytes) -> bool:
            Valida si una clave es adecuada para usar con Triple DES.
    Notas:
        - Utiliza padding PKCS7 para manejar textos de longitud arbitraria
        - Opera en modo CBC para mayor seguridad
        - Requiere claves de 16 o 24 bytes (128 o 192 bits)
        - El IV (vector de inicialización) se genera automáticamente y se incluye
        en los datos cifrados
    """

    @staticmethod
    def generate_key() -> bytes:
        """
        Genera una clave valida para el Triple DES

        Returns:
            bytes: Una clave de 24 bytes (necesaria para el Triple DES)
        """

        while True:
            try:
                key = get_random_bytes(24) # 24 bytes = 192 bits
                # Verifica que la clave sea valida para Triple DES
                DES3.adjust_key_parity(key)
                return key
            except ValueError:
                # Si la clave no es valida, genera otra
                continue
    
    @staticmethod
    def encrypt_des3(text: str, key: bytes) -> bytes:
        """
        Cifra un texto usando Tripe DES en modo CBC

        Args:
            text: El texto a cifrar
            key: Clave de 16 o 24 bytes (128 o 192 bits)

        Returns:
            bytes: IV + texto cifrado

        Raises:
            ValueError: Si la clave no tiene la longitud correcta o no es valida
        """
        try:
            # Ajusta la paridad de la clave
            key = DES3.adjust_key_parity(key)

            # Crea el objeto cipher en modo CBC
            cipher = DES3.new(key, DES3.MODE_CBC)

            # Cifra el texto con padding
            padded_text = pad(text.encode(), DES3.block_size)
            encrypted_text = cipher.encrypt(padded_text)

            # Retorna IV + texto cifrado
            return cipher.iv + encrypted_text
        
        except ValueError as e:
            raise ValueError(f"Error con la clave 3DES: {str(e)}")
        
    @staticmethod
    def decrypt_des3(encrypted_data: bytes, key: bytes) -> str:
        """
        Descifra datos cifrados con Triple DES.
        
        Args:
            encrypted_data: IV + datos cifrados
            key: La misma clave usada para cifrar (16 o 24 bytes)
        
        Returns:
            str: El texto descifrado
            
        Raises:
            ValueError: Si la clave no es válida o los datos están corruptos
        """
        try:
            # Ajusta la paridad de la clave
            key = DES3.adjust_key_parity(key)
            
            # Extrae el IV (primeros 8 bytes)
            iv = encrypted_data[:8]
            ciphertext = encrypted_data[8:]
            
            # Crea el objeto cipher con la clave y el IV
            cipher = DES3.new(key, DES3.MODE_CBC, iv)
            
            # Descifra y quita el padding
            padded_text = cipher.decrypt(ciphertext)
            text = unpad(padded_text, DES3.block_size)
            
            return text.decode()
            
        except ValueError as e:
            raise ValueError(f"Error al descifrar: {str(e)}")

    @staticmethod
    def validate_key(key: bytes) -> bool:
        """
        Valida si una clave es adecuada para Triple DES.
        
        Args:
            key: La clave a validar
        
        Returns:
            bool: True si la clave es válida, False en caso contrario
        """
        try:
            adjusted_key = DES3.adjust_key_parity(key)
            # Intenta crear un objeto cipher para verificar la clave
            DES3.new(adjusted_key, DES3.MODE_CBC)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        """
        Encripta un archivo usando Triple DES en modo CBC.

        Args:
            file_path (str): Ruta del archivo a encriptar.
            key (bytes): Clave de 16 o 24 bytes para Triple DES.
            output_file_path (str, optional): Ruta del archivo encriptado. Si no se proporciona, se usa la ruta original con extensión .enc.

        Raises:
            ValueError: Si la clave no es válida o el archivo no existe.
        """
        try:
            with open(file_path, 'rb') as file:
                plaintext = file.read()
            encrypted_data = TripleDESCipher.encrypt_des3(plaintext.decode(), key)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            TripleDESCipher.encrypt_file(file_path, key, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        """
        Desencripta un archivo previamente encriptado con Triple DES.

        Args:
            file_path (str): Ruta del archivo encriptado.
            key (bytes): Clave de 16 o 24 bytes usada para encriptar.
            output_file_path (str, optional): Ruta del archivo desencriptado. Si no se proporciona, se usa la ruta original con extensión .dec.

        Raises:
            ValueError: Si la clave no es válida o el archivo no existe.
        """
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_text = TripleDESCipher.decrypt_des3(encrypted_data, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")