from typing import List, Tuple
import struct
import os

class ChaCha20Cipher:
    """
    Implementación del cifrado de flujo ChaCha20.
    ChaCha20 es un cifrado de flujo diseñado por Daniel J. Bernstein. Es una variante
    del cifrado Salsa20 y utiliza una función de ronda basada en operaciones ADD-ROTATE-XOR (ARX).
    Características principales:
    - Clave de 256 bits (32 bytes)
    - Nonce de 96 bits (12 bytes) 
    - Contador de 32 bits
    - 20 rondas
    - Tamaño de bloque de 512 bits (64 bytes)
    El cifrado es considerado seguro y es ampliamente utilizado, siendo parte del protocolo
    TLS 1.3 y otros estándares de seguridad.
    Atributos:
        ROUNDS (int): Número de rondas del algoritmo (20 por defecto)
        SIGMA (bytes): Constante para claves de 256 bits
    Ejemplo de uso:
        >>> cipher = ChaCha20Cipher
        >>> key = cipher.generate_key()
        >>> texto = "Mensaje secreto"
        >>> encrypted, nonce = cipher.encrypt(texto, key)
        >>> decrypted = cipher.decrypt(encrypted, key, nonce)
        >>> print(decrypted)
        'Mensaje secreto'
    """

    ROUNDS = 20  # Número de rondas estándar
    SIGMA = b'expand 32-byte k'  # Constante para 256-bit keys

    @staticmethod
    def _rotate_left(value: int, shift: int) -> int:
        """Rotación circular a la izquierda de 32 bits."""
        return ((value << shift) & 0xFFFFFFFF) | (value >> (32 - shift))

    @staticmethod
    def _quarter_round(state: List[int], a: int, b: int, c: int, d: int) -> None:
        """
        Aplica una ronda de cuarto en ChaCha20.
        Modifica el estado in-place.
        
        Args:
            state: Estado actual
            a, b, c, d: Índices de las palabras a modificar
        """
        # Operaciones ADD-ROTATE-XOR (ARX)
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] ^= state[a]
        state[d] = ChaCha20Cipher._rotate_left(state[d], 16)

        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] ^= state[c]
        state[b] = ChaCha20Cipher._rotate_left(state[b], 12)

        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] ^= state[a]
        state[d] = ChaCha20Cipher._rotate_left(state[d], 8)

        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] ^= state[c]
        state[b] = ChaCha20Cipher._rotate_left(state[b], 7)

    @classmethod
    def _chacha20_block(cls, state: List[int]) -> List[int]:
        """
        Genera un bloque de keystream usando la función ChaCha20.
        
        Args:
            state: Estado inicial (16 palabras de 32 bits)
            
        Returns:
            Lista de 16 palabras transformadas
        """
        working_state = state.copy()
        
        # 20 rondas (10 rondas dobles)
        for _ in range(cls.ROUNDS // 2):
            # Ronda en columna
            cls._quarter_round(working_state, 0, 4, 8, 12)
            cls._quarter_round(working_state, 1, 5, 9, 13)
            cls._quarter_round(working_state, 2, 6, 10, 14)
            cls._quarter_round(working_state, 3, 7, 11, 15)
            
            # Ronda en diagonal
            cls._quarter_round(working_state, 0, 5, 10, 15)
            cls._quarter_round(working_state, 1, 6, 11, 12)
            cls._quarter_round(working_state, 2, 7, 8, 13)
            cls._quarter_round(working_state, 3, 4, 9, 14)

        # Suma con el estado inicial
        return [(working_state[i] + state[i]) & 0xFFFFFFFF for i in range(16)]

    @classmethod
    def _setup_state(cls, key: bytes, nonce: bytes, counter: int) -> List[int]:
        """
        Configura el estado inicial para ChaCha20.
        
        Args:
            key: Clave de 32 bytes
            nonce: Nonce de 12 bytes
            counter: Contador de 4 bytes
            
        Returns:
            Lista de 16 palabras de 32 bits que representa el estado inicial
        """
        assert len(key) == 32
        assert len(nonce) == 12
        
        # Convertir constantes a palabras de 32 bits
        constant = struct.unpack('<4I', cls.SIGMA)
        key_words = struct.unpack('<8I', key)
        nonce_words = struct.unpack('<3I', nonce)
        
        return [
            constant[0], constant[1], constant[2], constant[3],  # cccccccc
            key_words[0], key_words[1], key_words[2], key_words[3],  # kkkkkkkk
            key_words[4], key_words[5], key_words[6], key_words[7],  # kkkkkkkk
            counter & 0xFFFFFFFF,  # b
            nonce_words[0], nonce_words[1], nonce_words[2]  # nnnnnnnn
        ]

    @classmethod
    def encrypt(cls, text: str, key: bytes, nonce: bytes = None) -> Tuple[bytes, bytes]:
        """
        Cifra un texto usando ChaCha20.
        
        Args:
            text: Texto a cifrar
            key: Clave de 32 bytes
            nonce: Nonce de 12 bytes (opcional, se genera si no se proporciona)
            
        Returns:
            Tupla de (datos cifrados, nonce usado)
        """
        if nonce is None:
            nonce = os.urandom(12)
        
        # Convertir texto a bytes
        plaintext = text.encode()
        counter = 0
        result = bytearray()
        
        # Procesar el texto en bloques de 64 bytes
        for i in range(0, len(plaintext), 64):
            # Generar bloque de keystream
            state = cls._setup_state(key, nonce, counter)
            keystream_block = cls._chacha20_block(state)
            keystream = struct.pack('<16I', *keystream_block)
            
            # XOR con el texto plano
            chunk = plaintext[i:min(i + 64, len(plaintext))]
            for j in range(len(chunk)):
                result.append(chunk[j] ^ keystream[j])
            
            counter += 1
            
        return bytes(result), nonce

    @classmethod
    def decrypt(cls, encrypted_data: bytes, key: bytes, nonce: bytes) -> str:
        """
        Descifra datos cifrados con ChaCha20.
        
        Args:
            encrypted_data: Datos cifrados
            key: Clave de 32 bytes
            nonce: Nonce de 12 bytes usado en el cifrado
            
        Returns:
            Texto descifrado
        """
        # ChaCha20 es simétrico, el descifrado es igual al cifrado
        counter = 0
        result = bytearray()
        
        for i in range(0, len(encrypted_data), 64):
            state = cls._setup_state(key, nonce, counter)
            keystream_block = cls._chacha20_block(state)
            keystream = struct.pack('<16I', *keystream_block)
            
            chunk = encrypted_data[i:min(i + 64, len(encrypted_data))]
            for j in range(len(chunk)):
                result.append(chunk[j] ^ keystream[j])
            
            counter += 1
            
        return result.decode()

    @staticmethod
    def generate_key() -> bytes:
        """
        Genera una clave aleatoria para ChaCha20.
        
        Returns:
            Clave aleatoria de 32 bytes
        """
        return os.urandom(32)
    
    @classmethod
    def encrypt_file(cls, file_path: str, key: bytes, nonce: bytes = None, output_file_path: str = None):
        try:
            with open(file_path, 'rb') as file:
                plaintext = file.read()
            encrypted_data, nonce_used = cls.encrypt(plaintext.decode(), key, nonce)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            cls.encrypt_file(file_path, key, nonce, output_file_path)

    @classmethod
    def decrypt_file(cls, file_path: str, key: bytes, nonce: bytes, output_file_path: str = None):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_text = cls.decrypt(encrypted_data, key, nonce)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")