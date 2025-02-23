from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import Dict, Optional, List
import os
import requests

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not FIRECRAWL_API_KEY:
    raise ValueError("FIRECRAWL_API_KEY is not set")

class FirecrawlClient:
    def __init__(self):
        self.app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    def scrape(self, url: str):
        result = self.app.scrape_url(url, params={"formats": ["markdown", "html"]})
        if not result or (err:=result.get("error")):
            raise Exception(f"Failed to scrape {url}: {err}")
        return {
            "markdown": result["markdown"],
            "html": result["html"],
            "metadata": result["metadata"],
        }
    
    def scrape_batch(self, urls: List[str]):
        """Scrape multiple URLs synchronously and return aggregated results.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of dictionaries containing either successful results (markdown, html, metadata)
            or error information for failed scrapes
        """
        aggregated_data = []
        next_url = None
        
        # Initial request
        initial_response = self.app.batch_scrape_urls(urls, params={"formats": ["markdown", "html"]})

        if not initial_response or (err:=initial_response.get("error")):
            raise Exception(f"Failed to scrape batch: {err}")

        aggregated_data.extend(initial_response.get("data", []))
        next_url = initial_response.get("next")
        
        # Follow pagination
        while next_url:
            headers = {
                "x-api-key": FIRECRAWL_API_KEY,
                "Content-Type": "application/json"
            }
            response = requests.get(next_url, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            response_data = response.json()
            aggregated_data.extend(response_data.get("data", []))
            next_url = response_data.get("next")
        
        # Process all collected data
        results = []
        for result in aggregated_data:
            data = {
                "markdown": result.get("markdown"),
                "html": result.get("html"),
                "metadata": result.get("metadata"),
            }
            results.append(data)
        return results
    
    def async_scrape_batch(self, urls: List[str]) -> Dict:
        """Start an asynchronous batch scrape job.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            Dictionary containing job ID and status URL for checking progress
        """
        response = self.app.async_batch_scrape_urls(urls, params={"formats": ["markdown", "html"]})
        if not response or (err:=response.get("error")):
            raise Exception(f"Failed to start async batch scrape: {err}")
        return {
            "job_id": response["id"],
            "status_url": response["url"]
        }
    
    def check_batch_status(self, job_id: str) -> Dict:
        """Check the status of an async batch scrape job.
        
        Args:
            job_id: The ID of the batch scrape job
            
        Returns:
            Dictionary containing job status and results if completed
        """
        response = self.app.check_batch_scrape_status(job_id)
        if not response or (err:=response.get("error")):
            raise Exception(f"Failed to check batch status: {err}")
            
        # If job is completed, process the results same way as sync method
        if response.get("status") == "completed":
            results = []
            for result in response.get("data", []):
                data = {
                    "markdown": result.get("markdown"),
                    "html": result.get("html"),
                    "metadata": result.get("metadata"),
                }
                results.append(data)
            return {
                "status": "completed",
                "total": response.get("total"),
                "completed": response.get("completed"),
                "credits_used": response.get("creditsUsed"),
                "expires_at": response.get("expiresAt"),
                "results": results
            }
        
        # If job is still running, return status info
        return {
            "status": response.get("status", "unknown"),
            "total": response.get("total"),
            "completed": response.get("completed"),
            "credits_used": response.get("creditsUsed"),
            "expires_at": response.get("expiresAt"),
        }
    
    def crawl(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Crawl a website and all its subpages synchronously.
        
        Args:
            url: The URL to crawl
            params: Optional parameters for the crawl:
                - limit: Maximum number of pages to crawl
                - scrapeOptions: Options for scraping (formats, etc)
                - allowBackwardLinks: Whether to allow crawling parent/sibling pages
                
        Returns:
            Dictionary containing crawl results with markdown/html content and metadata
        """
        if params is None:
            params = {
                "limit": 100,
                "scrapeOptions": {"formats": ["markdown", "html"]}
            }
            
        # Start crawl
        crawl_status = self.app.crawl_url(url, params=params, poll_interval=30)
        if not crawl_status or (err:=crawl_status.get("error")):
            raise Exception(f"Failed to crawl {url}: {err}")
            
        return crawl_status
    
    def async_crawl(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Start an asynchronous crawl job.
        
        Args:
            url: The URL to crawl
            params: Optional parameters for the crawl
            
        Returns:
            Dictionary containing job ID and status URL
        """
        if params is None:
            params = {
                "limit": 100,
                "scrapeOptions": {"formats": ["markdown", "html"]}
            }
            
        response = self.app.async_crawl_url(url, params=params)
        if not response or (err:=response.get("error")):
            raise Exception(f"Failed to start crawl: {err}")
            
        return {
            "job_id": response["id"],
            "status_url": response["url"]
        }
    
    def check_crawl_status(self, job_id: str) -> Dict:
        """Check the status of an async crawl job.
        
        Args:
            job_id: The ID of the crawl job
            
        Returns:
            Dictionary containing job status and results if completed
        """
        response = self.app.check_crawl_status(job_id)
        if not response or (err:=response.get("error")):
            raise Exception(f"Failed to check crawl status: {err}")
            
        # Process results if completed
        if response.get("status") == "completed":
            return {
                "status": "completed",
                "total": response.get("total"),
                "completed": response.get("completed"),
                "credits_used": response.get("creditsUsed"),
                "expires_at": response.get("expiresAt"),
                "results": response.get("data", [])
            }
            
        # Return status info if still running
        return {
            "status": response.get("status", "unknown"),
            "total": response.get("total"),
            "completed": response.get("completed"),
            "credits_used": response.get("creditsUsed"),
            "expires_at": response.get("expiresAt"),
        }
    
    def crawl_with_websocket(self, url: str, params: Optional[Dict] = None, 
                           on_document=None, on_error=None, on_done=None):
        """Crawl a website with real-time updates via WebSocket.
        
        Args:
            url: The URL to crawl
            params: Optional parameters for the crawl
            on_document: Callback for each document scraped
            on_error: Callback for errors
            on_done: Callback when crawl is complete
        """
        if params is None:
            params = {
                "limit": 100,
                "scrapeOptions": {"formats": ["markdown", "html"]}
            }
            
        # Create watcher
        watcher = self.app.crawl_url_and_watch(url, params)
        
        # Add event listeners
        if on_document:
            watcher.add_event_listener("document", on_document)
        if on_error:
            watcher.add_event_listener("error", on_error)
        if on_done:
            watcher.add_event_listener("done", on_done)
            
        return watcher

    def extract(self):
        pass

    def map(self):
        pass