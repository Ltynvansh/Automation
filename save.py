import subprocess
import pyautogui
import time

APP_NAME = "VastuApp"  # Change if needed

pyautogui.FAILSAFE = True

pyautogui.PAUSE = 1

# ----------------------------
# 1️⃣ Open Application
# ----------------------------
print("Opening Vastu Application...")
subprocess.Popen(["open", "-a", APP_NAME])
time.sleep(5)

# ----------------------------
# 2️⃣ Click Recent Project
# ----------------------------
print("Clicking Recent Project...")
pyautogui.moveTo(350, 441, duration=1)
pyautogui.click()
time.sleep(5)

# ----------------------------
# 3️⃣ Move Cursor to Layout Area
# ----------------------------
pyautogui.moveTo(441, 388, duration=1)
time.sleep(1)

# ----------------------------
# 4️⃣ Move to Scroll Area
# ----------------------------
pyautogui.moveTo(443, 687, duration=1)
time.sleep(1)

# ----------------------------
# 5️⃣ Scroll Down
# ----------------------------
print("Scrolling down...")
for _ in range(10):
    pyautogui.scroll(-700)
    time.sleep(0.5)

time.sleep(1)

# ----------------------------
# 6️⃣ Click Gridded Report
# ----------------------------
print("Clicking Gridded Report...")
pyautogui.moveTo(169, 722, duration=1)
pyautogui.click()

time.sleep(5)

# ----------------------------
# 7️⃣ Click Save Button
# ----------------------------
print("Clicking Save button...")
pyautogui.moveTo(767, 390, duration=1)
pyautogui.click()

time.sleep(2)

# ----------------------------
# 8️⃣ Click Popup Button
# ----------------------------
print("Handling Popup...")
pyautogui.moveTo(799, 520, duration=1)
pyautogui.click()

print("✅ Report Generated & Popup Handled Successfully!")
print("🎉 FULL AUTOMATION COMPLETED!")
