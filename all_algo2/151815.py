import sys

wejsciowy = sys.argv[1]
wyjsciowy = sys.argv[2]
limit = sys.argv[3]

with open(wejsciowy, 'r') as f:
    n = int(f.readline().strip())
    zadania = []
    for i in range(n):
        linia = list(map(int, f.readline().strip().split()))
        linia.append(i + 1)  # Dodanie oryginalnego numeru zadania
        zadania.append(linia)

przypisania = [[] for _ in range(5)]
przypisania_1 = [[] for _ in range(5)]
czas_koncowy = [0] * 5  # Czas zakończenia ostatniego zadania każdego pracownika
czas_koncowy_1 = [0] * 5
opoznienia = 0
opoznienia_1 =0

zadania.sort(key=lambda x: x[-2])  # Sortuj po terminie zakonczenia

for zadanie in zadania:
    czasy = zadanie[:5]
    rj = zadanie[5]
    dj = zadanie[6]
    numer = zadanie[7]

    najlepszy_pracownik = None
    minimalny_czas = float('inf')

    for k in range(5):
        start = max(czas_koncowy[k], rj)
        koniec = start + czasy[k]
        if koniec < minimalny_czas:  # najmniejszy czas wykonania
            minimalny_czas = koniec
            najlepszy_pracownik = k

    przypisania[najlepszy_pracownik].append(numer)
    czas_koncowy[najlepszy_pracownik] = minimalny_czas

    if minimalny_czas > dj:
        opoznienia += 1

zadania.sort(key=lambda x: x[-3])  # Sortuj po terminie rozpoczecia

for zadanie in zadania:
    czasy_1 = zadanie[:5]
    rj_1 = zadanie[5]
    dj_1 = zadanie[6]
    numer_1 = zadanie[7]

    najlepszy_pracownik_1 = None
    minimalny_czas_1 = float('inf')

    for k in range(5):
        start_1 = max(czas_koncowy_1[k], rj_1)
        koniec_1 = start_1 + czasy_1[k]
        if koniec_1 < minimalny_czas_1:
            minimalny_czas_1 = koniec_1
            najlepszy_pracownik_1 = k

    przypisania_1[najlepszy_pracownik_1].append(numer_1)
    czas_koncowy_1[najlepszy_pracownik_1] = minimalny_czas_1

    if minimalny_czas_1 > dj_1:
        opoznienia_1 += 1

if(opoznienia<opoznienia_1):
    #print("opoznienia")
    with open(wyjsciowy, 'w') as f:
        f.write(f"{opoznienia}\n")
        for linia in przypisania:
            f.write(" ".join(map(str, linia)) + "\n")
else:
    #print("opoznienia2")
    with open(wyjsciowy, 'w') as f:
        f.write(f"{opoznienia_1}\n")
        for linia_1 in przypisania_1:
            f.write(" ".join(map(str, linia_1)) + "\n")

# print(f"Wynik zapisano do pliku {wyjsciowy}.")