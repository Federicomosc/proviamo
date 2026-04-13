def array_remove_pos(A,i):
    if i < 0 or i >= len(A):
        return A
    
    A[i] = A[-1]
    A.pop() 
    print(A)
def array_remove_value(A, x):
    write_index = 0
    
    for i in range(len(A)):
        
        if A[i] != x:
            A[write_index] = A[i]
            write_index += 1

    while len(A) > write_index:
        A.pop()

mia_lista = [3, 2, 2, 3, 4, 3, 5]
valore_da_rimuovere = 3

array_remove_value(mia_lista, valore_da_rimuovere)
print(mia_lista)


def pi(n):
    S = [True]*(n + 1)
    S[0] = False
    S[1] = False
    p = 2
    while p * p <= n:
        if S[p]:
            i = p * p
            while i <= n:
                S[i] = False
                i = i + p
        p = p + 1

    count = 0
    i = 1
    while i <= n:
        if S[i]:
            count = count + 1
        print (i, count)
        i = i + 1

pi(10)


def histogram(a):
    for i in range(len(a)):
        print("#" * a[i])

histogram([1,3,6,8,12])

def histogram_ver(a):
    max=0
    min=0
    for i in range(len(a)):
        if a[i] >= max:
            max = a[i]
        if a[i] <= min:
            min = a[i]
    line = []

    for h in range(max,0, -1):
        for i in range(len(a)):
            if a[i] >= h:
                line.append("#")
            else:
                line.append(" ")
        print("".join(line))
        line = []
    print("-" * len(a))

    for o in range(-1, min-1, -1):
        for i in range(len(a)):
            if a[i] <= o :
                line.append("#")
            else:
                line.append(" ")
        print("".join(line))
        line = []
histogram_ver([7, 3, -2, 10, 5, -3, 3, 5, 8 ])


def repetition(a):
    counter =1
    for i in range(1, len(a)):
        if a[i] == a[i-1]:
            counter += 1
        if a[i] != a[i-1]:
            if counter >= 3:
                print(a[i-1], " * ", counter)
                counter =1
            else:
                print(a[i-1])


repetition([-1, 1, 1, 1, 7, 7, 7, 7, 5, 5, 1, 1, 4, 1])


def leng (A):
    if len(A) >= 1:
        i = 0
        j = 1
        best = A[0]
        best_len = 1
        while j < len(A):
            if A[i] != A[j]:
                i = j            
            j = j + 1
            if j - i > best_len:
                best = A[i]
                best_len = j - i

        print(best)

leng([8, -2, 3, 3, 4, 4, 4, 2, 2, 2, 3, -2, 3, 3, 3, 3, 4, 4, 4, 8, 2, 2, 8, 2, 2, 22, 2, 22, 22, 2, 2, 22, 8])




