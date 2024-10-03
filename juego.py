import random

def adivina_el_numero():
    print("¡Bienvenido al juego de adivinanza de números!")
    numero_secreto = random.randint(1, 999)
    intentos = 0

    while True:
        intento = int(input("Adivina el número (entre 1 y 999): "))
        intentos += 1

        if intento < numero_secreto:
            print("Demasiado bajo. Intenta de nuevo.")
        elif intento > numero_secreto:
            print("Demasiado alto. Intenta de nuevo.")
        else:
            print(f"¡Felicidades! Adivinaste el número en {intentos} intentos.")
            break

adivina_el_numero()
