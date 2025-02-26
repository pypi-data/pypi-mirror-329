from pymongo import MongoClient

from src.infra.config.logging_config import get_logger

LOGGER = get_logger()


class ReviewRepository:
    """
    A repository class to manage the storage of code review data in MongoDB.

    Attributes:
        client (MongoClient): A MongoClient instance to connect to MongoDB.
        db (str): The name of the MongoDB database.
        collection (str): The name of the MongoDB collection.
    """

    def __init__(self, mongodb_host: str, mongodb_port: int, db_name: str, collection_name: str) -> None:
        self.client = MongoClient(mongodb_host, mongodb_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_review(self, project_id: int, merge_request_id: int, review_data: dict) -> None:
        """
        Saves the review data to MongoDB.

        Args:
            project_id (int): The ID of the project.
            merge_request_id (int): The ID of the merge request.
            review_data (dict): The review data to save.
        """
        try:
            existing_review = self.collection.find_one({"project_id": project_id, "merge_request_id": merge_request_id})
            if existing_review:
                self.collection.update_one(
                    {"project_id": project_id, "merge_request_id": merge_request_id},
                    {"$push": {"review_data.diffs": review_data}}
                )
            else:
                new_review = {
                    "project_id": project_id,
                    "merge_request_id": merge_request_id,
                    "review_count": 1,
                    "review_data": {
                        "diffs": [review_data]
                    }
                }
                self.collection.insert_one(new_review)
            LOGGER.debug(f"<<< Review saved successfully for merge request {merge_request_id} in project {project_id}")
        except Exception as e:
            LOGGER.error(f"::: Error saving review for merge request {merge_request_id}: {str(e)} :::")

    def increment_review_count(self, project_id: int, merge_request_id: int) -> None:
        """
        Increments the review count for a given merge request.

        Args:
            project_id (int): The ID of the project.
            merge_request_id (int): The ID of the merge request.
        """
        try:
            self.collection.update_one(
                {"project_id": project_id, "merge_request_id": merge_request_id},
                {"$inc": {"review_count": 1}}
            )
            LOGGER.debug(f"Review count incremented for merge request {merge_request_id} in project {project_id}")
        except Exception as e:
            LOGGER.error(f"Error incrementing review count for merge request {merge_request_id}: {str(e)}")

    def get_review_count(self, project_id: int, merge_request_id: int) -> int:
        """
        Gets the current review count for a given merge request.

        Args:
            project_id (int): The ID of the project.
            merge_request_id (int): The ID of the merge request.

        Returns:
            int: The current review count.
        """
        review = self.collection.find_one({"project_id": project_id, "merge_request_id": merge_request_id})
        if review:
            return review.get("review_count", 0)
        return 0
