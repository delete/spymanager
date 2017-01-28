from .browser import Browser
from . myexceptions import ChatIdOrTextCannotBeEmpty
from . import TELEGRAM_URL


class Publisher():

    def __init__(self, api_token):
        self.api_token = api_token
        self.browser = Browser()
        self.chat_id = ''
        self.text_to_send = ''

    def _create_url(self):
        return TELEGRAM_URL.format(
            token=self.api_token,
            method='sendMessage',
            chat_id=self.chat_id,
            text=self.text_to_send
        )

    def send_to(self, chat_id):
        self.chat_id = chat_id

    def send(self, text):
        self.text_to_send = text

        if not self.chat_id or not self.text_to_send:
            raise ChatIdOrTextCannotBeEmpty

        url = self._create_url()
        self.browser.set_url(url)
        self.browser.get()
