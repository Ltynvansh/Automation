import os

def switch_to_desktop(number):
    # This simulates the Control + [Number] shortcut
    # Note: '18' is the key code for '1', '19' for '2', etc.
    # A simpler way is to use the 'keystroke' command
    script = f'tell application "System Events" to keystroke "{number}" using control down'
    os.system(f"osascript -e '{script}'")

# Example: Switch to Desktop 2
switch_to_desktop(2)