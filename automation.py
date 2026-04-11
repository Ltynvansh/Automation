import subprocess
import pyautogui
import time
import json
import sys
import os
from PIL import ImageGrab, ImageChops

# ---------------- CONFIG ----------------
APP_NAME = "VastuApp"

EXPECTED_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/report_settings.json"
ACTUAL_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report_settings.json"

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
    return changed > 4000

def click_and_verify(x, y, step_name):
    log(f"Clicking {step_name} at ({x},{y})")

    before = ImageGrab.grab(bbox=VERIFY_REGION)

    pyautogui.moveTo(x, y, duration=0.6)
    pyautogui.click()
    time.sleep(WAIT)

    if screen_changed(before):
        log(f"✅ {step_name} worked")
    else:
        log(f"⚠ {step_name} no visible change")

# ---------------- INPUT ----------------
def enter_value(value):
    pyautogui.hotkey("command", "a")
    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.write(str(value), interval=0.1)
    time.sleep(0.5)

# =========================================================
# STEP 1: GET MEASUREMENT
# =========================================================
def run_get_measurement():

    log("Launching VastuApp...")
    subprocess.Popen(["open", "-a", APP_NAME])
    time.sleep(5)

    subprocess.call(['osascript', '-e', f'tell application "{APP_NAME}" to activate'])
    time.sleep(2)

    click_and_verify(370, 520, "Recent_Project")
    time.sleep(4)

    click_and_verify(355, 377, "Get_Measurement")
    click_and_verify(122, 295, "Set_Reference")

    pyautogui.click(361, 244)
    time.sleep(1)
    pyautogui.click(1092, 243)
    time.sleep(2)

    pyautogui.doubleClick(593, 424)
    enter_value(100)

    click_and_verify(711, 473, "Set_Distance")
    click_and_verify(163, 329, "Measure_Mode")

    pyautogui.click(361, 244)
    time.sleep(1)
    pyautogui.click(1092, 243)
    time.sleep(2)

    click_and_verify(137, 411, "Undo")

    click_and_verify(69, 521, "Reset_All")
    click_and_verify(180, 522, "Reset_Centre")
    click_and_verify(64, 621, "Zoom_In")
    click_and_verify(181, 617, "Zoom_Out")
    click_and_verify(153, 558, "Reset_Zoom")

    # 🔥 UPDATED CLOSE BUTTON
    click_and_verify(1120, 56, "Close_Measurement")

    log("✅ Measurement Completed")

# =========================================================
# STEP 2: LAYOUT + COMPASS (UPDATED)
# =========================================================
def create_layout_and_compass():

    log("Creating Layout")

    corners = [
        (606, 281),
        (1097, 275),
        (1096, 596),
        (603, 597),
        (606, 281)
    ]

    for i, (x, y) in enumerate(corners):
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        log(f"Point {i+1} clicked")
        time.sleep(1)

    log("✅ Layout Created")

    # 🔥 UPDATED COMPASS
    click_and_verify(373, 514, "Start_Compass")

    time.sleep(5)

    click_and_verify(373, 514, "Stop_Compass")

    log("⏳ Waiting 40 sec...")
    time.sleep(40)

    click_and_verify(991, 532, "Compass_Popup_OK")

# =========================================================
# STEP 3: GENERATE REPORT (UPDATED)
# =========================================================
def generate_gridded_report():

    log("Preparing Scroll Area")

    pyautogui.moveTo(437, 687, duration=1)
    pyautogui.click()

    for _ in range(10):
        pyautogui.scroll(-700)
        time.sleep(0.5)

    click_and_verify(138, 724, "Gridded_Report")

    log("⏳ Waiting 40 sec for report generation...")
    time.sleep(40)

    click_and_verify(766, 388, "Save_Button")
    time.sleep(2)

    click_and_verify(799, 520, "Save_OK")

    log("✅ Report Generated")

# =========================================================
# STEP 4: VALIDATION
# =========================================================
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def validate_toggles(expected, actual):

    log("Validating Toggles")

    exp = expected.get("toggles", {})
    act = actual.get("toggles", {})

    all_pass = True

    for key in exp:
        if key not in act:
            log(f"❌ Missing: {key}")
            all_pass = False
        elif exp[key] != act[key]:
            log(f"❌ Mismatch: {key}")
            all_pass = False
        else:
            log(f"✅ OK: {key}")

    return all_pass

# =========================================================
# MASTER FLOW
# =========================================================
if __name__ == "__main__":

    try:
        run_get_measurement()
        create_layout_and_compass()
        generate_gridded_report()

        log("Loading JSON")
        expected = load_json(EXPECTED_JSON)
        actual = load_json(ACTUAL_JSON)

        result = validate_toggles(expected, actual)

        print("\n" + "="*50)
        if result:
            print("🎉 FULL AUTOMATION PASSED")
        else:
            print("❌ FULL AUTOMATION FAILED")

    except KeyboardInterrupt:
        print("\n🛑 Stopped safely.")
        sys.exit(1)