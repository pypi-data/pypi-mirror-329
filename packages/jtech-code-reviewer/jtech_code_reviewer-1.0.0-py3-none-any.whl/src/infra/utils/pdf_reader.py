from PyPDF2 import PdfReader


class ReadPDF:
    """
    ReadPDF is a class that reads a PDF file and extracts its text content.

    Args:
        path (str): The path to the PDF file to read.
    """

    def __init__(self, path):
        self.path = path

    def read(self):
        """
        Reads the PDF file and extracts its text content.

        Returns:
            str: The text content of the PDF file.
        """
        content = []
        with open(self.path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                content.append(page.extract_text())
        return "\n".join(content)

    def extract_text(self):
        """
        Reads the PDF file and extracts its text content.

        Returns:
            str: The text content of the PDF file.
        """
        return self.read()
