import pyautogui
import time

print("🔁 Hover over the 'Claim Bonus' button. Script running...")

clicks = 0
while True:
    pyautogui.click()
    print(f"🖱️ Clicked at {time.strftime('%H:%M:%S')}")
    clicks += 1

    if clicks % 10 == 0:  # Every 10 minutes
        pyautogui.scroll(-5)  # Small scroll down
        pyautogui.scroll(5)   # Scroll back up
        print("↕️ Scrolled to prevent timeout")

    time.sleep(60)
