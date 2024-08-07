# Automatización y OCR Local

Se realizó un bot que es capaz de tomar decisiones, tales como aprobar o no el aspirante en base a conocer las aptitudes para un cargo en una empresa.   

### Pre-requisitos 📋

you should have to need this libraries:
- pytesseract
- pyutogui
- win32com
- Open_CV

```
pip install + #Librarie's name
```

### Instalación 🔧

Esta función me abre el navegador Microsoft Edge y utilizando la imagen 'bar.png' dentro de la carpeta principal 'PRUEBA' para encontrar la barra de busquedad, hacer click, y buscar la pagina principal de google.

```
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
```

Esta función me abre el editor de texto.
```
def open_text_edit(self):
        os.system('start notepad')
        time.sleep(0.5)
```

Esta función le hace una captura de pantalla completa y la guarda en la carpeta principal 'PRUEBA'.
```
def capt_screen():
        screenshot = robot.screenshot()
        screenshot_path = os.path.join(os.getcwd(), 'screen.png')
        screenshot.save(screenshot_path)
        return screenshot_path
```

Esta función utiliza la libreria Open_CV para cargar la captura que realizo anteriormente y extrae el texto de esa imagen con la libreria pytesseract.
```
def text_from_image(capture):
        capt = cv.imread(capture)
        txt = tess.image_to_string(capt)
        return txt
```

Esta función encuentra la posición en la que se encuentra la palabra clave a buscar en el texto que se extrajo de la captura.
```
def position_keyword(keyword, txt):
        lines = txt.split('\n')
        for position, line in enumerate(lines):
            if keyword.lower() in line.lower():
                return position, line.lower().index(keyword.lower())
        return None, None
```

Esta función en base a la posición que me devuelve la anterior me toma una captura de la región donde se encuentra la palabra clave y me la guarda en la carpeta 'screenshots'.
```
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
```

Esta función le pide al usuario que ingrese las palabras claves a buscar y las almacena en una lista.
```
def add_keywords(self, palabra):
        self.keywords_selected.append(palabra)
        print(f'Palabra clave "{palabra}" agregada a la lista.')
```

Esta función me obtiene el correo del aspirante en la hoja de vida.
```
def get_email(text):
        email_structure = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_structure, text)
        return emails
```

Esta función es la que recorre por la carpeta donde estan almacenadas todas las hojas de vida, las abre y llama a las demás funciones para realizar toda la tarea de analizar si el aspirante cumple con las condiciones o no para el trabajo.
```
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

```

## Ejecutando las pruebas ⚙️

* El programa main.py presenta un menú con las siguientes opciones:

- Agregar Palabra Clave: Permite al usuario ingresar palabras clave que desea buscar en las hojas de vida de los aspirantes.
- Mostrar Palabras Clave: Muestra las palabras clave que se han ingresado.
- Abrir Edge: Abre el navegador Microsoft Edge en la página de Google.
    En la carpeta principal hay una imagen llamada 'bar.png', esta es una imagen de la barra de busqueda del navegador. Con esta imagen el bot busca similitudes en el navegador abierto y le da click realizando asi la busqueda de la pagina principal de google.
- Ejecutar Bot: Ejecuta un bot que realiza las siguientes tareas:
    Busca las hojas de vida en la carpeta especificada.
    Abre los archivos .doc o .docx y toma una captura de la pantalla completa.
    Extrae el texto de la captura y analiza las palabras clave ingresadas por el usuario.
    Toma una captura de la región donde se encuentra la palabra clave.
    Si se encuentra la palabra clave, guarda el correo del aspirante en un archivo de texto en la carpeta Aspirantes_aprobados. Si no se encuentran las palabras clave, guarda el correo en la carpeta Aspirantes_no_aprobados para que el cliente tenga clasificados los aspirantes que más se adecuan a la vacante.
- Salir: Finaliza el programa.


* En la carpeta 'PRUEBA', se encuentran las siguientes subcarpetas:

- 'docs': Almacena las hojas de vida que se desean analizar.
- 'screenshots': Almacena las capturas realizadas en las regiones donde se encuentran las palabras clave.
- 'Aspirantes_aprobados': Almacena los correos de los aspirantes que cumplen con las aptitudes deseadas por la empresa.
- 'Aspirantes_no_aprobados': Almacena los correos de los aspirantes que no cumplen con las aptitudes deseadas por la empresa.


## Construido con 🛠️

* [pytesseract](https://pypi.org/project/pytesseract/) - an optical character recognition (OCR) tool for python
* [pyutogui](https://pypi.org/project/PyAutoGUI/) - cross-platform GUI automation Python module for human beings
* [win32com](https://pypi.org/project/pywin32/) - This is the readme for the Python for Win32 (pywin32) extensions
* [Open_CV](https://pypi.org/project/opencv-python/) - Library for computer vision tools

## Autores ✒️

* **Santiago Duran** - [santiago524](https://github.com/santiago524)

## Licencia 📄

README is available under the MIT license. See the LICENSE file for more info.

---
⌨️ by [santiago524](https://github.com/santiago524)
