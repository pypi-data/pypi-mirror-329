import os
from unittest.mock import Mock, patch

import pytest

from sourcestack.exceptions import SearchError
from sourcestack.search import SourceStackSearchService


@pytest.fixture
def search_service():
    api_key = os.getenv("SOURCESTACK_API_KEY")
    base_url = os.getenv("SOURCESTACK_BASE_URL")
    if not api_key:
        pytest.skip("SOURCESTACK_API_KEY environment variable not set")
    return SourceStackSearchService(api_key=api_key, base_url=base_url)


@pytest.fixture
def mock_search_service():
    with patch("sourcestack.search.Client") as mock_client:
        service = SourceStackSearchService(api_key="test_key", base_url="test_url")
        yield service, mock_client


@pytest.mark.integration
class TestJobSearchEndpoints:
    def test_jobs_search_by_name_contains(self, search_service):
        results = search_service.search_jobs(name="DevOps", exact=False, limit=2)
        assert results["status"] == "success"
        assert results["count"] > 0
        assert all("devops" in job["job_name"].lower() for job in results["entries"])

    def test_jobs_search_by_exact_name(self, search_service):
        results = search_service.search_jobs(
            name="Platform Engineer", exact=True, limit=2
        )
        assert results["status"] == "success"
        assert all(
            job["job_name"].lower() == "platform engineer" for job in results["entries"]
        )

    def test_jobs_search_by_parent_company(self, search_service):
        results = search_service.search_jobs(parent="Spotify", limit=2)
        assert results["status"] == "success"
        assert all(
            "spotify" in job["company_name"].lower() for job in results["entries"]
        )

    def test_jobs_search_by_url(self, search_service):
        results = search_service.search_jobs(url="canva.com", limit=2)
        assert results["status"] == "success"
        assert all(
            "canva.com" in job["company_url"].lower() for job in results["entries"]
        )

    def test_jobs_search_by_product_use(self, search_service):
        results = search_service.search_jobs(uses_product="Docker", exact=True, limit=2)
        assert results["status"] == "success"
        assert all(
            "docker" in [tag.lower() for tag in job["tags_matched"]]
            for job in results["entries"]
        )

    def test_jobs_search_by_category(self, search_service):
        results = search_service.search_jobs(
            uses_category="Container Orchestration", limit=2
        )
        assert results["status"] == "success"
        assert all(
            "container orchestration" in [cat.lower() for cat in job["tag_categories"]]
            for job in results["entries"]
        )


class TestSearchValidation:
    def test_exact_parameter_validation(self, mock_search_service):
        service, _ = mock_search_service

        service._validate_search_params({"name": "DevOps", "exact": True})
        service._validate_search_params({"uses_product": "Docker", "exact": True})

    def test_search_parameter_validation(self, mock_search_service):
        service, _ = mock_search_service

        with pytest.raises(SearchError):
            service._validate_search_params({})

        with pytest.raises(SearchError):
            service._validate_search_params({"name": "Engineer", "url": "company.com"})


class TestSearchResults:
    @pytest.mark.integration
    def test_search_results_limit(self, search_service):
        limit = 5
        results = search_service.search_jobs(name="developer", limit=limit)

        assert results["status"] == "success"
        assert len(results["entries"]) <= limit


@pytest.mark.integration
class TestAdvancedJobSearch:
    def test_search_jobs_advanced_single_filter(self, search_service):
        results = search_service.search_jobs_advanced(
            filters=[{"field": "country", "operator": "IN", "value": "United States"}],
            limit=2,
        )
        assert results["status"] == "success"
        assert results["count"] > 0
        assert all(job["country"] == "United States" for job in results["entries"])

    def test_search_jobs_advanced_with_limit(self, search_service):
        results = search_service.search_jobs_advanced(
            filters=[
                {"field": "department", "operator": "EQUALS", "value": "Engineering"}
            ],
            limit=5,
        )
        assert results["status"] == "success"
        assert len(results["entries"]) <= 5

    def test_search_jobs_advanced_date_filter(self, search_service):
        results = search_service.search_jobs_advanced(
            filters=[
                {
                    "field": "last_indexed",
                    "operator": "GREATER_THAN",
                    "value": "LAST_7D",
                }
            ],
            limit=2,
        )
        assert results["status"] == "success"
        assert results["count"] > 0

    def test_search_jobs_advanced_multiple_filters(self, search_service):
        results = search_service.search_jobs_advanced(
            filters=[
                {
                    "field": "job_name",
                    "operator": "CONTAINS_ANY",
                    "value": "Senior Engineer",
                },
                {"field": "country", "operator": "EQUALS", "value": "United States"},
            ],
            limit=5,
        )
        assert results["status"] == "success"
        assert results["count"] > 0
        assert all(
            job["country"] == "United States"
            and any(
                term.lower() in job["job_name"].lower()
                for term in ["senior", "engineer"]
            )
            for job in results["entries"]
        )


class TestAdvancedSearchValidation:
    def test_missing_required_parameters(self, mock_search_service):
        service, _ = mock_search_service
        with pytest.raises(
            SearchError, match="At least one filter condition must be provided"
        ):
            service.search_jobs_advanced(filters=[])

    def test_invalid_operator(self, mock_search_service):
        service, _ = mock_search_service
        with pytest.raises(SearchError, match="Invalid operator"):
            service.search_jobs_advanced(
                filters=[
                    {
                        "field": "country",
                        "operator": "INVALID_OP",
                        "value": "United States",
                    }
                ]
            )

    def test_valid_operator(self, mock_search_service):
        service, _ = mock_search_service
        with patch.object(service.client.jobs, "search_advanced") as mock_search:
            mock_search.return_value = {"data": []}
            service.search_jobs_advanced(
                filters=[
                    {"field": "country", "operator": "EQUALS", "value": "United States"}
                ]
            )
            mock_search.assert_called_once()


class TestAdvancedSearchResults:
    @pytest.mark.integration
    def test_statistics_present_in_response(self, search_service):
        results = search_service.search_jobs_advanced(
            filters=[
                {"field": "tags_matched", "operator": "CONTAINS_ANY", "value": "AWS"}
            ],
            limit=2,
        )
        assert "statistics" in results
        assert "companies" in results["statistics"]
        assert "technologies" in results["statistics"]
        assert "categories" in results["statistics"]

    @pytest.mark.integration
    def test_pagination_with_limit(self, search_service):
        limit = 5
        results = search_service.search_jobs_advanced(
            filters=[
                {"field": "tags_matched", "operator": "CONTAINS_ANY", "value": "Python"}
            ],
            limit=limit,
        )
        assert len(results["entries"]) <= limit
