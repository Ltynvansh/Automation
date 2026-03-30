import subprocess
import pyautogui
import time
import json
import zipfile

# ---------------- CONFIG ----------------

APP_NAME = "VastuApp"

JSON_PATH = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report_settings.json"

DOCX_PATH = "/Users/vanshlatiyan/Downloads/Gridded Report_latestProject_Flat_Layout_Report_20260317_152610.docx"

WAIT = 3


# ---------------- OPEN APP ----------------

print("\nLaunching VastuApp...\n")

subprocess.Popen(["open", "-a", APP_NAME])

time.sleep(6)


# ---------------- ACTIVATE APP ----------------

subprocess.call(
    ['osascript', '-e', f'tell application "{APP_NAME}" to activate']
)

time.sleep(2)


# ---------------- CLICK RECENT PROJECT ----------------

print("Opening recent project...")

pyautogui.moveTo(386, 514, duration=1)
pyautogui.click()

time.sleep(5)


# ---------------- DRAW CLOSED FIGURE ----------------
# Example coordinates (replace with your real ones)

print("Drawing closed figure...")

points = [
    (600, 400),
    (800, 400),
    (800, 600),
    (600, 600)
]

pyautogui.moveTo(points[0])

pyautogui.mouseDown()

for p in points[1:]:
    pyautogui.moveTo(p, duration=0.5)

pyautogui.moveTo(points[0], duration=0.5)

pyautogui.mouseUp()

time.sleep(2)


# ---------------- STOP COMPASS ----------------

print("Stopping compass...")

pyautogui.press("esc")

time.sleep(6)


# ---------------- SCROLL DOWN ----------------

print("Scrolling...")

pyautogui.scroll(-800)

time.sleep(2)


# ---------------- CLICK DETAILED REPORT ----------------

print("Opening detailed report...")

pyautogui.moveTo(342, 725, duration=1)
pyautogui.click()

time.sleep(5)


# ---------------- FULLSCREEN ----------------

print("Entering fullscreen...")

pyautogui.moveTo(54, 46, duration=1)
pyautogui.click()

time.sleep(2)


# ---------------- GENERATE REPORT ----------------

print("Generating report...")

pyautogui.moveTo(1187, 475, duration=1)
pyautogui.click()

print("Waiting for report generation...")

time.sleep(20)


# =====================================================
#                REPORT VALIDATION
# =====================================================

print("\nReading JSON toggles...\n")

# ---------------- LOAD JSON ----------------

with open(JSON_PATH) as f:
    data = json.load(f)

toggles = data.get("toggles", {})


# ---------------- TOGGLE → TITLE MAPPING ----------------

TOGGLE_TO_TITLE = {
    "8 Zones Analysis": "8 Vastu Zone Analysis",
    "16 Zones Analysis": "16 Vastu Zone Analysis",
    "24 Zones Analysis": "24 Vastu Zone Analysis",
    "64 Zones Analysis": "64 Vastu Gridded Image",
    "32 Zone Moderne vastu": "32 Zones Analysis (Moderne vastu)",
    "32 Zone Vedic Vastu": "32 Zones Analysis (Vedic)",
    "Marma sthan": "Marmsthan Image",
    "Body part": "Body Part Analysis",
    "64 padvinyash": "64 Padvinyash Analysis",
    "81 padvinyash": "81 Padvinyash Analysis",
    "Triguna": "TriGuna (Moderne vastu)",
    "Triguna Vedic Vastu": "TriGuna (Vedic)",
    "Tridosha Moderne vastu": "TriDosha (Moderne vastu)",
    "Tridosha Vedic Vastu": "TriDosha (Vedic)"
}


def get_title(toggle):
    return TOGGLE_TO_TITLE.get(toggle, toggle)


enabled_sections = []

for toggle, value in toggles.items():

    if value is True:

        title = get_title(toggle)

        enabled_sections.append(title)

        print("ON :", toggle, "→", title)


# ---------------- READ DOCX ----------------

print("\nReading generated report...\n")

with zipfile.ZipFile(DOCX_PATH) as docx:

    xml = docx.read("word/document.xml").decode()


# ---------------- VALIDATE ----------------

print("\nValidating report...\n")

pass_count = 0
fail_count = 0

for title in enabled_sections:

    if title in xml:

        print("PASS :", title)

        pass_count += 1

    else:

        print("FAIL :", title)

        fail_count += 1


# ---------------- SUMMARY ----------------

print("\n============================")
print("VALIDATION SUMMARY")
print("============================")

print("Total Checked :", len(enabled_sections))
print("PASS :", pass_count)
print("FAIL :", fail_count)

print("\nAutomation Completed Successfully\n")