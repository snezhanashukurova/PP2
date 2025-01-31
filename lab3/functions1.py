# 1
def ounces(grams):
     return 28.3495231 * grams


grams=float(input())
print(ounces(grams))



# 2

def centigrade(F):
     return (5 / 9) * (F - 32)

F=int(input())
print(centigrade(F))

# 3

def puzzle(heads, legs):
     rabbits = int((legs - 70)/2)
     chickens = int(head - rabbits)
     return rabits, chickens
heads = int(input())
legs=int(input())

print(puzzle(heads, legs))


# 4
def filter(list):
    result = []
    for i in list:
        count=0
        for j in range(1, i+1):
            if(i%j==0):
                count += 1

        if(count==2):
            result.append(i)

    return result
                
a=[1,2,4,7,8]

print(filter(a))


# 5

from itertools import permutations
def permut(string):
    p=permutations(string)
    print(list(p))

a=str(input())
permut(a)
