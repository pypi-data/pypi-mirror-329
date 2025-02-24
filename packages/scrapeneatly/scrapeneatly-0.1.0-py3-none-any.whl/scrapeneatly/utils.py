from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
import re
from typing import List, Dict, Any
from .config import Config
import logging

logger = logging.getLogger(__name__)

class ContentCleaner:
    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, 'lxml')
        self.base_url = base_url

    def process_exclude_tags(self, exclude_tags: List[str]):
        for tag in exclude_tags:
            if tag.startswith("*") and tag.endswith("*"):
                pattern = re.compile(tag[1:-1], re.I)
                elements = self.soup.find_all(
                    lambda elem: elem.name and (
                        pattern.search(elem.name) or
                        any(pattern.search(f'{attr}="{value}"') 
                            for attr, value in elem.attrs.items())
                    )
                )
                for element in elements:
                    element.decompose()
            else:
                for element in self.soup.select(tag):
                    element.decompose()

    def process_include_tags(self, include_tags: List[str]):
        new_soup = BeautifulSoup("<div></div>", 'lxml')
        new_div = new_soup.div
        
        for tag in include_tags:
            for element in self.soup.select(tag):
                new_div.append(element.copy())
        
        self.soup = new_soup

    def process_srcsets(self):
        """
        Process srcset attributes in img tags to handle responsive images.
        Supports various descriptor formats including:
        - Width descriptors (e.g., "100w")
        - Pixel density descriptors (e.g., "2x")
        - Sizes without descriptors
        """
        for img in self.soup.find_all('img', srcset=True):
            try:
                srcset = img['srcset']
                candidates = []
                
                # Split the srcset into individual source-descriptor pairs
                for part in [p.strip() for p in srcset.split(',')]:
                    if not part:
                        continue
                    
                    # Split into URL and descriptor (if any)
                    parts = part.split()
                    url = parts[0] if parts else ''
                    
                    if not url:
                        continue
                    
                    # Handle descriptor if present
                    descriptor = parts[1] if len(parts) > 1 else ''
                    numeric_value = None
                    
                    if descriptor:
                        # Try to extract numeric value from descriptor
                        try:
                            numeric_value = float(''.join(c for c in descriptor if c.isdigit() or c == '.'))
                        except ValueError:
                            pass
                    
                    candidates.append({
                        'url': url,
                        'descriptor': descriptor,
                        'numeric_value': numeric_value or 1  # Default to 1 if no numeric value
                    })
                
                if candidates:
                    # Sort candidates by numeric value (if available) in descending order
                    candidates.sort(key=lambda x: x['numeric_value'], reverse=True)
                    
                    # Store original srcset
                    img['data-original-srcset'] = srcset
                    
                    # Use the highest resolution/largest size as src
                    img['src'] = candidates[0]['url']
                    
                    # Store processed srcset data for potential future use
                    img['data-processed-srcset'] = ','.join(
                        f"{c['url']} {c['descriptor']}" if c['descriptor'] else c['url']
                        for c in candidates
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to process srcset: {str(e)}")
                # Keep original srcset in case of processing error
                if 'srcset' in img.attrs:
                    img['data-original-srcset'] = img['srcset']

    def make_urls_absolute(self):
        for tag in ['img', 'source', 'video', 'audio', 'link']:
            for element in self.soup.find_all(tag):
                for attr in ['src', 'href']:
                    if attr in element.attrs:
                        try:
                            element[attr] = urljoin(self.base_url, element[attr])
                        except Exception as e:
                            logger.warning(f"Failed to make URL absolute: {str(e)}")

    def clean(self, config) -> str:
        # Remove HTML comments
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove unwanted elements
        for tag in ['script', 'style', 'noscript', 'meta', 'head', 'iframe']:
            for element in self.soup.find_all(tag):
                element.decompose()

        # Clean attributes from all elements
        for element in self.soup.find_all():
            for attr in list(element.attrs.keys()):
                if attr in Config.REMOVE_ATTRIBUTES or (
                    attr.startswith('data-') and 
                    attr not in ['data-src', 'data-srcset', 'data-original-src', 'data-original-srcset']
                ):
                    del element.attrs[attr]

        # Handle include/exclude tags
        if config.include_selectors:
            self.process_include_tags(config.include_selectors)

        if config.exclude_selectors:
            self.process_exclude_tags(config.exclude_selectors)

        # Handle main content filtering
        if config.only_main_content:
            for selector in Config.EXCLUDE_SELECTORS:
                elements = self.soup.select(selector)
                for element in elements:
                    should_keep = any(
                        element.select_one(include_selector) 
                        for include_selector in Config.FORCE_INCLUDE_SELECTORS
                    )
                    if not should_keep:
                        element.decompose()

        # Handle media
        if config.media:
            if config.media.extract_srcsets:
                self.process_srcsets()
            
            if config.media.make_urls_absolute:
                self.make_urls_absolute()

            if not config.media.preserve_urls:
                for tag in ['img', 'video', 'audio', 'source']:
                    for element in self.soup.find_all(tag):
                        for attr in ['src', 'srcset']:
                            if attr in element.attrs:
                                element[f'data-original-{attr}'] = element[attr]
                                del element[attr]

        return str(self.soup)