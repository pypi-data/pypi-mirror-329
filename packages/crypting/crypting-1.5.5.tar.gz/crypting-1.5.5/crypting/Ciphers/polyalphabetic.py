import string

class PolyalphabeticCipher:
    """
    Una implementación del cifrado polialfabético (también conocido como cifrado de Vigenère).
    Este cifrador utiliza múltiples alfabetos de sustitución basados en una clave para cifrar texto.
    A diferencia del cifrado monoalfabético, cada letra en el texto puede ser sustituida por 
    diferentes letras dependiendo de su posición y la clave utilizada.
    Métodos:
        _clean_text(text: str) -> str:
            Limpia el texto de entrada eliminando caracteres no alfabéticos y convirtiendo a mayúsculas.
        encrypt_polyalphabetic(text: str, key: str) -> str:
            Cifra el texto utilizando el algoritmo polialfabético.
            Args:
                text: El texto a cifrar
                key: La clave de cifrado
            Returns:
                El texto cifrado en mayúsculas
        decrypt_polyalphabetic(text: str, key: str) -> str:
            Descifra el texto utilizando el algoritmo polialfabético.
            Args:
                text: El texto cifrado
                key: La clave de cifrado original
            Returns:
                El texto descifrado en mayúsculas
    Ejemplo:
        >>> cipher = PolyalphabeticCipher()
        >>> cipher.encrypt_polyalphabetic("HOLA", "CLAVE")
        'JZLN'
        >>> cipher.decrypt_polyalphabetic("JZLN", "CLAVE")
        'HOLA'
    """

    @staticmethod
    def _clean_text(text: str) -> str:
        return ''.join(c for c in text.upper() if c in string.ascii_uppercase)

    @staticmethod
    def encrypt_polyalphabetic(text: str, key: str) -> str:
        alphabet = string.ascii_uppercase
        clean_text = PolyalphabeticCipher._clean_text(text)
        clean_key = PolyalphabeticCipher._clean_text(key)
        
        result = []
        for i, char in enumerate(clean_text):
            if char in alphabet:
                shift = alphabet.index(clean_key[i % len(clean_key)])
                new_char = alphabet[(alphabet.index(char) + shift) % 26]
                result.append(new_char)
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt_polyalphabetic(text: str, key: str) -> str:
        alphabet = string.ascii_uppercase
        clean_text = PolyalphabeticCipher._clean_text(text)
        clean_key = PolyalphabeticCipher._clean_text(key)
        
        result = []
        for i, char in enumerate(clean_text):
            if char in alphabet:
                shift = alphabet.index(clean_key[i % len(clean_key)])
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
                result.append(new_char)
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def encrypt_file(file_path: str, key: str, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text = PolyalphabeticCipher.encrypt_polyalphabetic(text, key)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            PolyalphabeticCipher.encrypt_file(file_path, key, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, key: str, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = PolyalphabeticCipher.decrypt_polyalphabetic(encrypted_text, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
