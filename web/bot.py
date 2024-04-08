from pyppeteer import launch
import os

async def visit():
    browser = await launch(
        headless=True,
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        args=[
		        "--no-sandbox",
		        "--disable-setuid-sandbox",
		        "--js-flags=--noexpose_wasm,--jitless"
        ]
    )
    page = await browser.newPage()
    
    cookies = {'name': 'flag', 'value': os.getenv("FLAG"), 'url': 'http://127.0.0.1:1234'}
    await page.setCookie(cookies)
    
    await page.goto('http://127.0.0.1:1234/index')

    await page.close()

    await browser.close()
    return
