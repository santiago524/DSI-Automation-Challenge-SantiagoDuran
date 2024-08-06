from fastapi import FastAPI
import pyautogui as robot
import time
import os

def open_edge():
    os.system('start msedge')
    time.sleep(0.5)
    bar = robot.locateOnScreen('bar.png')
    print(bar)
    time.sleep(1)
    if bar:
        robot.click(bar)
        time.sleep(0.5)
        robot.write('https://www.google.com/')
        robot.press('enter')

def open_text_edit():
    os.system('start notepad')
    time.sleep(0.5)

def nav(name_doc):
    dir = os.chdir('/files')
    open(dir + f'/{name_doc}')

open_text_edit()