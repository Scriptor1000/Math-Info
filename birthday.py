import math

probality_of_collision = lambda k: 1 - math.factorial(365) / (math.factorial(365 - k) * 365 ** k) 

while True:
    while not (i := input("Anzahl der Personen: ")).isnumeric():
        print("Bitte geben Sie eine gültige Zahl ein.")
    if (i == "0"):
        print("Programm wird beendet.")
        break
    k = int(i)
    print(f"Die Wahrscheinlichkeit, dass mindestens zwei Personen am selben Tag Geburtstag haben, beträgt: {probality_of_collision(k) * 100:.2f}%\n")
