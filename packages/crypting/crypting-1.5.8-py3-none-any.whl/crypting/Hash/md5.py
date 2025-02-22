import struct
import os

class MD5Hash:
    """
    Implementación del algoritmo de hash MD5.
    MD5 es un algoritmo de hash criptográfico ampliamente utilizado que produce un valor hash de 128 bits.
    Aunque ya no se considera seguro para aplicaciones criptográficas, todavía se utiliza para la verificación de integridad de datos.
    """

    # Constantes para el algoritmo MD5
    S = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    K = [
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f2, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    ]

    @staticmethod
    def _left_rotate(x, c):
        """Rotación circular a la izquierda."""
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

    @staticmethod
    def _pad_message(message):
        """
        Aplica el padding al mensaje según el estándar MD5.
        """
        original_length = len(message) * 8
        message += b'\x80'
        while (len(message) + 8) % 64 != 0:
            message += b'\x00'
        message += struct.pack('<Q', original_length)
        return message

    @classmethod
    def _process_chunk(cls, chunk, h0, h1, h2, h3):
        """
        Procesa un bloque de 512 bits (64 bytes) del mensaje.
        """
        assert len(chunk) == 64

        # Dividir el bloque en 16 palabras de 32 bits
        words = list(struct.unpack('<16I', chunk))

        a, b, c, d = h0, h1, h2, h3

        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            temp = d
            d = c
            c = b
            b = (b + cls._left_rotate((a + f + cls.K[i] + words[g]), cls.S[i])) & 0xFFFFFFFF
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF

        return h0, h1, h2, h3

    @classmethod
    def hash(cls, message: str) -> str:
        """
        Calcula el hash MD5 de un mensaje.
        
        Args:
            message: Mensaje a hashear.
            
        Returns:
            Hash MD5 en formato hexadecimal.
        """
        # Convertir el mensaje a bytes
        message = message.encode()

        # Aplicar padding al mensaje
        message = cls._pad_message(message)

        # Inicializar variables de estado
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476

        # Procesar el mensaje en bloques de 512 bits
        for i in range(0, len(message), 64):
            chunk = message[i:i + 64]
            h0, h1, h2, h3 = cls._process_chunk(chunk, h0, h1, h2, h3)

        # Producir el hash final
        digest = struct.pack('<4I', h0, h1, h2, h3)
        return ''.join(f'{byte:02x}' for byte in digest)

    @classmethod
    def hash_file(cls, file_path: str) -> str:
        """
        Calcula el hash MD5 de un archivo.
        
        Args:
            file_path: Ruta al archivo a hashear.
            
        Returns:
            Hash MD5 en formato hexadecimal.
        """
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
            return cls.hash(file_content.decode())
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return ""