import subprocess
import pyautogui
import time
import sys
from PIL import ImageGrab, ImageChops

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

# ---------------- SCREEN CHANGE VERIFY ----------------
def screen_changed(before_img):
    after = ImageGrab.grab(bbox=VERIFY_REGION)
    diff = ImageChops.difference(before_img, after)
    pixels = list(diff.getdata())
    changed = sum(1 for p in pixels if sum(p[:3]) > 30)
    return changed > 4000

# ---------------- CLICK VERIFY ----------------
def click_and_verify(x, y, step_name):

    log(f"Clicking {step_name} at ({x},{y})")

    before = ImageGrab.grab(bbox=VERIFY_REGION)

    pyautogui.moveTo(x, y, duration=0.7)
    pyautogui.click()
    time.sleep(WAIT)

    if screen_changed(before):
        log(f"✅ {step_name} worked")
    else:
        log(f"⚠ {step_name} may not visibly change screen")

# ---------------- ENTER VALUE ----------------
def enter_value(value):
    time.sleep(0.5)
    pyautogui.hotkey("command", "a")
    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.write(str(value), interval=0.1)
    time.sleep(0.5)

# ---------------- MAIN FLOW ----------------
def run_get_measurement():

    log("Launching VastuApp...")
    subprocess.Popen(["open", "-a", APP_NAME])
    time.sleep(5)

    subprocess.call(['osascript', '-e', f'tell application "{APP_NAME}" to activate'])
    time.sleep(2)

    # STEP 1 - Open Recent Project
    click_and_verify(384, 466, "Recent_Project")
    time.sleep(4)

    # STEP 2 - Click Get Measurement
    click_and_verify(355, 377, "Get_Measurement")

    # STEP 3 - Set Reference
    click_and_verify(122, 295, "Set_Reference")

    # Reference Points
    log("Selecting Reference Points")
    pyautogui.moveTo(361, 244, duration=0.6)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(1092, 243, duration=0.6)
    pyautogui.click()
    time.sleep(2)

    # Enter Distance
    log("Entering Reference Distance")
    pyautogui.moveTo(593, 424, duration=0.6)
    pyautogui.doubleClick()
    enter_value(100)

    click_and_verify(711, 473, "Set_Distance")

    # STEP 4 - Measure Distance
    click_and_verify(163, 329, "Measure_Distance_Mode")

    log("Selecting Measurement Points")
    pyautogui.moveTo(361, 244, duration=0.6)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(1092, 243, duration=0.6)
    pyautogui.click()
    time.sleep(2)

    # STEP 5 - Undo
    click_and_verify(137, 411, "Undo_Last")

    # STEP 6 - Navigation Controls
    log("Testing Navigation Controls")

    click_and_verify(69, 521, "Reset_All")
    click_and_verify(180, 522, "Reset_Centre")
    click_and_verify(64, 621, "Zoom_In")
    click_and_verify(181, 617, "Zoom_Out")

    time.sleep(2)
    click_and_verify(181, 617, "Zoom_Out_Again")

    click_and_verify(153, 558, "Reset_Zoom")
    
    click_and_verify(1251 , 54, "close window button")

    print("\n" + "="*50)
    print("GET MEASUREMENT AUTOMATION COMPLETED")
    print("="*50)

# ---------------- RUN ----------------
if __name__ == "__main__":
    try:
        run_get_measurement()
    except KeyboardInterrupt:
        print("\n🛑 Automation stopped safely.")
        sys.exit()
