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
        self.__run_async(self.__initialize())

    async def __initialize(self):
        """Asynchronously launches the browser and retrieves the first page."""
        self.browser = await pyppeteer.launch(**config.browser)
        self.page = (await self.browser.pages())[0]

    async def __set_code(self, token):
        """Private coroutine to set the authentication code using the provided token.

        Args:
            token (str): The token to be entered.
        """
        await self.page.waitForSelector(tags.secret)

        await self.__clear_input()

        await self.page.keyboard.type(token)
        await asyncio.sleep(1)

    async def __clear_input(self):
        """Clears the input field by selecting all text and deleting it.

        This function simulates a user selecting all text in the input field
        and then pressing 'Backspace' to delete it.

        Steps:
        1. Click on the input field to focus.
        2. Hold 'Control' key (or 'Command' on macOS).
        3. Press 'A' to select all text.
        4. Release 'Control' key.
        5. Press 'Backspace' to delete the selected text.
        """

        await self.page.click(tags.secret)  # Focus on the input field
        await self.page.keyboard.down('Control')  # Hold Control key
        await self.page.keyboard.press('A')  # Select all text
        await self.page.keyboard.up('Control')  # Release Control key
        await self.page.keyboard.press('Backspace')  # Delete the selected text

    async def __get_code(self):
        """Private coroutine to retrieve the authentication code.

        Returns:
            str: The authentication code.
        """
        element = await self.page.waitForSelector(tags.code)
        return await document.getAttribute(self.page, 'value', element)

    async def __close(self):
        """Closes the browser instance."""
        await self.browser.close()

    def set_code(self, token):
        """Sets the authentication code synchronously.

        Args:
            token (str): The token to be entered.
        """
        self.loop.run_until_complete(self.__set_code(token))

    def get_code(self):
        """Retrieves the authentication code synchronously.

        Returns:
            str: The authentication code.
        """
        return self.loop.run_until_complete(self.__get_code())

    def close(self):
        """Closes the browser instance."""
        return self.loop.run_until_complete(self.__close())

    def __run_async(self, coro):
        """Runs the given coroutine until complete.

        Args:
            coro (Coroutine): The coroutine to run.

        Returns:
            Any: The result of the coroutine.
        """
        return self.loop.run_until_complete(coro)
