import threading
import keyboard
import time
import pyautogui

FishStreak = 0
Enabled = True
Reeling = False
ImagePaths = [
    "Images/FishCaught.png",
    "Images/TreasureCaught.png"
]


def await_image(image="Images/Exclamation.png", confidence=1.0, fish_caught=False):
    global Reeling, FishStreak
    found = False
    while Enabled and not found:
        try:
            res = pyautogui.locateOnScreen(image, confidence=confidence)
            found = True
            if not fish_caught:
                Reeling = True
                print("!")
                for i in ImagePaths:
                    result_thread = threading.Thread(target=await_image, args=(i, 0.6, True))
                    result_thread.start()
                while Reeling:
                    pyautogui.click()
                    time.sleep(0.1)
                return True
            else:
                Reeling = False
                time.sleep(0.5)
                pyautogui.click()
                return True
        except Exception as e:
            pass
    return False


def on_key_event(e):
    global Enabled, Reeling
    if e.name == 'page down':
        Enabled = not Enabled
        Reeling = False


if __name__ == "__main__":
    keyboard.on_press_key('page down', on_key_event)
    try:
        while True:
            time.sleep(0.15)
            if Enabled:
                await_image(confidence=0.75)
                if not Reeling:
                    FishStreak += 1
                    print(f"Caught {FishStreak}")

    finally:
        keyboard.unhook_all()
