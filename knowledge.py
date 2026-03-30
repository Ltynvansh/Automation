import subprocess
import pyautogui # type: ignore
import time
import sys
from PIL import ImageGrab, ImageChops # type: ignore

# ---------------- CONFIG ----------------
APP_NAME = "VastuApp"
WAIT = 2
VERIFY_REGION = (300, 200, 1200, 800)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

script_start = time.time()

# ---------------- LOG ----------------
def log(msg):
    print(f"[{round(time.time()-script_start,2)}s] {msg}")

# ---------------- SCREEN VERIFY ----------------
def screen_changed(before_img):
    after = ImageGrab.grab(bbox=VERIFY_REGION)
    diff = ImageChops.difference(before_img, after)
    pixels = list(diff.getdata())
    changed = sum(1 for p in pixels if sum(p[:3]) > 30)
    return changed > 5000

def click_and_verify(x, y, step_name):
    log(f"Clicking {step_name} at ({x},{y})")
    before = ImageGrab.grab(bbox=VERIFY_REGION)
    pyautogui.moveTo(x, y, duration=0.6)
    pyautogui.click()
    time.sleep(WAIT)

    if screen_changed(before):
        log(f"✅ {step_name} worked")
    else:
        log(f"⚠ {step_name} may not change screen")

# ---------------- GENERIC CARD PROCESSOR ----------------
def process_cards(cards, start_index):
    success = 0
    for i, (show_coord, close_coord) in enumerate(cards):
        card_number = start_index + i
        log(f"Opening Card {card_number}")

        pyautogui.moveTo(*show_coord)
        pyautogui.click()
        time.sleep(2)

        pyautogui.moveTo(*close_coord)
        pyautogui.click()
        time.sleep(1.5)

        success += 1

    return success

# ---------------- MAIN KNOWLEDGE FLOW ----------------
def run_knowledge():

    log("Launching VastuApp...")
    subprocess.Popen(["open", "-a", APP_NAME])
    time.sleep(5)

    subprocess.call(['osascript', '-e', f'tell application "{APP_NAME}" to activate'])
    time.sleep(2)

    click_and_verify(152, 315, "Knowledge_Section")
    click_and_verify(260, 423, "Fullscreen")

    total_success = 0

    # ----------- C1–C8 -----------
    cards_part1 = [
        ((436, 372), (615, 588)),
        ((619, 366), (632, 567)),
        ((833, 370), (687, 549)),
        ((1092, 378), (666, 548)),
        ((413, 676), (615, 631)),
        ((653, 682), (647, 588)),
        ((864, 676), (693, 518)),
        ((1096, 685), (653, 629)),
    ]

    total_success += process_cards(cards_part1, 1)

    # Scroll after C8
    log("Scrolling after C8")
    pyautogui.moveTo(1271, 284)
    pyautogui.click()
    time.sleep(3)

    # ----------- C9–C16 -----------
    cards_part2 = [
        ((389, 298), (619, 589)),
        ((653, 296), (646, 589)),
        ((872, 294), (651, 588)),
        ((1109, 298), (638, 662)),
        ((399, 594), (642, 517)),
        ((634, 594), (638, 547)),
        ((865, 595), (637, 588)),
        ((1114, 594), (640, 569)),
    ]

    total_success += process_cards(cards_part2, 9)

    # Scroll after C16
    log("Scrolling after C16")
    pyautogui.moveTo(1274, 423)
    pyautogui.click()
    time.sleep(3)

    # ----------- C17–C24 -----------
    cards_part3 = [
        ((394, 298), (638, 514)),   # C17
        ((632, 297), (642, 575)),   # C18
        ((874, 300), (643, 573)),   # C19
        ((1104, 295), (635, 591)),  # C20
        ((396, 625), (649, 537)),   # C21
        ((630, 625), (648, 537)),   # C22
        ((868, 618), (644, 514)),   # C23
        ((1109, 621), (640, 574)),  # C24
    ]

    total_success += process_cards(cards_part3, 17)

    # Final scroll after C24
    log("Final Scroll after C24")
    pyautogui.moveTo(1273, 559)
    pyautogui.click()
    time.sleep(3)

    print("\n" + "="*50)
    print("KNOWLEDGE SECTION AUTOMATION COMPLETE")
    print("="*50)
    print(f"Total Cards Processed: {total_success}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    try:
        run_knowledge()
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped safely.")
        sys.exit()