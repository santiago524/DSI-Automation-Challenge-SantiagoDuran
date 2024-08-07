from fastapi import FastAPI
import pyautogui as robot
import time
import os


class Open_app:
    
    def open_edge(self):
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

    def open_text_edit(self):
        os.system('start notepad')
        time.sleep(0.5)

    def nav(self, name_doc):
        dir = os.chdir('/files')
        open(dir + f'/{name_doc}')
