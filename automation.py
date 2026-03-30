import subprocess
import pyautogui
import time
import json
import sys
import os

APP_NAME = "VastuApp"

EXPECTED_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/report_settings.json"
ACTUAL_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report_settings.json"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1


# ---------------- JSON LOAD ----------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        sys.exit(1)


# ---------------- TOGGLE VALIDATION ----------------
def validate_toggles(expected, actual):

    print("\n🔎 Validating TOGGLES section...\n")

    expected_toggles = expected.get("toggles", {})
    actual_toggles = actual.get("toggles", {})

    all_pass = True

    # Missing + mismatch check
    for key in expected_toggles:
        if key not in actual_toggles:
            print(f"❌ Missing toggle: {key}")
            all_pass = False
        elif expected_toggles[key] != actual_toggles[key]:
            print(
                f"❌ Toggle mismatch → {key}: "
                f"expected={expected_toggles[key]} "
                f"actual={actual_toggles[key]}"
            )
            all_pass = False
        else:
            print(f"✅ {key} = {expected_toggles[key]}")

    print("\n====================================")

    if all_pass:
        print("✅ TOGGLE VALIDATION PASSED")
    else:
        print("❌ TOGGLE VALIDATION FAILED")

    return all_pass


# ---------------- UI AUTOMATION ----------------
def generate_gridded_report():

    print("Opening Vastu Application...")
    subprocess.Popen(["open", "-a", APP_NAME])
    time.sleep(5)

    print("Clicking Recent Project...")
    pyautogui.moveTo(350, 441, duration=1)
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(441, 388, duration=1)
    time.sleep(1)

    pyautogui.moveTo(443, 687, duration=1)
    time.sleep(1)

    print("Scrolling down...")
    for _ in range(10):
        pyautogui.scroll(-700)
        time.sleep(0.5)

    time.sleep(1)

    print("Clicking Gridded Report...")
    pyautogui.moveTo(169, 722, duration=1)
    pyautogui.click()
    time.sleep(5)

    print("Clicking Save button...")
    pyautogui.moveTo(767, 390, duration=1)
    pyautogui.click()
    time.sleep(2)

    print("Handling Popup...")
    pyautogui.moveTo(799, 520, duration=1)
    pyautogui.click()

    print("✅ Report Generated Successfully!")

    # Wait for file update
    print("Waiting for updated JSON...")
    for _ in range(10):
        if os.path.exists(ACTUAL_JSON):
            print("Actual JSON detected.")
            return
        time.sleep(1)

    print("❌ Actual JSON not found!")
    sys.exit(1)


# ---------------- RUN FULL FLOW ----------------
if __name__ == "__main__":

    try:
        generate_gridded_report()

        print("\n🔍 Loading JSON files...")
        expected = load_json(EXPECTED_JSON)
        actual = load_json(ACTUAL_JSON)

        result = validate_toggles(expected, actual)

        if result:
            print("\n🎉 FINAL RESULT: AUTOMATION PASSED")
            sys.exit(0)
        else:
            print("\n❌ FINAL RESULT: AUTOMATION FAILED")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C detected. Automation stopped safely.")
        sys.exit(1)
