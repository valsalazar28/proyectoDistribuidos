from Snake import main as snake
from Minesweeper import main as mine

def main():
    while True:
        print("Bienvenido al menú de juegos:")
        print("1. Jugar Snake")
        print("2. Jugar Buscaminas")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            snake()
        elif opcion == "2":
            mine()

        elif opcion == "3":
            print("¡Gracias por jugar!")
            break
        else:
            print("Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()