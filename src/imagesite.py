from src.user import User
from src.browser import Browser


class ImageSite():
    BASE_URL = 'https://www.instagram.com/{}'

    def __init__(self, browser=None):
        self.browser = browser
        # Default browser to simplify
        if not self.browser:
            self.browser = Browser()

    def get_user(self, username):
        content = self._get_user_content(username)
        return User(username, content)

    def _get_user_content(self, username):
        url = ImageSite.BASE_URL.format(username)
        self.browser.set_url(url)
        return self.browser.get_page_content()
