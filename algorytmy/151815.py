import sys

wejsciowy = open(sys.argv[1], 'r')
wyjsciowy = sys.argv[2]
limit = sys.argv[3]
#wejsciowy = open('151815_1.txt', 'r')

n = int(wejsciowy.readline().strip())

pd_pairs = []
S = []

for _ in range(n):
    line = wejsciowy.readline().strip().split()
    p, d = int(line[0]), int(line[1])
    pd_pairs.append((p, d))

for _ in range(n):
    row = list(map(float, wejsciowy.readline().strip().split()))
    S.append(row)

wejsciowy.close()

#print(f"n = {n}")
#print("Pary (p, d):", pd_pairs)
#print("Macierz S:")
#for row in S:
#    print(row)



odwiedzone = [0] * n
odwiedzone_indeksy=[]
poprzednie_zadanie=min(pd_pairs, key=lambda x: x[0])
index_min = pd_pairs.index(poprzednie_zadanie)
odwiedzone_indeksy.append(index_min)
odwiedzone[index_min] = 1
Czas=poprzednie_zadanie[0]
#print(f"Wybrane zadanie: {poprzednie_zadanie}, Czas: {Czas}")

Y = 0

for i in range(1, n):  # kolejne n-1 zadań
    minimalny_czas = float('inf')
    wybrane_zadanie = None
    index_wybrane_zadanie = -1

    #przeszukaj zadania
    for j in range(n):
        if not odwiedzone[j]:  #nieodwiedzone
            p_j = pd_pairs[j][0]
            d_j = pd_pairs[j][1]
            czas_przezbrojenia = S[index_min][j]
            calkowity_czas_zadania = p_j + czas_przezbrojenia + Czas
            if calkowity_czas_zadania > d_j:
                calkowity_czas_zadania_kara=calkowity_czas_zadania+d_j #spoznione, kara
            else:
                calkowity_czas_zadania_kara=calkowity_czas_zadania #niespoznione, brak kary

            if calkowity_czas_zadania_kara < minimalny_czas:
                minimalny_czas = calkowity_czas_zadania_kara #do poszukiwania lepszej opcji
                min_czas_bez_kar = calkowity_czas_zadania #do przesuwania czasu
                wybrane_zadanie = pd_pairs[j]
                index_wybrane_zadanie = j

    C_j = min_czas_bez_kar
    p_j = wybrane_zadanie[0]
    d_j = wybrane_zadanie[1]
    Y_j = min(p_j, max(0, C_j - d_j))
    Y += Y_j

    odwiedzone[index_wybrane_zadanie] = 1  #odwiedz
    odwiedzone_indeksy.append(index_wybrane_zadanie) #dopisz do listy
    Czas = min_czas_bez_kar  #nowy czas
    index_min = index_wybrane_zadanie  #nowy poprzedni

    #print(f"Wybrane zadanie: {wybrane_zadanie}, Czas: {Czas}")

#print(f"Całkowite opóźnienie Y = {Y}")
#print("Odwiedzone indeksy:", odwiedzone_indeksy)

with open(wyjsciowy, 'w') as wynikowy:
    wynikowy.write(f"{Y}\n")
    wynikowy.write(" ".join(str(index + 1) for index in odwiedzone_indeksy) + "\n")

#print("Wyniki zostały zapisane do pliku 'wynik.txt'.")