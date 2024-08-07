import pytesseract as tess
from PIL import Image
import pyautogui as robot
import os
import cv2 as cv
import time
import win32com.client
import pygetwindow as gw
import re

tess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Analysis:
    def __init__(self):
        self.keywords_selected = []

    def open_edge(self):
        os.system('start msedge')
        time.sleep(0.5)
        bar = robot.locateOnScreen('bar.png')
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

    @staticmethod
    def capt_screen():
        screenshot = robot.screenshot()
        screenshot_path = os.path.join(os.getcwd(), 'screen.png')
        screenshot.save(screenshot_path)
        return screenshot_path

    @staticmethod
    def text_from_image(capture):
        capt = cv.imread(capture)
        txt = tess.image_to_string(capt)
        return txt

    @staticmethod
    def position_keyword(keyword, txt):
        lines = txt.split('\n')
        for position, line in enumerate(lines):
            if keyword.lower() in line.lower():
                return position, line.lower().index(keyword.lower())
        return None, None

    @staticmethod
    def capt_region(capture, keyword):
        txt = Analysis.text_from_image(capture)
        position, line = Analysis.position_keyword(keyword, txt)

        if position is not None:
            data = tess.image_to_data(cv.imread(capture), output_type=tess.Output.DICT)

            for pos, word in enumerate(data['text']):
                if keyword.lower() in word.lower():
                    x, y, w, h = data['left'][pos], data['top'][pos], data['width'][pos], data['height'][pos]
                    region = (x - 20, y - 20, w + 50, h + 50)
                    screenshot = robot.screenshot(region=region)
                    screenshot_path = os.path.join(os.getcwd(), 'screenshots', f'{keyword}_region{pos}.png')
                    screenshot.save(screenshot_path)
                    return screenshot_path
        return None
    
    def add_keywords(self, palabra):
        self.keywords_selected.append(palabra)
        print(f'Palabra clave "{palabra}" agregada a la lista.')
    
    def show_keywords(self):
        print("Palabras clave actuales:")
        for palabra in self.keywords_selected:
            print(f'- {palabra}')

    @staticmethod
    def get_email(text):
        email_structure = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_structure, text)
        return emails

    def open_doc(self, doc, keywords):
        time.sleep(1)
        word_app = win32com.client.Dispatch('Word.Application')
        word_app.Visible = True
        approved_path = os.getcwd() + '\Aspirantes_aprobados' 
        not_approved_path = os.getcwd() + '\Aspirantes_no_aprobados'

        for filename in os.listdir(doc):
            if filename.endswith('.docx') or filename.endswith('.doc'):
                path = os.path.join(doc, filename)
                document = word_app.Documents.Open(path)
                time.sleep(3)
                word_app.WindowState = 1

                word_window = gw.getWindowsWithTitle('Word')[0]
                word_window.activate()

                time.sleep(1)
                capture = self.capt_screen()

                for keyword in keywords:
                    region = self.capt_region(capture, keyword)
                    if region:
                        text = self.text_from_image(capture)
                        email = self.get_email(text)
                        if email:
                            with open(os.path.join(approved_path, f'{email[0]}.txt'), 'w') as f:
                                    f.write(email[0])
                    else:
                        text = self.text_from_image(capture)
                        email = self.get_email(text)
                        with open(os.path.join(not_approved_path, f'{email[0]}.txt'), 'w') as f:
                            f.write(email[0]) 


                document.Close(False)
        word_app.Quit()

if __name__ == '__main__':
    path = os.getcwd() + '\docs'
    keywords = ['hola']
    bot = Analysis()
    bot.open_doc(path, keywords)
