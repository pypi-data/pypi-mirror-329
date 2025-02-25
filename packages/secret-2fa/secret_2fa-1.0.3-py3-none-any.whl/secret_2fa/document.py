async def getAttribute(page, attribute, element):
    return await page.evaluate(f'(element) => element.getAttribute("{attribute}")', element)
