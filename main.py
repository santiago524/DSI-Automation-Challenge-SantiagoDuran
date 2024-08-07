from functions import *


if __name__ == "__main__":
    bot = Analysis()
    
    while True:
        print("\nOpciones:")
        print("1. Agregar palabra clave")
        print("2. Mostrar palabras clave")
        print("3. Abrir Edge")
        print("4. Ejecutar bot")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            palabra = input("Ingresa la palabra clave: ")
            bot.agregar_palabra_clave(palabra)
        elif opcion == '2':
            bot.mostrar_palabras_clave()
        elif opcion == '3':
            bot.abrir_edge()
        elif opcion == '4':
            bot.abrir_bloc_de_notas()
        elif opcion == '5':
            nombre_doc = input("Ingresa el nombre del documento (con extensión): ")
            bot.navegar(nombre_doc)
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")