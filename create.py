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

# ---------------- LOG FUNCTION ----------------
def log(msg):
    print(f"[{round(time.time()-script_start,2)}s] {msg}")

# ---------------- SCREEN CHANGE DETECTION ----------------
def screen_changed(before_img):
    after = ImageGrab.grab(bbox=VERIFY_REGION)
    diff = ImageChops.difference(before_img, after)

    pixels = list(diff.getdata())

    changed = sum(
        1 for p in pixels if sum(p[:3]) > 30
    )

    return changed > 5000

# ---------------- CLICK WITH VERIFY ----------------
def click_and_verify(x, y, step_name):

    log(f"Clicking {step_name} at ({x},{y})")

    before = ImageGrab.grab(bbox=VERIFY_REGION)

    pyautogui.moveTo(x, y, duration=0.8)
    pyautogui.click()
    time.sleep(WAIT)

    if screen_changed(before):
        log(f"✅ {step_name} worked")
        return True
    else:
        log(f"⚠ {step_name} may not change screen (continuing)")
        return True

# ---------------- STABLE TEXT ENTRY ----------------
def enter_value(value):
    time.sleep(0.5)
    pyautogui.hotkey("command", "a")
    time.sleep(0.3)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.write(str(value), interval=0.1)
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(0.5)

# ---------------- MAIN AUTOMATION FLOW ----------------
def run_layout_shape_automation():

    log("Launching VastuApp...")
    subprocess.Popen(["open", "-a", APP_NAME])
    time.sleep(5)

    subprocess.call(['osascript', '-e', f'tell application "{APP_NAME}" to activate'])
    time.sleep(2)

    # STEP 1 - Create & Edit Layout
    if not click_and_verify(381, 263, "Create_Edit_Layout"):
        return

    # STEP 2 - Fullscreen (Your Coordinate)
    log("Applying Fullscreen")
    pyautogui.moveTo(55, 44, duration=1)
    pyautogui.click()
    time.sleep(3)

    # STEP 3 - New Layout
    if not click_and_verify(127, 138, "New_Layout"):
        return

    # STEP 4 - Generate Layout
    if not click_and_verify(280, 629, "Generate_Layout"):
        return

    # STEP 5 - Use Layout
    if not click_and_verify(256, 679, "Use_Layout"):
        return

    # STEP 6 - Select Rectangle Shape
    if not click_and_verify(1182, 355, "Rectangle_Shape"):
        return

    # STEP 7 - Enter Length = 100
    log("Activating Length field")
    pyautogui.moveTo(380, 331, duration=0.6)
    pyautogui.doubleClick()
    enter_value(100)
    log("Length entered")

    # STEP 8 - Enter Breadth = 100
    log("Activating Breadth field")
    pyautogui.moveTo(370, 364, duration=0.6)
    pyautogui.doubleClick()
    enter_value(100)
    log("Breadth entered")

    # STEP 9 - Click Create
    if not click_and_verify(522, 703, "Create_Shape"):
        return
    # Step 10 - Apply Grid on layout 
    if not click_and_verify(680, 151, "Apply_Grid"):
        return
    # Step 11 - Click Show Grid
    if not click_and_verify(603, 451, "Show_Grid"):
        return
    
    #Step 12 - Click Apply Button on Grid
    if not click_and_verify(592, 501, "Apply_Grid"):
        return
    # Step 13 - Click Ok Button on Popup
    if not click_and_verify(669, 507, "Popup_OK"):
        return
    # Step 14 Click on set refernce point
    if not click_and_verify(764, 147, "Set_Reference"):
        return  
    #Step 15 - Click on layout to set reference point
    if not click_and_verify(380, 312, "Set_Reference_Point"):
        return  
    #Step 16 Click on second point to set reference distance
    if not click_and_verify(816, 311, "Set_Reference_Point_2"):
        return
    # Step 17 - Enter Reference Distance
    log("Activating Reference Distance field")
    pyautogui.moveTo(566, 424, duration=0.6)
    pyautogui.doubleClick()
    enter_value(100)
    log("Reference Distance entered")
    # Step 18 - Click Set Distance
    if not click_and_verify(728, 512, "Set_Reference_Distance"):
        return
    
    #Step 19 - Click on Add Compas Button
    if not click_and_verify(850, 145, "Add_Compass"):
        return
    
    #Step 21 - Enter Compass Value 
    log("Activating Compass Angle field")
    pyautogui.moveTo(604, 422, duration=0.6)
    pyautogui.doubleClick()
    enter_value(45)
    log("Compass Angle entered")
    # Step 22 - Click Set Compass
    if not click_and_verify(586, 530, "Set_Compass"):
        return
    #step 23 - click ok on popup
    if not click_and_verify(586, 530, "Popup_OK_Compass"):
        return
    #Step 24 - Click on Remove Image 
    if not click_and_verify(570, 150, "Remove_Image"):
        return
    

    print("\n" + "="*50)
    print("LAYOUT SHAPE CREATION SUCCESSFUL")
    print("="*50)

# ---------------- RUN ----------------
if __name__ == "__main__":
    try:
        run_layout_shape_automation()
    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C detected. Automation stopped safely.")
        sys.exit()
