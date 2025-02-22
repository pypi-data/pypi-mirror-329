"""
Este es el modulo que incluye la clase de reproductor de musica
"""

class Player:
    """
    Esta clase crea un reproductor de musica
    """

    def play(self, song):
        """
        Esta funcion reproduce la cancion que recibió como parametro

        Parameters:
        song (str): String con el Path de la cancion

        Returns:
            int: devuelve 1 si reproduce con exito, en caso contrario devuelve 0
        """
        print(f"Reproduciendo {song}")
    
    def stop(self):
        """
        Esta funcion detiene la reproduccion de la cancion
        """
        print("Stopping...")
