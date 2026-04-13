def algo_x(A,x):
    i = len(A) - 1
    j = 0
    while i >= 0:
        if j == i:
            j = 0
            i = i - 1
        elif A[i] - A[j] > x or A[j] - A[i] > x:
            return True
        else:
            j = j + 1
    return False

print(algo_x([6, 8, 3, 2, 7, 6, 11, 5, 9, 4], 5))



def algo_x(A,k):
    B = algo_y(A,0,len(A))
    c = 0
    for i in range(len(B)):
        if i < k:
            c = c + B[i]
        else:
            return c
    return c

def algo_y(A,i,j):
    D = []
    if j - i == 1:
        D.append(A[i])
    elif j - i > 1:
        k = (i + j)//2
        B = algo_y(A,i,k)
        C = algo_y(A,k,j)
        b = 0
        c = 0
        while b < k - i or c < j - k:
            if c >= j - k or (b < k - i and B[b] < C[c]):
                D.append(B[b])
                b = b + 1
            else:
                D.append(C[c])
                c = c + 1
    return D





def bst_lower_bound_dict(root, x):
    result = None
    current = root
    
    while current is not None:
        if current["key"] == x:
            return current            # Trovato il limite perfetto
        elif current["key"] > x:
            result = current          # Candidato valido, lo memorizziamo
            current = current["left"] # Cerchiamo a sinistra
        else:
            current = current["right"]# Valore troppo piccolo, cerchiamo a destra
            
    return result


albero = {
    "key": 10,
    "left": {
        "key": 5,
        "left": None,
        "right": None
    },
    "right": {
        "key": 15,
        "left": None,
        "right": None
    }
}

x = 8
nodo_trovato = bst_lower_bound_dict(albero, x)

if nodo_trovato:
    print(f"Il lower bound di {x} è {nodo_trovato['key']}")
else:
    print(f"Nessun valore maggiore o uguale a {x} trovato.")

def second_minimum(a):
    min = a[0]
    min_2 =a[0]
    for i in range(len(a)-1):
        if a[i] < min:
            min_2 = min
            min = a[i]

        elif a[i] < min_2 and a[i] != min:
            min_2 = a[i]

    return min, min_2

print(second_minimum([6, 8, 3, 2, 7, 6, 11, 5, 9, 4]))