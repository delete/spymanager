import requests
import shutil


class Browser():
    """Handle HTTP requests"""

    def __init__(self, url=''):
        self.url = url

    def set_url(self, url):
        self.url = url

    def get(self):
        return requests.get(self.url)

    # Return HTML text content
    def get_page_content(self):
        page = self.get()
        return page.text

    # Download content from URL and save with the given filename
    def save_as(self, filename):
        response = requests.get(self.url, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
