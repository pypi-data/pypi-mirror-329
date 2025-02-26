class Extract:

    @staticmethod
    def extract_review_content(response: str) -> str:
        """
        Extracts the content from the response starting from 'Review:'.

        Args:
            response (str): The response string.

        Returns:
            str: The extracted review content.
        """
        review_start = response.find("Review:")
        if review_start != -1:
            return response[review_start:].strip()
        return "Review content not found."
