def classify_triangle(a,b,c):
    # it is convenient to first sort the three lengths, A, B, and C,
    # so that we can refer to the maximal length as a
    if b > a:
        a, b = b, a             # swap a <==> b
    if c > a:
        a, c = c, a             # swap a <==> c

    if a > b + c:
        print ('impossible')
    else:
        if a*a > b*b + c*c:
            angle = 'obtuse'
        elif a*a < b*b + c*c:
            angle = 'acute'
        else:
            angle = 'right'
        if a == b and b == c:
            sides = 'equilateral'
        elif a == b or b == c or a == c:
            sides = 'isosceles'
        else:
            sides = 'scalene'
        print (angle, sides)

classify_triangle(5,5,7)


def minimum(a):
    counter = 1000000000
    for i in range(len(a)):
        if counter > a[i]:
            counter = a[i]
    print (counter)

minimum([100,2,55,4,3,2,67,3])
minimum([7])

def count_lower(a, b):
    counter = 0
    for i in range(len(a)):
        if a[i] < b:
            counter += 1
    print(counter)

count_lower([3, 2, 1, 1, 3, 2, 2, 3, 1], 2)


def multiples_of_three(a):
    counter = 0
    for i in range(len(a)):
        if a[i] % 3 == 0:
            counter += 1
    print(counter)


multiples_of_three([34, 31, 45, 5, 38, 19, 19, 26, 25, 19, 39, 40])


def check_sorted (A):
    for i in range(1,len(A)):
          if A[i] < A[i-1]:
              return False
    return True

print(check_sorted([43,51,50,51,70]))


def is_monotonic(a , i, j ):
    cmp = True
    sequence = []
    for f in range(len(a)):
        if f < i:
            continue
        if f >= i and f <= j:
            sequence.append(a[f])
        else :
            continue
    
    for i in range(1,len(sequence)):
          if sequence[i] >= sequence[i-1]:
              continue
          else:
              cmp = False
              break
    print(sequence)
    print(cmp)

is_monotonic([1,1,1,2,1,3], 0, 5)


def find_peak(a):

    for i in range(1, len(a)):
        
        if a[i] < a[i-1]:
            print(a[i-1])
            return
            
    print(a[-1])

find_peak([1, 2, 3, 2, 1]) 
find_peak([1, 2, 3, 4])  

def log_base_two(a):
    n =0
    while 2**n < a:
        n +=1 
    print(n-1)

log_base_two(1000)
log_base_two(5)

def maximal_difference(a):
    if len(a) <= 1:
        print(0)
        return  

    lowest = a[0]
    maximum = a[0]

    for i in range(1, len(a)):  
        
        if a[i] <= lowest:
            lowest = a[i]
    
        if a[i] >= maximum:
            maximum = a[i]
            
    print(maximum - lowest)

maximal_difference([2, 1, 5, 9, 4, 10, 8])


def minimal_sum(a, x):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    if sum < x:
        print (False)
    else:
        print(True)

minimal_sum([32,-3,10,7,-4,18,25], 94)
minimal_sum([3, 2], 4)



def isolated_elements(a):

    for i in range(1, len(a)-1):
        if a[i-1] != a[i] and i==1:
            print (a[i-1])
        if a[i-1] == a[i] == a[i+1]:
            continue
        else:
            print(a[i])

isolated_elements([2, 2, 3, 2, 3])


def repeated_adjacent_elements(a):
    for i in range(1, len(a)):
        if a[i] == a[i-1]:

            if i == 1 or a[i] != a[i-2]:
                print(a[i])


repeated_adjacent_elements([1, -1, 7, 7, -1, 7, 1, 7, 7, 7, 7, 2, 2])

