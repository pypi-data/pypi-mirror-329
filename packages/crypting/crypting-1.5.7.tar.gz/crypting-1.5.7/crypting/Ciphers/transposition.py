class TranspositionCipher:
    """
    Implementa el cifrado por transposición Rail Fence.
    El cifrado Rail Fence es un tipo de cifrado por transposición que escribe el texto en un patrón zigzag
    sobre un número específico de "rieles" y luego lee el texto cifrado rail por rail.
    Métodos:
        encrypt_transposition(text: str, rails: int) -> str:
            Cifra un texto usando el método Rail Fence.
            Args:
                text (str): El texto a cifrar.
                rails (int): El número de rieles a usar (debe ser >= 2).
            Returns:
                str: El texto cifrado.
        decrypt_transposition(text: str, rails: int) -> str:
            Descifra un texto que fue cifrado usando el método Rail Fence.
            Args:
                text (str): El texto cifrado a descifrar.
                rails (int): El número de rieles usado en el cifrado (debe ser >= 2).
            Returns:
                str: El texto descifrado.
    Ejemplo:
        >>> cipher = TranspositionCipher()
        >>> cipher.encrypt_transposition("HELLOWORLD", 3)
        'HOLELWRDLO'
        >>> cipher.decrypt_transposition("HOLELWRDLO", 3)
        'HELLOWORLD'
    """

    @staticmethod
    def encrypt_transposition(text: str, rails: int) -> str:
        if rails < 2:
            return text
            
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in text:
            fence[rail].append(char)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        return ''.join(''.join(rail) for rail in fence)

    @staticmethod
    def decrypt_transposition(text: str, rails: int) -> str:
        if rails < 2 or not text:
            return text
            
        positions = []
        rail = 0
        direction = 1
        
        for _ in range(len(text)):
            positions.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        rail_indices = {i: [] for i in range(rails)}
        for i, pos in enumerate(positions):
            rail_indices[pos].append(i)
        
        result = [''] * len(text)
        current_pos = 0
        
        for rail in range(rails):
            for pos in rail_indices[rail]:
                if current_pos < len(text):
                    result[pos] = text[current_pos]
                    current_pos += 1
        
        return ''.join(result)

    @staticmethod
    def encrypt_file(file_path: str, rails: int, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text = TranspositionCipher.encrypt_transposition(text, rails)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            TranspositionCipher.encrypt_file(file_path, rails, output_file_path)

    @staticmethod
    def decrypt_file(file_path: str, rails: int, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = TranspositionCipher.decrypt_transposition(encrypted_text, rails)
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
