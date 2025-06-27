from playwright.sync_api import sync_playwright
import json
import os
import time

COOKIES_PATH = "stake_cookies.json"
USER_DATA_DIR = "/tmp/playwright-stake"
BONUS_URL = "https://stake.us/settings/api?tab=dailyBonus"

def save_cookies(context):
    context.storage_state(path=COOKIES_PATH)
    print("[+] Session cookies saved.")

def load_browser(playwright):
    print("[*] Launching persistent browser session...")
    browser = playwright.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        slow_mo=50
    )
    return browser

def claim_daily_bonus():
    with sync_playwright() as p:
        browser = load_browser(p)
        page = browser.pages[0] if browser.pages else browser.new_page()

        print(f"[*] Navigating to {BONUS_URL}")
        page.goto(BONUS_URL)

        if not os.path.exists(COOKIES_PATH):
            print("[!] First-time login required.")
            print("🔐 Please log in manually and solve the CAPTCHA.")
            input("✅ Once logged in and bonus wallet is visible, press ENTER here...")
            save_cookies(browser)
        else:
            print("[*] Using existing session...")

        try:
            print("[*] Waiting for 'Claim Daily Bonus' button...")
            page.wait_for_selector("text=Claim Daily Bonus", timeout=10000)
            page.click("text=Claim Daily Bonus")
            print("[+] Bonus claimed successfully!")

        except Exception as e:
            print("[!] Bonus not available or button not found.")
            print(f"    Debug: {e}")

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    claim_daily_bonus()
