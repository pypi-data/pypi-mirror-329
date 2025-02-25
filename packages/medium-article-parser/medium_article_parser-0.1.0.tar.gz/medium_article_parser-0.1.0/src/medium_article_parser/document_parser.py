import requests
from bs4 import BeautifulSoup
import html
import re
from typing import Optional, Literal

class ExportFormat:
    """A class to export articles in either markdown or plaintext format."""
    
    def __init__(self, url: str):
        """Initialize with article URL."""
        self.url = url
        self.soup = None
        self.article = None

    def fetch_article(self) -> None:
        """Fetch and parse the article."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, 'html.parser')
            self.article = self.soup.find('article')
            if not self.article:
                raise ValueError("Could not find article content. Please check if the URL is valid.")
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch the article: {str(e)}")

    def _convert_paragraph(self, paragraph: BeautifulSoup, output_format: str) -> str:
        """Convert HTML paragraph to desired format."""
        try:
            if output_format == 'plaintext':
                return paragraph.text.strip()
            
            # For markdown
            paragraph_text = str(paragraph)
            conversions = [
                (r'<p[^>]*>', ''),
                (r'</p>', ''),
                (r'<strong[^>]*>', '**'),
                (r'</strong>', '**'),
                (r'<em[^>]*>', '*'),
                (r'</em>', '*'),
                (r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)')
            ]
            
            for pattern, replacement in conversions:
                paragraph_text = re.sub(pattern, replacement, paragraph_text)
            return paragraph_text
        except Exception:
            return str(paragraph)

    def _convert_list(self, list_tag: BeautifulSoup, ordered: bool, output_format: str) -> str:
        """Convert HTML list to desired format."""
        try:
            items = []
            for idx, item in enumerate(list_tag.find_all('li')):
                if output_format == 'plaintext':
                    content = item.text.strip()
                else:
                    content = re.sub(r'</li>', '', 
                                   re.sub(r'<li[^>]*>', '', 
                                        self._convert_paragraph(item, 'markdown')))
                
                prefix = f"{idx + 1}. " if ordered else "- "
                items.append(f"{prefix}{content}")
            
            return '\n'.join(items) + '\n'
        except Exception:
            return ''

    def _convert_code_block(self, code_block: BeautifulSoup) -> str:
        """Convert HTML code block to text."""
        try:
            code_span = code_block.find('span')
            if not code_span:
                return str(code_block)
            
            cleaned_text = str(code_span)
            cleaned_text = re.sub(r'<br\s*/?>', '\n', cleaned_text)
            cleaned_text = re.sub(r'</?span[^>]*>', '', cleaned_text)
            return html.unescape(cleaned_text)
        except Exception:
            return str(code_block)

    def _convert_image(self, image: BeautifulSoup, output_format: str) -> Optional[str]:
        """Convert HTML image to desired format."""
        try:
            source = image.find('source')
            if source and source.get('srcset'):
                image_link = source.get('srcset').split(',')[0].split(' ')[0]
                if output_format == 'markdown':
                    return f'![Image]({image_link})'
                return image_link
            return None
        except Exception:
            return None

    def export_article(self, output_format: Literal['markdown', 'plaintext'] = 'markdown') -> str:
        """
        Export the article in the specified format.
        
        Args:
            output_format: Either 'markdown' or 'plaintext'
        
        Returns:
            The exported article text
        """

        if output_format not in ['markdown', 'plaintext']:
            raise ValueError("Invalid output format. Use 'markdown' or 'plaintext'")
            sys.exit()

        if not self.article:
            try:
                self.fetch_article()
            except Exception as e:
                raise Exception(f"Failed to fetch article: {e}")

        text_blocks = []
        tag_handlers = {
            'p': lambda tag: (f"{self._convert_paragraph(tag, output_format)}\n\n"
                            if 'pw-post-body-paragraph' in tag.get('class', []) else ''),
            
            'h1': lambda tag: (f"## {tag.text.strip()}\n" if output_format == 'markdown' else f"{tag.text.strip()}\n\n"
                            if 'pw-post-title' not in tag.get('class', []) else ''),
            
            'h2': lambda tag: (f"### {tag.text.strip()}\n" if output_format == 'markdown' else f"{tag.text.strip()}\n\n"),
            
            'blockquote': lambda tag: (f"> {self._convert_paragraph(tag.find('p'), output_format)}\n"
                                    if tag.find('p') else ''),
            
            'ul': lambda tag: f"{self._convert_list(tag, ordered=False, output_format=output_format)}\n",
            
            'ol': lambda tag: f"{self._convert_list(tag, ordered=True, output_format=output_format)}\n",
            
            'pre': lambda tag: (f"```{self._convert_code_block(tag)}```\n" 
                              if output_format == 'markdown' else f"{self._convert_code_block(tag)}\n"),
            
            'figure': lambda tag: (f"{self._convert_image(tag, output_format)}\n\n"
                                if self._convert_image(tag, output_format) else '')
        }

        for tag in self.article.find_all(['h1', 'h2', 'p', 'blockquote', 'ul', 'ol', 'pre', 'figure']):
            handler = tag_handlers.get(tag.name)
            if handler:
                text_blocks.append(handler(tag))

        return ''.join(text_blocks)