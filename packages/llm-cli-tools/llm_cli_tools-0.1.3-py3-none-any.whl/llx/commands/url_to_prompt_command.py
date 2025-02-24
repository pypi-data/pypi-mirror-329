import click
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
from llx.crawler import Crawler
from abc import ABC

class UrlToPromptCommand(ABC):
    """Handle URL crawling and content extraction"""
    
    def __init__(self):
        self.content_extractor = ContentExtractor()

    def execute(self, url: str, prompt: Optional[str], extract_text: bool,
                domain: Optional[str], max_depth: int, max_urls: int):
        crawler = Crawler(url, domain, max_depth, max_urls)
        urls = crawler.crawl()
        content = self.content_extractor.extract_content(urls, extract_text)
        formatted_output = self._format_output(content, prompt, extract_text)
        click.echo(formatted_output)

    def _format_output(self, content: List[Dict], prompt: Optional[str], extract_text: bool) -> str:
        if extract_text:
            full_text = "<instruction>\n"
            if prompt:
                full_text += f"  {prompt}\n"
            full_text += "</instruction>\n<urls>\n"
            for item in content:
                full_text += f"  <url>\n"
                full_text += f"    <link>{item['link']}</link>\n"
                full_text += f"    <title>{item['title']}</title>\n"
                full_text += f"    <content>{item['content']}</content>\n"
                full_text += f"  </url>\n"
            full_text += "</urls>"
        else:
            full_text = "\n\n".join(content)
            if prompt:
                full_text = f"{prompt}\n\n{full_text}"
        return full_text

class ContentExtractor:
    """Handle content extraction from URLs"""
    
    def extract_content(self, urls: List[str], extract_text: bool) -> List[Dict]:
        content = []
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                if extract_text:
                    content.append(self._extract_text_content(response.text, url))
                else:
                    content.append(response.text)
        return content

    def _extract_text_content(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        text = ' '.join(soup.stripped_strings)
        return {
            'link': url,
            'title': title,
            'content': text
        }
