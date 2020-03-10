import itertools
import random
import time


def randomSet():
    #initialize the array
    set = []

    #set length of array
    length = 10

    #range of numbers
    numRange = 100
    
    #for loop append randomize numbers into array
    for i in range(length):
        r = random.randint(1, numRange)
        if r not in set: 
            set.append(r)
        else: 
            while r in set:
                r = random.randint(1, numRange)
            set.append(r)
    print(set)       
    return set



def validateSet(arr):
    #partition = []# partition stores the index where the numbers are added in the partition of the set
    sum = calculateSum(arr)
    

    #if the sum is divisible by 3, it can be divided into 3 partitions with equal sum
    if (sum % 3) == 0 :
        #print("sum: ", sum)
        return True
    else:
        #return false to loop and generate new set of random numbers
        return False

def calculateSum(arr):
    sum = 0
    #calculate sum of list
    for i in range (len(arr)):
        sum += arr[i] 
    return sum


def findRemainElem(arr, foundArr):
    remain = arr
    
    print("found Arr: ", foundArr)
    for i in range(len(foundArr)):
        remain.remove(foundArr[i])

    #print("remain: ", remain)
    return remain
    

def partitions(arr,sum):
    
    remainArr = []
    print("rA",remainArr)
    sumDivision = sum/3
    
    for i in range (len(arr)):
        #create combination of i(number) of elements
        part = list(itertools.combinations(arr,i))
        print("All partition",part)

        #loop through all combinations
        for j in range (int(len(part))):       
            if (calculateSum(part[j]) == sumDivision):
                print("part j",part[j])
                remainArr = findRemainElem(arr,part[j])
                return remainArr

       
        if (remainArr != []):
            return remainArr

def beginSearch(arr, sum):
    #find first partition
    remainFirst = partitions(arr,sum)
    print(remainFirst)

    #find 2nd partition
    if(remainFirst != [] and remainFirst != None):
        remainSecond = partitions(remainFirst,sum)
        if(remainSecond != [] and remainSecond != None):
            print("found: ", remainSecond)
            return remainSecond
        else:
           return False

def main():
    #initialize var to store starting time
    t = time.perf_counter_ns()

    valid = False
    result =[]
       
    while (valid == False):
        arr = []

        #get set from randomSet function
        arr = randomSet()

        sum = calculateSum(arr)

        #print out array
        print("set: ", arr)
        
        #validate set if can be divided by 3
        validSet = validateSet(arr)

        print("valid set: ", validSet)

        if(validSet != False):
            t = time.perf_counter_ns()
            
            result = beginSearch(arr, sum)
            if(result != [] and result != None and result != False):
                valid = True
        
                
    if(result != [] and result != None and result != False):
        print("Partition found!")
    else:
        print("Partition not found!")
        
    end_time = time.perf_counter_ns()
    elapsed_time = (end_time - t)

    print("\n----------------------------------------------")
    print("time: ", (elapsed_time/1000000), "\n")
    print("----------------------------------------------\n")
    
    f = open("Range.txt", "a+")
    #f.write(str(elapsed_time/1000000)+"\n")
    f.close()

loop = 20

for i in range (loop):
    #main()
    randomSet()

