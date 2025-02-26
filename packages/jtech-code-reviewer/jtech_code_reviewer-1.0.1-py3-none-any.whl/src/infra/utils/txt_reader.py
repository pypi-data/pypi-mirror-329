class ReadText:
    """
    ReadText é uma classe que lê um arquivo de texto e extrai seu conteúdo.

    Args:
        path (str): O caminho para o arquivo de texto a ser lido.
    """

    def __init__(self, path):
        self.path = path

    def read(self):
        """
        Lê o arquivo de texto e extrai seu conteúdo.

        Returns:
            str: O conteúdo do arquivo de texto.
        """
        with open(self.path, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    def extract_text(self):
        """
        Extrai o conteúdo do arquivo de texto.

        Returns:
            str: O conteúdo do arquivo de texto.
        """
        return self.read()
