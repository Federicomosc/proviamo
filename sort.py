def intersort(a):
    for i in range(1,len(a)):
        j=i
        while j > 0 and a[i-1] > a[i]:
            a[i], a[i-1] = a[i-1], a[i]
            j = j - 1


intersort([6, 8, 3, 2, 7, 6, 11, 5, 9, 4])


def serach (a, B):
    left = 0
    right =len(B)

    while left < right :
        middle = (left + right) // 2

        if B[middle] > a :
            right = middle

        elif B[middle] < a:
            left = middle +1
        else :
            return True
    return False

# Esempio di utilizzo:
B = [2, 4, 6, 8, 10]
print(serach(6, B))  # Dovrebbe restituire True se 6 è trovato
print(serach(5, B))  # Dovrebbe restituire False se 5 non è trovato


def merge_sort(A,B):
    X = []
    a = 0
    b = 0
    while a < len(A) and b < len(B):
        if A[a] < B[b]:
            X.append(A[a])
            a += 1
        else:
            X.append(B[b])
            b += 1
    return X

# Esempio di utilizzo:
A = [1, 3, 5, 7]
B = [2, 4, 6, 8]
print(merge_sort(A, B))  # Output atteso: [1, 2, 3, 4, 5, 6, 7, 8]





def merge_sort2(A,B):
    X = []
    a = 0
    b = 0
    while a < len(A) or b < len(B):
        if a < len(A) and (b >= len(B) or A[a] < B[b]):
            X.append(A[a])
            a += 1
        else:
            X.append(B[b])
            b += 1
    return X

A = [1 ,2, 3, 5, 7]
B = [2, 4, 6, 7, 8]
print(merge_sort2(A, B))  # Output atteso: [1, 2, 3, 4, 5, 6, 7, 8]


def merge_sort3 (a):
    if len(a) == 1:
        return a[:]
    
    m = len(a)//2
    l = merge_sort3(a[:m])
    r = merge_sort3(a[m:])
    return merge_sort2 (l,r)

print(merge_sort3([6, 8, 3, 2, 7, 6, 11, 5, 9, 4]))



def getMinDistance(self, nums, target, start):
        """
        :type nums: List[int]
        :type target: int
        :type start: int
        :rtype: int
        """
        x = 0
        for i in range(len(nums)):
            if nums[i] == target :
                x = i
                print(x)
                break
        return abs(x-start)
        

print(getMinDistance(0, [1,1,1,1,1,1,1,1,1,1], 1, 9))