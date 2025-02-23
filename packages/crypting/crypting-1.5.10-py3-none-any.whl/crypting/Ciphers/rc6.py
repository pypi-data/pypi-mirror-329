from typing import List, Tuple
import struct
import os

class RC6Cipher:
    """
    Implementación del algoritmo de cifrado RC6.
    RC6 es un cifrado por bloques derivado de RC5. Esta implementación usa:
    - Tamaño de palabra de 32 bits
    - 20 rondas
    - Tamaño de bloque variable
    Atributos:
        WORD_SIZE (int): Tamaño de palabra en bits (w=32)
        ROUNDS (int): Número de rondas (r=20) 
        P (int): Constante P32 = Odd((e-2)*2^WORD_SIZE)
        Q (int): Constante Q32 = Odd((φ-1)*2^WORD_SIZE)
        MASK (int): Máscara de 32 bits
    Métodos:
        encrypt_rc6(text: str, key: bytes) -> bytes:
            Cifra un texto usando RC6
        decrypt_rc6(encrypted_data: bytes, key: bytes) -> str:
            Descifra datos previamente cifrados con RC6
        generate_key(size: int = 16) -> bytes:
            Genera una clave aleatoria del tamaño especificado
        _expand_key(key: bytes) -> List[int]:
            Expande la clave en subclaves (método interno)
        _rotate_left(value: int, shift: int, bits: int = 32) -> int:
            Realiza rotación circular a la izquierda (método interno)
        _rotate_right(value: int, shift: int, bits: int = 32) -> int:
            Realiza rotación circular a la derecha (método interno)
    Referencias:
        RC6 Block Cipher - https://www.rfc-editor.org/rfc/rfc2268
    """

    # Constantes para RC6-32/20/b
    WORD_SIZE = 32  # w (bits)
    ROUNDS = 20     # r
    P = 0xB7E15163  # P32 = Odd((e-2)*2^WORD_SIZE)
    Q = 0x9E3779B9  # Q32 = Odd((φ-1)*2^WORD_SIZE)
    MASK = 0xFFFFFFFF  # Máscara para 32 bits

    @staticmethod
    def _rotate_left(value: int, shift: int, bits: int = 32) -> int:
        """Rotación circular a la izquierda."""
        shift %= bits
        value &= ((1 << bits) - 1)  # Asegurar que el valor está en el rango correcto
        return ((value << shift) | (value >> (bits - shift))) & ((1 << bits) - 1)

    @staticmethod
    def _rotate_right(value: int, shift: int, bits: int = 32) -> int:
        """Rotación circular a la derecha."""
        shift %= bits
        value &= ((1 << bits) - 1)  # Asegurar que el valor está en el rango correcto
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
        t = 2 * (cls.ROUNDS + 2)  # RC6 necesita 2r + 4 palabras
        S = [0] * t
        S[0] = cls.P

        # Llenar array S
        for i in range(1, t):
            S[i] = (S[i-1] + cls.Q) & cls.MASK

        # Mezclar
        i = j = A = B = 0
        v = 3 * max(len(L), t)
        for s in range(v):
            A = S[i] = cls._rotate_left((S[i] + A + B) & cls.MASK, 3)
            B = L[j] = cls._rotate_left((L[j] + A + B) & cls.MASK, (A + B) & 31)
            i = (i + 1) % t
            j = (j + 1) % len(L)

        return S

    @classmethod
    def encrypt_rc6(cls, text: str, key: bytes) -> bytes:
        """
        Cifra un texto usando RC6.
        
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
        padding_length = (16 - len(text_bytes) % 16) % 16
        text_bytes += bytes([padding_length] * padding_length)

        # Procesar bloques de 16 bytes (cuatro palabras de 32 bits)
        result = []
        for i in range(0, len(text_bytes), 16):
            block = text_bytes[i:i+16]
            A = int.from_bytes(block[0:4], 'little')
            B = int.from_bytes(block[4:8], 'little')
            C = int.from_bytes(block[8:12], 'little')
            D = int.from_bytes(block[12:16], 'little')

            # Pre-whitening
            B = (B + S[0]) & cls.MASK
            D = (D + S[1]) & cls.MASK

            for r in range(1, cls.ROUNDS + 1):
                t = cls._rotate_left((B * (2 * B + 1)) & cls.MASK, 5)
                u = cls._rotate_left((D * (2 * D + 1)) & cls.MASK, 5)
                A = (cls._rotate_left((A ^ t) & cls.MASK, u & 31) + S[2 * r]) & cls.MASK
                C = (cls._rotate_left((C ^ u) & cls.MASK, t & 31) + S[2 * r + 1]) & cls.MASK
                A, B, C, D = B, C, D, A

            # Post-whitening
            A = (A + S[2 * cls.ROUNDS + 2]) & cls.MASK
            C = (C + S[2 * cls.ROUNDS + 3]) & cls.MASK

            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))
            result.extend(C.to_bytes(4, 'little'))
            result.extend(D.to_bytes(4, 'little'))

        return bytes(result)

    @classmethod
    def decrypt_rc6(cls, encrypted_data: bytes, key: bytes) -> str:
        """
        Descifra datos cifrados con RC6.
        
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
        for i in range(0, len(encrypted_data), 16):
            block = encrypted_data[i:i+16]
            A = int.from_bytes(block[0:4], 'little')
            B = int.from_bytes(block[4:8], 'little')
            C = int.from_bytes(block[8:12], 'little')
            D = int.from_bytes(block[12:16], 'little')

            # Revertir post-whitening
            C = (C - S[2 * cls.ROUNDS + 3]) & cls.MASK
            A = (A - S[2 * cls.ROUNDS + 2]) & cls.MASK

            for r in range(cls.ROUNDS, 0, -1):
                A, B, C, D = D, A, B, C
                u = cls._rotate_left((D * (2 * D + 1)) & cls.MASK, 5)
                t = cls._rotate_left((B * (2 * B + 1)) & cls.MASK, 5)
                C = ((cls._rotate_right(C - S[2 * r + 1], t & 31)) ^ u) & cls.MASK
                A = ((cls._rotate_right(A - S[2 * r], u & 31)) ^ t) & cls.MASK

            # Revertir pre-whitening
            D = (D - S[1]) & cls.MASK
            B = (B - S[0]) & cls.MASK

            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))
            result.extend(C.to_bytes(4, 'little'))
            result.extend(D.to_bytes(4, 'little'))

        # Quitar padding
        padding_length = result[-1]
        if padding_length < 16:
            result = result[:-padding_length]

        return result.decode()

    @staticmethod
    def generate_key(size: int = 16) -> bytes:
        """
        Genera una clave aleatoria para RC6.
        
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
            encrypted_data = cls.encrypt_rc6(text, key)
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
            decrypted_text = cls.decrypt_rc6(encrypted_data, key)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")