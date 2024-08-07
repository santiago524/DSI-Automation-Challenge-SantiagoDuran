import pytesseract as tess
from PIL import Image
import pyautogui as robot
import os
import cv2 as cv
import time
import win32com.client
import pygetwindow as gw
import re
from OpenWeb import Open_app

tess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'         


def capt_screen():
    screenshot = robot.screenshot()
    screenshot.save('screen.png')
    return 'screen.png'

def text_from_image(capture):
    capt = cv.imread(capture)
    txt = tess.image_to_string(capt)
    return txt

def position_keyword(keyword, txt):
    lines = txt.split('\n')
    for position, line in enumerate(lines):
        if keyword.lower() in line.lower():
            return position, line.lower().index(keyword.lower())
    return None, None

def capt_region(capture, keyword):
    txt = text_from_image(capture)
    position, line = position_keyword(keyword, txt)

    if position is not None:
        data = tess.image_to_data(cv.imread(capture), output_type=tess.Output.DICT)

        for pos, word in enumerate(data['text']):
            if keyword.lower() in word.lower():
                x, y, w, h= data['left'][pos], data['top'][pos], data['width'][pos], data['height'][pos] 
                region = (x-20, y-20, w + 50, h + 50)
                screenshot = robot.screenshot(region=region)
                screenshot_path = os.getcwd() + os.path.join('/screenshots', f'{keyword}_region{pos}.png')
                screenshot.save(screenshot_path)
                return screenshot_path
    return None


def get_email(text):
    email_structure = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    email = re.findall(email_structure, text)
    
    return email


def open_doc(doc, keywords):
    time.sleep(1)
    word_app = win32com.client.Dispatch('Word.Application')
    word_app.Visible = True

    for filename in os.listdir(doc):
        if filename.endswith('.docx') or filename.endswith('.doc'):
            path = os.path.join(doc, filename)
            document = word_app.Documents.Open(path)
            time.sleep(3)
            word_app.WindowState = 1

            
            word_window = gw.getWindowsWithTitle('Word')[0]
            word_window.activate()

            time.sleep(1)
            capture = capt_screen()

            for keyword in keywords:
                region = capt_region(capture, keyword)
                if region:
                    text = text_from_image(capture)
                    email = get_email(text)                   
                        # robot.write(f'nombre: {name}\n')
                        # robot.write(f'correo: {email}.')
                else:
                    print(f'no se encontro la palabra')
            
            if email:
                open = Open_app()
                open.open_text_edit()

            document.Close(False)
    word_app.Quit()

if __name__ == '__main__':
    path = os.getcwd() + '\docs'
    keywords = ['python', 'LabVIEW']
    open_doc(path, keywords)
