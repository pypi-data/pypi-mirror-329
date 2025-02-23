from typing import List, Tuple
import struct
import os

class Salsa20Cipher:
    """
    Implementación del cifrado de flujo Salsa20.
    Salsa20 es un cifrado de flujo diseñado por Daniel J. Bernstein. Utiliza una clave de 256 bits (32 bytes)
    y un nonce de 64 bits (8 bytes) para generar un flujo de bytes pseudoaleatorio que se combina con el texto
    plano mediante XOR para producir el texto cifrado.
    Atributos:
        ROUNDS (int): Número de rondas del cifrado (20 por defecto)
        SIGMA (bytes): Constante de 16 bytes usada para claves de 256 bits
    Métodos:
        encrypt(text: str, key: bytes, nonce: bytes = None) -> Tuple[bytes, bytes]:
            Cifra un texto usando Salsa20
        decrypt(encrypted_data: bytes, key: bytes, nonce: bytes) -> str:
            Descifra datos previamente cifrados con Salsa20
        generate_key() -> bytes:
            Genera una clave aleatoria de 32 bytes
    Ejemplo:
        >>> cipher = Salsa20Cipher()
        >>> key = cipher.generate_key()
        >>> encrypted, nonce = cipher.encrypt("Texto secreto", key)
        >>> decrypted = cipher.decrypt(encrypted, key, nonce)
        >>> print(decrypted)
        'Texto secreto'
    """

    ROUNDS = 20 # Numero de rondas estandar
    SIGMA = b'expand 32-byte k' # Constante para 256-bit keys


    @staticmethod
    def _rotate_left(value: int, shift: int) -> int:
        """Rotacion circular a la izquierda de 32 bits"""
        return ((value << shift) & 0xFFFFFFFF) | (value >> (32 - shift))
    
    @staticmethod
    def _quarter_round(y0: int, y1: int, y2: int, y3: int) -> Tuple[int, int, int, int]:
        """
        Aplica una ronda de cuatro en Salsa20

        Args:
            y0, y1, y2, y3: Cuatro palabras de 32 bits
        
        Returns:
            Tupla con las cuatro palabras transformadas
        """

        z1 = y1 ^ Salsa20Cipher._rotate_left((y0 + y3) & 0xFFFFFFFF, 7)
        z2 = y2 ^ Salsa20Cipher._rotate_left((z1 + y0) & 0xFFFFFFFF, 9)
        z3 = y3 ^ Salsa20Cipher._rotate_left((z2 + z1) & 0xFFFFFFFF, 13)
        z0 = y0 ^ Salsa20Cipher._rotate_left((z3 + z2) & 0xFFFFFFFF, 18)
        return z0, z1, z2, z3

    @classmethod
    def _salsa20_block(cls, input_block: List[int]) -> List[int]:
        """
        Genera un bloque de keystream usando la funcion Salsa20

        Args:
            input_block: Lista de 16 palabras de 32 bits

        Returns:
            Lista de 16 palabras transformadas
        """
        x = input_block.copy()

        for _ in range(cls.ROUNDS // 2):
            # Rondas en columna
            x[4], x[8], x[12], x[0] = cls._quarter_round(x[0], x[4], x[8], x[12])
            x[9], x[13], x[1], x[5] = cls._quarter_round(x[5], x[9], x[13], x[1])
            x[14], x[2], x[6], x[10] = cls._quarter_round(x[10], x[14], x[2], x[6])
            x[3], x[7], x[11], x[15] = cls._quarter_round(x[15], x[3], x[7], x[11])

            # Rondas en diagonal
            x[1], x[6], x[11], x[12] = cls._quarter_round(x[0], x[5], x[10], x[15])
            x[2], x[7], x[8], x[13] = cls._quarter_round(x[5], x[10], x[15], x[4])
            x[3], x[4], x[9], x[14] = cls._quarter_round(x[10], x[15], x[4], x[9])
            x[0], x[5], x[10], x[15] = cls._quarter_round(x[15], x[4], x[9], x[14])
        
        # Suma con el estado inicial
        return [(x[i] + input_block[i]) & 0xFFFFFFFF for i in range(16)]
    
    @classmethod
    def _setup_state(cls, key: bytes, nonce: bytes, counter: int) -> List[int]:
        """
        Configura el estado inicial para Salsa20.
        
        Args:
            key: Clave de 32 bytes
            nonce: Nonce de 8 bytes
            counter: Contador de 8 bytes
            
        Returns:
            Lista de 16 palabras de 32 bits que representa el estado inicial
        """
        assert len(key) == 32
        assert len(nonce) == 8
        
        # Convertir constantes a palabras de 32 bits
        sigma = struct.unpack('<4I', cls.SIGMA)
        key_words = struct.unpack('<8I', key)
        nonce_words = struct.unpack('<2I', nonce)
        
        return [
            sigma[0],
            key_words[0], key_words[1], key_words[2], key_words[3],
            sigma[1],
            nonce_words[0], nonce_words[1],
            counter & 0xFFFFFFFF, (counter >> 32) & 0xFFFFFFFF,
            sigma[2],
            key_words[4], key_words[5], key_words[6], key_words[7],
            sigma[3]
        ]

    @classmethod
    def encrypt(cls, text: str, key: bytes, nonce: bytes = None) -> Tuple[bytes, bytes]:
        """
        Cifra un texto usando Salsa20.
        
        Args:
            text: Texto a cifrar
            key: Clave de 32 bytes
            nonce: Nonce de 8 bytes (opcional, se genera si no se proporciona)
            
        Returns:
            Tupla de (datos cifrados, nonce usado)
        """
        if nonce is None:
            nonce = os.urandom(8)
        
        # Convertir texto a bytes
        plaintext = text.encode()
        counter = 0
        result = bytearray()
        
        # Procesar el texto en bloques de 64 bytes
        for i in range(0, len(plaintext), 64):
            # Generar bloque de keystream
            state = cls._setup_state(key, nonce, counter)
            keystream_block = cls._salsa20_block(state)
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
        Descifra datos cifrados con Salsa20.
        
        Args:
            encrypted_data: Datos cifrados
            key: Clave de 32 bytes
            nonce: Nonce de 8 bytes usado en el cifrado
            
        Returns:
            Texto descifrado
        """
        # Salsa20 es simétrico, el descifrado es igual al cifrado
        counter = 0
        result = bytearray()
        
        for i in range(0, len(encrypted_data), 64):
            state = cls._setup_state(key, nonce, counter)
            keystream_block = cls._salsa20_block(state)
            keystream = struct.pack('<16I', *keystream_block)
            
            chunk = encrypted_data[i:min(i + 64, len(encrypted_data))]
            for j in range(len(chunk)):
                result.append(chunk[j] ^ keystream[j])
            
            counter += 1
            
        return result.decode()

    @staticmethod
    def generate_key() -> bytes:
        """
        Genera una clave aleatoria para Salsa20.
        
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
