# Automatización y OCR Local

Se realizó un bot que es capaz de tomar decisiones, tales como aprobar o no el aspirante en base a conocer las aptitudes para un cargo en una empresa.   

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


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

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Dí cómo será ese paso_

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_

## Ejecutando las pruebas ⚙️

* Se ejecuta el main.py en el que van a aparecer una serie de opciones
Opciones:
    1. Agregar palabra clave
    2. Mostrar palabras clave
    3. Abrir Edge"
    4. Ejecutar bot"
    5. Salir

en la opcion 1 te va pedir las palabras clave que quieres que busque en las hojas de vida de los aspirantes.
En la opción 2 va a mostrar las palabras claves que se hayan ingresado.
En la opcion 3 va a abrir el navegador Microsoft Edge en la pagina de google.
En la opcion 4 va a ejecutar el bot el cual primeramente busca las hojas de vida en la carpeta, luego abre esos archivos .doc o .docx y toma una captura de la pantalla completa, posteriormente extrae el texto de esa captura para analizarlo y encontrar las palabras clave digitadas por el usuario y realizar otra captura pero ya en la zona donde esta la palabra clave y con eso tomar la decisión de guardar el correo del aspirante en un archivo de texto en la carpeta 'Aspirantes_aprobados' si es que encuentra las palabras clave en el archivo, si no se encuentran lo guardar en la carpeta 'Aspirantes_no_aprobados' para que ya el cliente tenga clasificados los aspirantes que mas se adecuan a la vacante.
En la opción 5 se sale y finaliza el programa.

En la carpeta 'PRUEBA' hay subcarpetas tales como:
- carpeta 'docs' que es donde se deben almacenar las hojas de vida que se quieren analizar.
- carpeta 'screenshots' que es donde se almacenan las capturas que realiza en las regiones donde se encuentran las palabras clave.
- carpeta 'Aspirantes_aprobados' que es donde se van a almacenar los correos de los aspirantes que cumplen con las aptitudes deseadas por la empresa.
- carpeta 'Aspirantes_no_aprobados' que es donde se almacenan los correos de los aspirantes que no cumplen con las aptitudes deseadas por la empresa. 


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
