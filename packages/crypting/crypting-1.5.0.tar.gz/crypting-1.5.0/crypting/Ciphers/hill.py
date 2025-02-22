import numpy as np
from typing import List, Tuple

class HillCipher:
    """
    A class implementing the Hill cipher encryption and decryption algorithm.
    The Hill cipher is a polygraphic substitution cipher based on linear algebra.
    It uses a matrix as the key to encrypt blocks of plaintext letters.
    Methods:
        matrix_mod_inverse(matrix, modulus): Calculate modular multiplicative inverse of matrix
        text_to_numbers(text): Convert text to numbers (A=0 to Z=25)
        numbers_to_text(numbers): Convert numbers back to text
        pad_text(numbers, block_size): Pad text to fit block size
        encrypt_hill(text, key_matrix): Encrypt text using Hill cipher
        decrypt_hill(text, key_matrix, padding_count): Decrypt Hill cipher text
    Note:
        - Only works with uppercase letters A-Z
        - Key matrix must be invertible modulo 26
        - Text length must be multiple of key matrix size (padding is added if needed)
    """
    
    @staticmethod
    def matrix_mod_inverse(matrix: np.ndarray, modulus: int) -> np.ndarray:
        """Calculate the modular multiplicative inverse of a matrix."""
        det = int(round(np.linalg.det(matrix)))
        det_inverse = pow(det % modulus, -1, modulus)
        adjugate = np.round(det * np.linalg.inv(matrix)).astype(int)
        return np.mod(adjugate * det_inverse, modulus)

    @staticmethod
    def text_to_numbers(text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)."""
        try:
            numbers = []
            for c in str(text):  # Aseguramos que text sea string
                if c.isalpha():
                    number = ord(c.upper()) - ord('A')
                    numbers.append(number)
            return numbers
        except Exception as e:
            print(f"Error en text_to_numbers: {e}")
            raise

    @staticmethod
    def numbers_to_text(numbers: List[int]) -> str:
        """Convert numbers back to text."""
        return ''.join(chr(int(n) % 26 + ord('A')) for n in numbers)

    @staticmethod
    def pad_text(numbers: List[int], block_size: int) -> Tuple[List[int], int]:
        padding = block_size - (len(numbers) % block_size)
        if padding < block_size:
            return numbers + [23] * padding, padding
        return numbers, 0

    @staticmethod
    def encrypt_hill(text: str, key_matrix: List[List[int]]) -> Tuple[str, int]:
        """Encrypt text using HillCipher cipher."""
        key = np.array(key_matrix, dtype=int)
        block_size = len(key_matrix)
        
        numbers = HillCipher.text_to_numbers(text)
        numbers, padding_count = HillCipher.pad_text(numbers, block_size)
        
        result = []
        for i in range(0, len(numbers), block_size):
            block = np.array(numbers[i:i + block_size], dtype=int)
            encrypted_block = np.mod(np.dot(key, block), 26)
            result.extend(encrypted_block)
            
        return HillCipher.numbers_to_text(result), padding_count

    @staticmethod
    def decrypt_hill(text: str, key_matrix: List[List[int]], padding_count: int = 0) -> str:
        """Decrypt text using HillCipher cipher."""
        key = np.array(key_matrix, dtype=int)
        inverse_key = HillCipher.matrix_mod_inverse(key, 26)
        block_size = len(key_matrix)
        
        numbers = HillCipher.text_to_numbers(text)
        
        result = []
        for i in range(0, len(numbers), block_size):
            block = np.array(numbers[i:i + block_size], dtype=int)
            decrypted_block = np.mod(np.dot(inverse_key, block), 26)
            result.extend(decrypted_block)
            
        if padding_count > 0:
            result = result[:-padding_count]
            
        return HillCipher.numbers_to_text(result)

    @staticmethod
    def encrypt_file(file_path: str, key_matrix: List[List[int]], output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text, padding_count = HillCipher.encrypt_hill(text, key_matrix)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            HillCipher.encrypt_file(file_path, key_matrix, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, key_matrix: List[List[int]], padding_count: int = 0, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = HillCipher.decrypt_hill(encrypted_text, key_matrix, padding_count)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")