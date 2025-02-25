import asyncio
import pyppeteer

from . import document
from . import config
from . import tags


class authen:
    """Class for handling two-factor authentication using pyppeteer."""

    def __init__(self):
        """Initializes the event loop and launches the browser."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.run_async(self.initialize())

    async def initialize(self):
        """Asynchronously launches the browser and retrieves the first page."""
        self.browser = await pyppeteer.launch(**config.browser)
        self.page = (await self.browser.pages())[0]

    async def _set_code(self, token):
        """Private coroutine to set the authentication code using the provided token.

        Args:
            token (str): The token to be entered.
        """
        await self.page.waitForSelector(tags.secret)
        await self.page.click(tags.secret)
        await self.page.keyboard.type(token)

    async def _get_code(self):
        """Private coroutine to retrieve the authentication code.

        Returns:
            str: The authentication code.
        """
        element = await self.page.waitForSelector(tags.code)
        return await document.getAttribute(self.page, 'value', element)

    def set_code(self, token):
        """Sets the authentication code synchronously.

        Args:
            token (str): The token to be entered.
        """
        self.loop.run_until_complete(self._set_code(token))

    def get_code(self):
        """Retrieves the authentication code synchronously.

        Returns:
            str: The authentication code.
        """
        return self.loop.run_until_complete(self._get_code())

    def run_async(self, coro):
        """Runs the given coroutine until complete.

        Args:
            coro (Coroutine): The coroutine to run.

        Returns:
            Any: The result of the coroutine.
        """
        return self.loop.run_until_complete(coro)
