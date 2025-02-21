import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from urllib.parse import urlparse
import os
import shutil
from crawk.crawk import crawl_and_save, crawl_url, save_markdown, app, main

# Fixtures
@pytest.fixture
def mock_crawler():
    class MockResult:
        def __init__(self, markdown=None, links=None):
            self.markdown = markdown
            self.links = links or {'internal': []}

    class MockCrawler:
        async def arun(self, url):
            return MockResult(
                markdown="# Test Content\nThis is test content.",
                links={'internal': [{'href': '/page1'}, {'href': '/page2'}]}
            )
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    return MockCrawler()

@pytest.fixture
def test_url():
    return "https://example.com"

@pytest.fixture
def cleanup_docs():
    # Setup
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs')
    
    yield
    
    # Teardown
    if os.path.exists('docs'):
        shutil.rmtree('docs')

# Tests for save_markdown
def test_save_markdown(cleanup_docs):
    url = "https://example.com/test/page"
    content = "# Test Content\nThis is a test."
    
    save_markdown(url, content)
    
    expected_path = os.path.join('docs', 'example.com', 'test/page.md')
    assert os.path.exists(expected_path)
    
    with open(expected_path, 'r') as f:
        saved_content = f.read()
    assert saved_content == content

def test_save_markdown_index(cleanup_docs):
    url = "https://example.com"
    content = "# Index Content"
    
    save_markdown(url, content)
    
    expected_path = os.path.join('docs', 'example.com', 'index.md')
    assert os.path.exists(expected_path)
    
    with open(expected_path, 'r') as f:
        saved_content = f.read()
    assert saved_content == content

# Tests for crawl_url
@pytest.mark.asyncio
async def test_crawl_url(mock_crawler):
    url = "https://example.com"
    depth = 0
    domain = urlparse(url).netloc
    visited = set()
    queue = []
    
    with patch('crawk.crawk.save_markdown') as mock_save:
        await crawl_url(mock_crawler, url, depth, domain, visited, queue)
        
        # Verify save_markdown was called
        mock_save.assert_called_once()
        
        # Verify queue was updated with new URLs
        assert len(queue) == 2
        assert queue[0] == ('https://example.com/page1', 1)
        assert queue[1] == ('https://example.com/page2', 1)

@pytest.mark.asyncio
async def test_crawl_url_with_relative_url(mock_crawler):
    url = "example.com"  # No protocol
    depth = 0
    domain = "example.com"
    visited = set()
    queue = []
    
    with patch('crawk.crawk.save_markdown') as mock_save:
        await crawl_url(mock_crawler, url, depth, domain, visited, queue)
        
        # Verify save_markdown was called with proper URL
        call_args = mock_save.call_args[0]
        assert call_args[0].startswith('https://')

# Tests for crawl_and_save
@pytest.mark.asyncio
async def test_crawl_and_save(mock_crawler):
    url = "https://example.com"
    
    with patch('crawk.crawk.AsyncWebCrawler', return_value=mock_crawler), \
         patch('crawk.crawk.save_markdown') as mock_save:
        await crawl_and_save(url, max_depth=1, concurrency=1)
        
        # Verify save_markdown was called at least once
        assert mock_save.called

# Tests for main and app
@pytest.mark.asyncio
async def test_main():
    url = "https://example.com"
    
    with patch('crawk.crawk.crawl_and_save') as mock_crawl:
        await main(url)
        mock_crawl.assert_called_once_with(url)

def test_app():
    test_args = ['script', 'https://example.com']
    
    with patch('sys.argv', test_args), \
         patch('asyncio.run') as mock_run:
        app()
        mock_run.assert_called_once()

# Error handling tests
@pytest.mark.asyncio
async def test_crawl_url_no_markdown(mock_crawler):
    class MockCrawlerNoMarkdown:
        async def arun(self, url):
            return Mock(markdown=None, links={'internal': []})
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    url = "https://example.com"
    depth = 0
    domain = urlparse(url).netloc
    visited = set()
    queue = []
    
    with patch('crawk.crawk.save_markdown') as mock_save:
        await crawl_url(MockCrawlerNoMarkdown(), url, depth, domain, visited, queue)
        
        # Verify save_markdown was not called when no markdown content
        mock_save.assert_not_called()

@pytest.mark.asyncio
async def test_crawl_and_save_max_depth(mock_crawler):
    url = "https://example.com"
    max_depth = 0  # Should only crawl the initial URL
    
    with patch('crawk.crawk.AsyncWebCrawler', return_value=mock_crawler), \
         patch('crawk.crawk.save_markdown') as mock_save:
        await crawl_and_save(url, max_depth=max_depth, concurrency=1)
        
        # Should only save one page due to max_depth=0
        assert mock_save.call_count == 1
