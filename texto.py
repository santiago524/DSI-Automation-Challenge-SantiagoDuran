import pytesseract as tess
from PIL import Image
import pyautogui as robot
import os
import cv2 as cv
import time
import win32com.client
import pygetwindow as gw


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
                screenshot_path = os.path.join(os.getcwd(), '/screenshots', f'{keyword}_region{pos}.png')
                screenshot.save(screenshot_path)
                return data
    return None

def open_doc(doc, keywords):
    time.sleep(1)
    word_app = win32com.client.Dispatch('Word.Application')
    word_app.Visible = True

    for filename in os.listdir(doc):
        if filename.endswith('.docx') or filename.endswith('.doc'):
            path = os.path.join(doc, filename)
            document = word_app.Documents.Open(path)
            time.sleep(3)
            #robot.hotkey('alt', 'tab')
            # Maximiza la ventana de Word
            word_app.WindowState = 1  # Maximiza la ventana

            # Asegúrate de que la ventana de Word esté en el frente
            word_window = gw.getWindowsWithTitle('Word')[0]
            word_window.activate()

            time.sleep(1)
            capture = capt_screen()

            for keyword in keywords:
                region = capt_region(capture, keyword)
                print(region)
                if region:
                    print(f'capture completed')
                else:
                    print(f'no se encontro la palabra')

            document.Close(False)
    word_app.Quit()

if __name__ == '__main__':
    path = os.getcwd() + '\docs'
    keywords = ['hola']
    open_doc(path, keywords)
