import random
import string

class MonoalphabeticCipher:
    """
    Implementa un cifrado por sustitución monoalfabética, donde cada letra del alfabeto original
    es sustituida consistentemente por otra letra del alfabeto.
    Este cifrado es una forma simple de encriptación donde cada letra del texto plano es reemplazada
    por otra letra del alfabeto de manera única y constante a lo largo de todo el mensaje.
    Métodos:
        generate_substitution_alphabet(): Genera un diccionario con un alfabeto de sustitución aleatorio.
            Returns:
                dict: Un diccionario que mapea cada letra del alfabeto original a su sustitución.
        encrypt_monoalphabetic(text, substitution_alphabet): Encripta un texto usando el alfabeto de sustitución.
            Args:
                text (str): El texto a encriptar.
                substitution_alphabet (dict): El diccionario de sustitución a utilizar.
            Returns:
                str: El texto encriptado.
        decrypt_monoalphabetic(text, substitution_alphabet): Desencripta un texto usando el alfabeto de sustitución.
            Args:
                text (str): El texto a desencriptar.
                substitution_alphabet (dict): El diccionario de sustitución usado para encriptar.
            Returns:
                str: El texto desencriptado.
    Nota:
        El cifrado preserva las mayúsculas/minúsculas y los caracteres no alfabéticos permanecen sin cambios.
    """

    @staticmethod
    def generate_substitution_alphabet() -> dict:
        alphabet = list(string.ascii_lowercase)
        substitute_alphabet = alphabet[:]
        random.shuffle(substitute_alphabet)
        return dict(zip(alphabet, substitute_alphabet))

    @staticmethod
    def encrypt_monoalphabetic(text: str, substitution_alphabet: dict) -> str:
        result = []
        for char in text:
            if char.lower() in substitution_alphabet:
                new_char = substitution_alphabet[char.lower()]
                result.append(new_char.upper() if char.isupper() else new_char)
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def decrypt_monoalphabetic(text: str, substitution_alphabet: dict) -> str:
        inverse_alphabet = {v: k for k, v in substitution_alphabet.items()}
        return MonoalphabeticCipher.encrypt(text, inverse_alphabet)

    @staticmethod
    def encrypt_file(file_path: str, substitution_alphabet: dict, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text = MonoalphabeticCipher.encrypt_monoalphabetic(text, substitution_alphabet)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            MonoalphabeticCipher.encrypt_file(file_path, substitution_alphabet, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, substitution_alphabet: dict, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = MonoalphabeticCipher.decrypt_monoalphabetic(encrypted_text, substitution_alphabet)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")