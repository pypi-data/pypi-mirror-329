from typing import Optional


class SearchError(Exception):
    """Base exception for search service errors"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        """Initialize search error
        Args:
            message: Error message
            status_code: Optional HTTP status code
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of the error"""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message
