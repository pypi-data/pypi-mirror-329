from typing import List, Tuple
import struct
import os

class RC5Cipher:
    """
    Implementación del algoritmo de cifrado RC5 (Rivest Cipher 5).
    Esta clase proporciona métodos para cifrar y descifrar datos usando el algoritmo RC5,
    específicamente en su variante RC5-32/12/b donde:
    - 32 es el tamaño de palabra en bits
    - 12 es el número de rondas
    - b es el tamaño de la clave en bytes (variable)
    El algoritmo RC5 fue diseñado por Ronald Rivest en 1994 y es un cifrado por bloques
    con un tamaño de bloque variable, número de rondas variable y tamaño de clave variable.
    Atributos:
        WORD_SIZE (int): Tamaño de palabra en bits (32)
        ROUNDS (int): Número de rondas de cifrado (12)
        P (int): Constante mágica P32 derivada de e
        Q (int): Constante mágica Q32 derivada de φ (phi)
    Ejemplo de uso:
        >>> cipher = RC5Cipher()
        >>> key = RC5Cipher.generate_key()
        >>> encrypted = RC5Cipher.encrypt_rc5("texto secreto", key)
        >>> decrypted = RC5Cipher.decrypt_rc5(encrypted, key)
        >>> print(decrypted)
        'texto secreto'
    """

    # Constantes para RC5-32/12/b
    WORD_SIZE = 32  # w (bits)
    ROUNDS = 12     # r
    P = 0xB7E15163  # P32 = Odd((e-2)*2^WORD_SIZE)
    Q = 0x9E3779B9  # Q32 = Odd((φ-1)*2^WORD_SIZE)

    @staticmethod
    def _rotate_left(value: int, shift: int, bits: int = 32) -> int:
        """Rotación circular a la izquierda."""
        shift %= bits
        return ((value << shift) | (value >> (bits - shift))) & ((1 << bits) - 1)

    @staticmethod
    def _rotate_right(value: int, shift: int, bits: int = 32) -> int:
        """Rotación circular a la derecha."""
        shift %= bits
        return ((value >> shift) | (value << (bits - shift))) & ((1 << bits) - 1)

    @classmethod
    def _expand_key(cls, key: bytes) -> List[int]:
        """
        Expande la clave en un array de subclaves.
        
        Args:
            key: Clave de entrada en bytes
            
        Returns:
            Lista de subclaves expandidas
        """
        # Convertir la clave a palabras
        key_words = []
        for i in range(0, len(key), 4):
            key_words.append(int.from_bytes(key[i:i+4].ljust(4, b'\0'), 'little'))

        # Inicializar array L
        L = key_words + [0] * (8 - len(key_words))

        # Inicializar array S
        t = 2 * (cls.ROUNDS + 1)
        S = [0] * t
        S[0] = cls.P

        # Llenar array S
        for i in range(1, t):
            S[i] = (S[i-1] + cls.Q) & 0xFFFFFFFF

        # Mezclar
        i = j = A = B = 0
        for k in range(3 * max(t, len(L))):
            A = S[i] = cls._rotate_left(S[i] + A + B, 3)
            B = L[j] = cls._rotate_left(L[j] + A + B, A + B)
            i = (i + 1) % t
            j = (j + 1) % len(L)

        return S

    @classmethod
    def encrypt_rc5(cls, text: str, key: bytes) -> bytes:
        """
        Cifra un texto usando RC5.
        
        Args:
            text: Texto a cifrar
            key: Clave de cifrado
            
        Returns:
            Datos cifrados en bytes
        """
        # Expandir la clave
        S = cls._expand_key(key)

        # Convertir texto a bytes y añadir padding si es necesario
        text_bytes = text.encode()
        padding_length = (8 - len(text_bytes) % 8) % 8
        text_bytes += bytes([padding_length] * padding_length)

        # Procesar bloques de 8 bytes (dos palabras de 32 bits)
        result = []
        for i in range(0, len(text_bytes), 8):
            block = text_bytes[i:i+8]
            A = int.from_bytes(block[0:4], 'little')
            B = int.from_bytes(block[4:8], 'little')

            A = (A + S[0]) & 0xFFFFFFFF
            B = (B + S[1]) & 0xFFFFFFFF

            for r in range(1, cls.ROUNDS + 1):
                A = (cls._rotate_left(A ^ B, B) + S[2*r]) & 0xFFFFFFFF
                B = (cls._rotate_left(B ^ A, A) + S[2*r + 1]) & 0xFFFFFFFF

            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))

        return bytes(result)

    @classmethod
    def decrypt_rc5(cls, encrypted_data: bytes, key: bytes) -> str:
        """
        Descifra datos cifrados con RC5.
        
        Args:
            encrypted_data: Datos cifrados
            key: Clave de cifrado
            
        Returns:
            Texto descifrado
        """
        # Expandir la clave
        S = cls._expand_key(key)

        # Procesar bloques cifrados
        result = bytearray()
        for i in range(0, len(encrypted_data), 8):
            block = encrypted_data[i:i+8]
            A = int.from_bytes(block[0:4], 'little')
            B = int.from_bytes(block[4:8], 'little')

            for r in range(cls.ROUNDS, 0, -1):
                B = cls._rotate_right(B - S[2*r + 1], A) ^ A
                A = cls._rotate_right(A - S[2*r], B) ^ B

            B = (B - S[1]) & 0xFFFFFFFF
            A = (A - S[0]) & 0xFFFFFFFF

            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))

        # Quitar padding
        padding_length = result[-1]
        if padding_length < 8:
            result = result[:-padding_length]

        return result.decode()

    @staticmethod
    def generate_key(size: int = 16) -> bytes:
        """
        Genera una clave aleatoria para RC5.
        
        Args:
            size: Tamaño de la clave en bytes (por defecto 16)
            
        Returns:
            Clave aleatoria en bytes
        """
        return os.urandom(size)

    @classmethod
    def encrypt_file(cls, file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_data = cls.encrypt_rc5(text, key)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            cls.encrypt_file(file_path, key, output_file_path)

    @classmethod
    def decrypt_file(cls, file_path: str, key: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_text = cls.decrypt_rc5(encrypted_data, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")