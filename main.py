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

        opcion = input("Por favor digite una opción: ")

        if opcion == '1':
            palabra = input("Por favor digite una palabra clave: ")
            bot.add_keywords(palabra)
        elif opcion == '2':
            bot.show_keywords()
        elif opcion == '3':
            bot.open_edge()
        elif opcion == '4':
            path = os.getcwd() + '\docs'
            if bot.keywords_selected:
                bot.open_doc(path, bot.keywords_selected)
            else:
                print('¡No has digitado palabras clave!')
        elif opcion == '5':
            print("Hasta luego!!!")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")