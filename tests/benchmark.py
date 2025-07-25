import pytest
from locust import HttpUser, task, between

class Pre911User(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def test_combined_endpoint(self):
        self.client.get("/combined")
        
    @task(3)
    def test_cached_endpoint(self):
        self.client.get("/cached")

@pytest.mark.benchmark
def test_data_ingestion_benchmark(benchmark):
    from pre911.core.data_pipeline import DataPipeline
    
    def run_pipeline():
        pipeline = DataPipeline()
        return pipeline.run_pipeline()
        
    result = benchmark(run_pipeline)
    assert len(result) > 0
