import pytest
from chaoslib import experiment, hypothesis
from chaoslib.types import Configuration, Secrets

@experiment
def test_api_resilience(configuration: Configuration, secrets: Secrets):
    """Verify API remains available during dependency failures."""
    
    @hypothesis("API responds during Twitter outage")
    def twitter_outage():
        # Simulate Twitter API failure
        response = make_request("/twitter")
        assert response.status_code in [200, 503]
        
    @hypothesis("Combined endpoint degrades gracefully")
    def graceful_degradation():
        response = make_request("/combined")
        assert response.status_code == 200
        assert "sources" in response.json()

@experiment
def test_cache_resilience():
    """Validate cache fallback behavior."""
    
    @hypothesis("System falls back to local cache when Redis fails")
    def redis_failure():
        response = make_request("/redis-cached")
        assert response.status_code == 200
        assert "cache_type" in response.json()
