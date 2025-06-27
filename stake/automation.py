from playwright.sync_api import sync_playwright
import json
import os
import time

COOKIES_PATH = "stake_cookies.json"
BONUS_URL = "https://stake.us/settings/api?tab=dailyBonus"

def save_cookies(context):
    cookies = context.storage_state(path=None)
    with open(COOKIES_PATH, "w") as f:
        json.dump(cookies, f)
    print("[+] Session cookies saved.")

def load_cookies():
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, "r") as f:
            return json.load(f)
    return None

def claim_daily_bonus():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = None

        cookies = load_cookies()
        if cookies:
            context = browser.new_context(storage_state=cookies)
            print("[*] Loaded session from cookies.")
        else:
            context = browser.new_context()
            print("[!] No saved session. Logging in manually required.")

        page = context.new_page()
        page.goto(BONUS_URL)

        if not cookies:
            print("Please log in manually...")
            input("Press ENTER once you're fully logged in and can see your bonus wallet...")
            save_cookies(context.storage_state())

        try:
            print("[*] Looking for bonus claim button...")
            page.wait_for_selector("text=Claim Daily Bonus", timeout=10000)
            page.click("text=Claim Daily Bonus")
            print("[+] Bonus claimed successfully!")

        except Exception:
            print("[!] Bonus not available to claim or button not found.")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    claim_daily_bonus()
