class Binary:
    """
    Una clase que proporciona métodos estáticos para la conversión entre texto y representación binaria.
    Methods
    -------
    text_to_binary(text: str) -> str
        Convierte una cadena de texto a su representación binaria.
        Parámetros:
            text (str): El texto a convertir.
        Retorna:
            str: La representación binaria del texto, con cada carácter 
            separado por espacios y representado en 8 bits.
    binary_to_text(binary: str) -> str
        Convierte una representación binaria a texto.
        Parámetros:
            binary (str): La cadena binaria a convertir, con cada byte 
            separado por espacios.
        Retorna:
            str: El texto decodificado de la representación binaria.
    """
    @staticmethod
    def text_to_binary(text: str) -> str:
        return ' '.join(format(ord(c), '08b') for c in text)

    @staticmethod
    def binary_to_text(binary: str) -> str:
        binary_list = binary.split(' ')
        return ''.join(chr(int(b, 2)) for b in binary_list)
    
    @staticmethod
    def text_to_binary_file(text: str, file_path: str):
        """
        Convierte un texto a su representación binaria y lo guarda en un archivo.

        Args:
            text (str): El texto a convertir.
            file_path (str): Ruta del archivo donde se guardará la representación binaria.
        """
        binary_text = Binary.text_to_binary(text)
        with open(file_path, 'w') as file:
            file.write(binary_text)
        print(f"Binary representation saved to {file_path}")

    @staticmethod
    def binary_file_to_text(file_path: str) -> str:
        """
        Convierte un archivo con representación binaria a texto.

        Args:
            file_path (str): Ruta del archivo con la representación binaria.

        Returns:
            str: El texto decodificado.

        Raises:
            FileNotFoundError: Si el archivo no existe.
        """
        try:
            with open(file_path, 'r') as file:
                binary_text = file.read()
            return Binary.binary_to_text(binary_text)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return ""