import threading
import keyboard
import time
import pyautogui

Version = "0.22a"
FishStreak = 0
Enabled = True
Reeling = False
Cooldown = 0
ImagePaths = [
    "Images/FishCaught.png",
    "Images/TreasureCaught.png",
    "Images/JunkCaught.png"
]


def await_image(image="Images/Exclamation.png", confidence=1.0, fish_caught=False, timeout=0.0):
    global Reeling, FishStreak, Cooldown
    found = False
    while Enabled and not found and timeout == 0 or timeout > time.time():
        try:
            res = pyautogui.locateOnScreen(image, confidence=confidence, grayscale=True)
            found = True
            if not fish_caught:
                Reeling = True
                print("!")
                for i in ImagePaths:
                    result_thread = threading.Thread(target=await_image, args=(i, 0.7, True))
                    result_thread.start()
                while Reeling:
                    pyautogui.click()
                return True
            elif Reeling:
                if Cooldown == 0 or Cooldown < time.time():
                    Cooldown = time.time() + 8
                    Reeling = False
                    return True
                return False
            else:
                return False
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
                if Cooldown == 0 or Cooldown < time.time()-6:
                    await_image(confidence=0.65, timeout=time.time()+30)
                    if not Reeling:
                        pyautogui.click()
                        FishStreak += 1
                        print(f"Caught {FishStreak}")

    finally:
        keyboard.unhook_all()
