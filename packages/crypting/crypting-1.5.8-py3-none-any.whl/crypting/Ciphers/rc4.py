class RC4Cipher:
    """
    Implementación del cifrado RC4 (Rivest Cipher 4).
    El cifrado RC4 es un algoritmo de cifrado de flujo diseñado por Ron Rivest para RSA Security.
    Este cifrado utiliza una clave para generar un flujo de bytes pseudoaleatorio que se combina
    con el texto plano mediante operaciones XOR.
    Métodos:
        _init_sbox(key: bytes) -> list:
            Inicializa la S-box del algoritmo RC4 usando la clave proporcionada.
            Args:
                key: Clave en bytes para inicializar la S-box.
            Returns:
                Lista que representa la S-box inicializada.
        encrypt_rc4(text: str, key: bytes) -> bytes:
            Cifra un texto usando el algoritmo RC4.
            Args:
                text: Texto plano a cifrar.
                key: Clave en bytes para el cifrado.
            Returns:
                Texto cifrado en bytes.
        decrypt_rc4(encrypted_text: bytes, key: bytes) -> str:
            Descifra un texto previamente cifrado con RC4.
            Args:
                encrypted_text: Texto cifrado en bytes.
                key: Clave en bytes para el descifrado.
            Returns:
                Texto descifrado como string.
    Advertencia:
        RC4 se considera inseguro para aplicaciones que requieren alta seguridad criptográfica.
        Se recomienda usar algoritmos más modernos para aplicaciones críticas.
    """

    @staticmethod
    def _init_sbox(key: bytes) -> list:
        S = list(range(256))
        j = 0
        key_length = len(key)
        
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
            
        return S

    @staticmethod
    def encrypt_rc4(text: str, key: bytes) -> bytes:
        S = RC4Cipher._init_sbox(key)
        i = j = 0
        result = []
        
        for byte in text.encode():
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            result.append(byte ^ k)
            
        return bytes(result)

    @staticmethod
    def decrypt_rc4(encrypted_text: bytes, key: bytes) -> str:
        S = RC4Cipher._init_sbox(key)
        i = j = 0
        result = []
        
        for byte in encrypted_text:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            result.append(byte ^ k)
            
        return bytes(result).decode()
    
    @staticmethod
    def encrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_data = RC4Cipher.encrypt_rc4(text, key)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            RC4Cipher.encrypt_file(file_path, key, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_text = RC4Cipher.decrypt_rc4(encrypted_data, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")