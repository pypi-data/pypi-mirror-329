import numpy as np
from typing import List, Tuple, Dict

class EnigmaMachine:
    """
    Implementación de la máquina Enigma, un dispositivo de cifrado histórico usado durante la Segunda Guerra Mundial.
    Esta clase simula el funcionamiento de una máquina Enigma de 3 rotores con un reflector. La máquina Enigma
    es un sistema de cifrado polialfabético que utiliza rotores mecánicos para codificar mensajes.
    Atributos:
        rotors (List[Dict[int, int]]): Lista de diccionarios que representan el cableado de cada rotor.
        rotor_positions (List[int]): Lista con las posiciones actuales de los rotores.
        notch_positions (List[str]): Lista con las posiciones de muesca de cada rotor.
        reflector (Dict[str, str]): Diccionario que representa el cableado del reflector.
        ring_settings (List[int]): Lista con la configuración de los anillos de cada rotor.
        current_positions (List[int]): Lista con las posiciones actuales de cada rotor.
    Ejemplo:
        >>> rotor_configs = [
        ...     {'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},  # Rotor I
        ...     {'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},  # Rotor II
        ...     {'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'}   # Rotor III
        ... ]
        >>> reflector = {'A': 'Y', 'B': 'R', ...}  # Reflector B
        >>> enigma = EnigmaMachine(rotor_configs, reflector, [1, 1, 1], ['A', 'A', 'A'])
        >>> encrypted = enigma.encrypt("HELLO")
    Referencias:
        - https://en.wikipedia.org/wiki/Enigma_machine
    """
    
    def __init__(self, rotor_configs: List[Dict[str, str]], reflector: Dict[str, str], ring_settings: List[int], initial_positions: List[str]):
        """
        Inicializa la máquina Enigma.
        
        Args:
            rotor_configs: Lista de diccionarios con la configuración de cada rotor
            reflector: Diccionario con la configuración del reflector
            ring_settings: Configuración de los anillos de cada rotor (1-26)
            initial_positions: Posiciones iniciales de los rotores (A-Z)
        """
        self.rotors = []
        self.rotor_positions = []
        self.notch_positions = []
        
        # Configuración de los rotores
        for config in rotor_configs:
            self.rotors.append(self._create_rotor_mapping(config))
            self.notch_positions.append(config.get('notch', 'Q'))
        
        self.reflector = reflector
        self.ring_settings = ring_settings
        self.current_positions = [ord(pos) - ord('A') for pos in initial_positions]
        
    @staticmethod
    def _create_rotor_mapping(config: Dict[str, str]) -> Dict[int, int]:
        """Crea el mapeo de un rotor a partir de su configuración."""
        mapping = {}
        wiring = config['wiring']
        for i, char in enumerate(wiring):
            mapping[i] = ord(char) - ord('A')
        return mapping
    
    def _rotate_rotors(self):
        """Rota los rotores según las reglas de Enigma."""
        # Rotación del rotor derecho en cada pulsación
        self.current_positions[2] = (self.current_positions[2] + 1) % 26
        
        # Comprueba si el rotor medio debe rotar
        if chr(self.current_positions[2] + ord('A')) == self.notch_positions[2]:
            self.current_positions[1] = (self.current_positions[1] + 1) % 26
            
            # Doble paso: si el rotor medio está en su muesca
            if chr(self.current_positions[1] + ord('A')) == self.notch_positions[1]:
                self.current_positions[0] = (self.current_positions[0] + 1) % 26
    
    def _pass_through_rotor(self, char_idx: int, rotor: Dict[int, int], position: int, ring_setting: int, reverse: bool = False) -> int:
        """Pasa un carácter a través de un rotor."""
        shifted = (char_idx + position - ring_setting + 26) % 26
        
        if not reverse:
            out = rotor[shifted]
        else:
            out = list(rotor.keys())[list(rotor.values()).index(shifted)]
            
        return (out - position + ring_setting + 26) % 26
    
    def encrypt_char(self, char: str) -> str:
        """Encripta un solo carácter usando la máquina Enigma."""
        if not char.isalpha():
            return char
            
        # Convertir a mayúsculas y obtener índice
        char = char.upper()
        char_idx = ord(char) - ord('A')
        
        # Rotar rotores
        self._rotate_rotors()
        
        # Paso a través de los rotores (de derecha a izquierda)
        for i in range(2, -1, -1):
            char_idx = self._pass_through_rotor(
                char_idx,
                self.rotors[i],
                self.current_positions[i],
                self.ring_settings[i]
            )
        
        # Paso a través del reflector
        char_idx = ord(self.reflector[chr(char_idx + ord('A'))]) - ord('A')
        
        # Paso a través de los rotores en sentido inverso (de izquierda a derecha)
        for i in range(3):
            char_idx = self._pass_through_rotor(
                char_idx,
                self.rotors[i],
                self.current_positions[i],
                self.ring_settings[i],
                reverse=True
            )
        
        return chr(char_idx + ord('A'))
    
    def encrypt(self, text: str) -> str:
        """Encripta un texto completo usando la máquina Enigma."""
        return ''.join(self.encrypt_char(c) for c in text)

    def encrypt_file(self, file_path: str, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            encrypted_text = self.encrypt(text)
            output_file_path = output_file_path or file_path + ".enc"
            with open(output_file_path, 'w') as file:
                file.write(encrypted_text)
            print(f"File encrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found. Creating a new file.")
            with open(file_path, 'w') as file:
                file.write("")
            self.encrypt_file(file_path, output_file_path)

    def decrypt_file(self, file_path: str, output_file_path: str = None):
        try:
            with open(file_path, 'r') as file:
                encrypted_text = file.read()
            decrypted_text = self.encrypt(encrypted_text)  # Enigma es simétrica
            output_file_path = output_file_path or file_path.replace(".enc", ".dec")
            with open(output_file_path, 'w') as file:
                file.write(decrypted_text)
            print(f"File decrypted and saved to {output_file_path}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")


# Configuraciones históricas de ejemplo
ROTOR_I = {
    'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    'notch': 'Q'
}   
ROTOR_II = {
    'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    'notch': 'E'
}
ROTOR_III = {
    'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    'notch': 'V'
}
REFLECTOR_B = {
    'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L',
    'H': 'D', 'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K',
    'O': 'M', 'P': 'I', 'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C',
    'V': 'W', 'W': 'V', 'X': 'J', 'Y': 'A', 'Z': 'T'
}