class CaesarCipher:
    """
    Una implementación del cifrado César clásico.
    El cifrado César es una técnica de cifrado por sustitución donde cada letra en el texto original
    es reemplazada por una letra que se encuentra un número fijo de posiciones más adelante en el alfabeto.
    Methods:
        encrypt_caesar(text: str, shift: int) -> str:
            Encripta un texto usando el cifrado César.
            Args:
                text (str): El texto a encriptar.
                shift (int): El número de posiciones a desplazar cada letra.
            Returns:
                str: El texto encriptado.
        decrypt_caesar(text: str, shift: int) -> str:
            Desencripta un texto que ha sido cifrado con César.
            Args:
                text (str): El texto cifrado a desencriptar.
                shift (int): El número de posiciones que se usó para cifrar.
            Returns:
                str: El texto desencriptado.
    """
    
    @staticmethod
    def encrypt_text(text: str, shift: int) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % 26 + base
                result.append(chr(shifted))
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt_text(text: str, shift: int) -> str:
        return CaesarCipher.encrypt_text(text, -shift)


    @staticmethod
    def encrypt_file(file_path: str, shift: int, output_file_path: str = None):
        
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text = CaesarCipher.encrypt_text(text, shift)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file")
            with open(file_path, 'w') as file:
                file.write("")
            CaesarCipher.encrypt_file(file_path, shift, output_file_path)
    
    @staticmethod
    def decrypt_file(file_path: str, shift: int, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = CaesarCipher.decrypt_text(encrypted_text, shift)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")