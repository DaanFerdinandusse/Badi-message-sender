# Standard
import json
import logging
from time import sleep

# Playwright
from playwright.sync_api import sync_playwright, Browser, Page


def send_message_to_room(room_url: str, page: Page):
    MESSAGE: str = """Hi {landlord_name},

Would it be possible to rent the apartment for 2 weeks instead of the normal long term stay? I am a young professional working in tech and looking for a short term accommodation in Barcelona.

I am very clean and respectful of other people's space. I am in Barcelona at the moment so it would be possible to meet in person if you would like.

Looking forward to hearing from you soon :) """
    # Load the room page
    page.goto(room_url, wait_until='load')

    # Accept the cookies
    if page.is_visible('button[class="iubenda-cs-accept-btn iubenda-cs-btn-primary"]'):
        page.click('button[class="iubenda-cs-accept-btn iubenda-cs-btn-primary"]')

    # Check ifn the "Request chat" button is available
    if not page.is_visible('button[data-qa="simplify-enquiry-button"]'):
        logging.info(f"Skipping {room_url} as the 'Request chat' button is not available")
        sleep(2)
        return

    # Click on the "Request chat" button
    page.click('button[data-qa="simplify-enquiry-button"]')

    page.wait_for_selector('h1[data-qa="user-nameage-heading"]')

    # Get the name of the person renting out the appartment
    landlord_name: str = page.text_content('h1[data-qa="user-nameage-heading"]').split(", ")[0]

    # Fill in the message field
    page.type('textarea[name="enquiry-message"]', MESSAGE.format(landlord_name=landlord_name))

    # Click on the "Send" button
    page.click('button[data-qa="message-enquiry-submit"]')

    sleep(2)



def main():
    """

    :return:
    """
    with open("rooms_data.json", "r") as f:
        rooms_data = json.load(f)

    BASE_URL = "https://badi.com/en/room/"
    URLS = [f"{BASE_URL}{room['room_id']}" for room in rooms_data["data"]['results']]

    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()  # Create a new browser context

        # Set cookies
        context.add_cookies([
            {
                'name': 'badi_device_id',
                'value': '4a3b313a-fbcd-40d9-98ba-ce6b40eb7ce7',
                'domain': 'badi.com',
                'path': '/',
            },
            {
                'name': 't_app',
                'value': 'c56d32d3c1b1f3b41c9fd42d1973780123660609f2db225e5a0dda12e0b390f5%7CBearer%7C1715150105777%7C1712520403000%7C3798328%7Cfalse%7Cdefault%7Ctrue%7C29670896103139917e51e5c698b1f642beb9f7b65341fa8398a64a2748d4660f',
                'domain': 'badi.com',
                'path': '/',
            }
        ])

        page = context.new_page()
        # Disable image loading to speed up the scraping
        page.route('**/*.{png,jpg,jpeg,webp,gif}', lambda route: route.abort())

        for url in URLS:
            send_message_to_room(url, page)

        page.close()
        browser.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()