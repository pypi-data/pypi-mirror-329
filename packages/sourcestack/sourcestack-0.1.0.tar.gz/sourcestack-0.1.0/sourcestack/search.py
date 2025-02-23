import os
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from sourcestack.client import Client
from sourcestack.exceptions import SearchError


class SourceStackSearchService:
    """Service for searching SourceStack Jobs"""

    SEARCH_PARAMS = {
        "name",
        "url",
        "parent",
        "uses_product",
        "uses_category",
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the search service

        Args:
            api_key: Optional API key (defaults to SOURCESTACK_API_KEY env var)
            base_url: Optional base URL (defaults to SOURCESTACK_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("SOURCESTACK_API_KEY")
        self.base_url = base_url or os.getenv("SOURCESTACK_BASE_URL")

        if not self.api_key:
            raise SearchError(
                "No API key provided and SOURCESTACK_API_KEY environment variable not set"
            )

        self.client = Client(api_key=self.api_key, base_url=self.base_url)

    def _validate_search_params(self, params: Dict[str, Any]) -> None:
        """Validate search parameters"""
        search_params_used = [param for param in self.SEARCH_PARAMS if param in params]
        if len(search_params_used) != 1:
            raise SearchError(
                f"Exactly one search parameter required from: {self.SEARCH_PARAMS}"
            )

    def _validate_filter_format(self, filters: List[Dict[str, Any]]) -> None:
        """Validate the format of search filters"""
        if not filters:
            raise SearchError("Filters list cannot be empty")

        required_keys = {"field", "operator", "value"}
        for filter_dict in filters:
            if not isinstance(filter_dict, dict):
                raise SearchError("Each filter must be a dictionary")
            if not all(key in filter_dict for key in required_keys):
                raise SearchError(
                    f"Filter must contain all required keys: {required_keys}"
                )

    def _process_url(self, url: str) -> str:
        """Process URL by removing common prefixes"""
        url = url.replace("https://", "").replace("http://", "")
        return url.replace("www.", "")

    def _format_results(
        self,
        results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Format the search results with statistics"""
        if not results:
            return {
                "status": "error",
                "message": "No results found",
                "timestamp": datetime.now().isoformat(),
                "count": 0,
            }

        # Collect statistics
        companies = Counter(
            str(result.get("company_name", "Unknown")) for result in results
        )
        technologies = Counter(
            tech for result in results for tech in result.get("tags_matched", [])
        )
        categories = Counter(
            category
            for result in results
            for category in result.get("tag_categories", [])
        )

        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "count": len(results),
            "statistics": {
                "companies": [
                    {"name": k, "count": v} for k, v in companies.most_common(5)
                ],
                "technologies": [
                    {"name": k, "count": v} for k, v in technologies.most_common(5)
                ],
                "categories": [
                    {"name": k, "count": v} for k, v in categories.most_common(5)
                ],
            },
            "entries": results,
        }

        return response

    def search_jobs(self, **kwargs) -> Dict[str, Any]:
        """Search for jobs using the SourceStack API

        Args:
            name (str, optional): Search by job name
            url (str, optional): Search by company URL
            parent (str, optional): Search by parent company
            uses_product (str, optional): Search by product usage
            uses_category (str, optional): Search by product category
            exact (bool, optional): Whether to do exact matching (default varies by endpoint)
            limit (int, optional): Maximum number of results to return

        Returns:
            Dict containing search results and metadata
        """
        try:
            self._validate_search_params(kwargs)

            # Process URL if provided
            if url := kwargs.get("url"):
                kwargs["url"] = self._process_url(url)

            # Determine which search method to use and execute
            if "name" in kwargs:
                exact = kwargs.pop("exact", False)
                results = self.client.jobs.by_name(
                    kwargs.pop("name"), exact=exact, **kwargs
                )
            elif "url" in kwargs:
                results = self.client.jobs.by_url(kwargs.pop("url"), **kwargs)
            elif "parent" in kwargs:
                results = self.client.jobs.by_parent(kwargs.pop("parent"), **kwargs)
            elif "uses_product" in kwargs:
                exact = kwargs.pop("exact", True)
                results = self.client.jobs.by_uses_product(
                    kwargs.pop("uses_product"), exact=exact, **kwargs
                )
            elif "uses_category" in kwargs:
                exact = kwargs.pop("exact", True)
                results = self.client.jobs.by_uses_category(
                    kwargs.pop("uses_category"), exact=exact, **kwargs
                )

            # Format results with statistics
            response = self._format_results(results["data"])

            return response

        except Exception as e:
            raise SearchError(f"Search failed: {str(e)}") from e

    def search_jobs_advanced(self, **kwargs) -> Dict[str, Any]:
        """Search for jobs using advanced filtering

        Args:
            filters (List[Dict]): List of filter conditions, each containing:
                - field (str): The field to filter on
                - operator (str): The operator to use. Supported operators vary by field type:
                    - Text: EQUALS, NOT_EQUALS, IN, NOT_IN, CONTAINS_ANY, NOT_CONTAINS_ANY, CONTAINS_ALL, NOT_CONTAINS_ALL
                    - Number: All operators except CONTAINS variants
                    - List: CONTAINS_ANY, NOT_CONTAINS_ANY, CONTAINS_ALL, NOT_CONTAINS_ALL
                    - Boolean: EQUALS, NOT_EQUALS
                    - Datetime: All operators except CONTAINS variants and IN/NOT_IN
                - value (str): The value to filter by
            limit (int, optional): Maximum number of results to return
            preview (str): Number of entries to preview

        Returns:
            Dict containing search results and metadata

        Raises:
            SearchError: If the search fails or filter validation fails
        """
        try:
            # Check if filters exist in kwargs
            filters = kwargs.get("filters", [])
            if not isinstance(filters, list):
                raise SearchError(
                    "Filters must be provided as a list of filter conditions"
                )

            if not filters:
                raise SearchError("At least one filter condition must be provided")

            # Validate each filter
            valid_operators = {
                # Basic comparison operators
                "EQUALS",
                "NOT_EQUALS",
                "GREATER_THAN",
                "LESS_THAN",
                # List operators
                "IN",
                "NOT_IN",
                # Content matching operators
                "CONTAINS_ANY",
                "NOT_CONTAINS_ANY",
                "CONTAINS_ALL",
                "NOT_CONTAINS_ALL",
            }

            for filter_condition in filters:
                # Validate required parameters for each filter
                required_params = {"field", "operator", "value"}
                if not all(param in filter_condition for param in required_params):
                    raise SearchError(
                        f"Each filter must contain all required parameters: {required_params}"
                    )

                # Validate operator for each filter
                if filter_condition["operator"] not in valid_operators:
                    raise SearchError(
                        f"Invalid operator. Must be one of: {valid_operators}"
                    )

            # Execute search via client with all filters
            search_params = {"filters": filters, "limit": kwargs.get("limit")}
            results = self.client.jobs.search_advanced(**search_params)

            # Format results with statistics
            response = self._format_results(results["data"])

            return response

        except Exception as e:
            raise SearchError(f"Advanced search failed: {str(e)}") from e
