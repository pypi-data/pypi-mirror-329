import asyncio
import logging
from alive_progress import alive_bar
from urllib.parse import urlparse, urljoin
from crawl4ai import AsyncWebCrawler
import os
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def crawl_and_save(base_url, max_depth=2, concurrency=5):
    domain = urlparse(base_url).netloc
    visited = set()
    queue = [(base_url, 0)]
    total_urls = 0
    crawling_tasks = []

    async with AsyncWebCrawler() as crawler:
        with alive_bar(title="Crawling", enrich_print=False) as bar:
            while queue or crawling_tasks:
                while queue and len(crawling_tasks) < concurrency:
                    url, depth = queue.pop(0)
                    if url in visited or depth > max_depth:
                        continue
                    visited.add(url)
                    total_urls += 1
                    logging.info(f"Crawling: {url} (Depth: {depth})")
                    crawling_tasks.append(asyncio.create_task(crawl_url(crawler, url, depth, domain, visited, queue)))

                if crawling_tasks:
                    done, pending = await asyncio.wait(crawling_tasks, return_when=asyncio.FIRST_COMPLETED)
                    crawling_tasks = list(pending)
                    for task in done:
                        await task
                        bar()

async def crawl_url(crawler, url, depth, domain, visited, queue):
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    result = await crawler.arun(url)
    
    # Check if markdown content exists before saving
    if result and result.markdown:
        save_markdown(url, result.markdown)
    else:
        print(f"No markdown content generated for {url}")

    for link in result.links.get('internal', []):
        next_url = urljoin(url, link['href'])
        if urlparse(next_url).netloc == domain:
            queue.append((next_url, depth + 1))

def save_markdown(url, content):
    domain = urlparse(url).netloc
    path = urlparse(url).path.strip('/')
    if not path:
        path = 'index'
    
    # Create directory for the domain
    domain_dir = os.path.join('docs', domain)
    os.makedirs(domain_dir, exist_ok=True)

    full_path = os.path.join(domain_dir, f'{path}.md') if path != 'index' else os.path.join(domain_dir, 'index.md')
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)
    logging.info(f"Saved: {full_path}")

async def main(url: str):
    await crawl_and_save(url)

def app():
    parser = argparse.ArgumentParser(description="Crawl a website and save the content as markdown files.")
    parser.add_argument("url", help="The URL to crawl.")
    args = parser.parse_args()
    asyncio.run(main(args.url))
    

if __name__ == "__main__":
    app()