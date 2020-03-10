import copy
import random
import time

#----------------------------------------------------------------------------
#       GENERATE ARRAY
#----------------------------------------------------------------------------

def randomSet():
    list=[]
    length = 18
    lowerBound = 0
    upperBound =  200
    for x in range(length):
        list.append(random.randint(lowerBound,upperBound))
    return list


def validateSet(arr):
    #partition = []# partition stores the index where the numbers are added in the partition of the set
    sum = calculateSum(arr)

    #if the sum is divisible by 3, it can be divided into 3 partitions with equal sum
    if (sum%3) == 0 :
        #print("sum: ", sum)
        return True
    else:
        #return false to loop and generate new set of random numbers
        return False


def initialiseArr():
    while True:
        list = randomSet()
        if (validateSet(list) == True):
            break
    return list


#----------------------------------------------------------------------------
#   GREEDY METHOD
#----------------------------------------------------------------------------

def greedy(arr):
    A = []
    B = []
    C = []

    #sort the numbers
    for i in sorted(arr, reverse = True):
        #put i into the smallest sum partition set
        if calculateSum(A) <= calculateSum(B) and calculateSum(A) <= calculateSum (C):
            A.append(i)
        elif calculateSum(B) < calculateSum(A) and calculateSum(B) <= calculateSum(C):
            B.append(i)
        elif calculateSum(C) < calculateSum(A) and calculateSum(C) < calculateSum(B):
            C.append(i)
       
    return (A, B, C)

#Find the set that has the smallest difference
#Find the two sets that have larger differences 
def getSwapSet(diffA, diffB, diffC, A, B, C):
    tempArr = [0, 1, 2]

    if (diffA < diffB) and (diffA < diffC):
        remainSet = 0
    elif (diffB < diffA) and (diffB < diffC):
        remainSet = 1
    else:
        remainSet = 2

    tempArr.remove(remainSet)
    swapSet_1 = tempArr[0]
    swapSet_2 = tempArr[1]
    

    return (swapSet_1, swapSet_2, remainSet)



#----------------------------------------------------------------------------
#   LOCAL SEARCH METHOD
#----------------------------------------------------------------------------

#A, B are the selected sets to be swapped with their elements
#swap the numbers until solution is found, if not, elements are randomly swapped
#to increase probability to find better solution
def localSearch(A, B, pV):
    
    betterA = []
    betterB = []

    
    diffA = abs(pV - calculateSum(A))
    diffB = abs(pV - calculateSum(B))

    
    for h in range(3):

        #on 2nd loop: smallest element in B is added to A
        if h == 1 and abs(pV - calculateSum(A)) != 0:
            minIndex = 0
            for k in range(len(B)):
                if k == 0:
                    min = B[k]
                elif min > B[k]:
                    min = B[k]
                    minIndex=k

            A.append(B[minIndex])
            B.remove(B[minIndex])
            

        #on 3rd loop: 2 smallest elements of A are added to B
        if h == 2:
            for m in range(2):
                minIndex = 0
                for k in range(len(A)):
                    if k == 0:
                        min = A[k]
                    elif min > A[k]:
                            min = A[k]
                            minIndex = k
                
                B.append(A[minIndex])
                A.remove(A[minIndex])

        #swap B elements with A elements one by one to find best solution
        #return when one or both of (A,B) has 0 difference with sum//3(pV)
        #return value: found best A and B, True = solution found, False = solution not found yet
        for i in range(len(A)):
            for j in range(len(B)):
                temp = A[i]    
                A[i] = B[j]
                B[j] = temp

                if pV == calculateSum(A) and pV == calculateSum(B): #A, B is zero found solution
                    return A, B, True
                    break

                elif pV == calculateSum(A) or pV == calculateSum(B): #found zero 
                    return A, B, False
                    break

                elif abs(pV - calculateSum(A)) < diffA or abs(pV - calculateSum(B)) < diffB: #better solution
                     
                    betterA = []
                    betterB = []
                    betterA.extend(A)
                    betterB.extend(B)

                    diffA = abs(pV - calculateSum(A))
                    diffB = abs(pV - calculateSum(B))
                    
                else:
                    B[j] = A[i] #no change 
                    A[i] = temp

    #return if better solutions are found
    if len(betterA) > 0:
        if betterA is not None:
            return betterA, betterB, False
    else:#if after local search, better solution not found
        #add back 2 smallest elements from B to A
        minIndex = 0
        for k in range(len(B)):
            if k == 0:
                min = B[k]
            elif min > B[k]:
                min = B[k]
                minIndex = k
                       
        A.append(B[minIndex])
        B.remove(B[minIndex])

        #since there is no better solution found, randomly swap between TWO numbers
        #numbersToChange = number of times to swap between two numbers
        numbersToChange = random.randint(0, len(A))

        for i in range (numbersToChange):
            numToAppend = random.randint(0, len(B)-1)#so that it randoms in array index
            numToRemove = random.randint(0, len(A)-1)#so that it randoms in array index

            A.append(B[numToAppend])
            B.remove(B[numToAppend])

            B.append(A[numToRemove])
            A.remove(A[numToRemove])
 
        return A, B, False



#----------------------------------------------------------------------------
#   SUPPORTING METHODS
#----------------------------------------------------------------------------

#calculate sum of the given array
def calculateSum(arr):
    sum = 0
    #calculate sum of list
    for i in range (len(arr)):
        sum += arr[i]
    return sum

def accuracy(a,b,c,pV):
  accA = 100 - (a*100 / pV)
  accB = 100 - (b*100 / pV)
  accC = 100 - (c*100 / pV)
  acc = (accA + accB + accC)/3
  acc = str(round(acc, 2))
  
  return acc



#----------------------------------------------------------------------------
#   MAIN FUNCTION
#----------------------------------------------------------------------------
def main():
    
    #loop for sets of different array
    numOftest = 50

    #loop for localSearch
    numOfchances = 99

    f = open("RangeAcc.txt", "a+")
    #duration=0
    
    for i in range(numOftest):
        setArr = []
        bestSetArr = []
        best_diff = 0
        f = open("RangeAcc.txt", "a+")
        #generate array
        arr = initialiseArr()
        print(arr)

        #initialize var to store starting time
        start = time.perf_counter_ns()
        
        #use greedy algo to get partitions
        A, B, C = greedy(arr)
        
        setArr = [A, B, C]
        print(setArr)
        #get the difference of each set (difference from the sum//3)
        sum = calculateSum(arr)
        print("Sum of initial set =", sum)
        pV = sum//3
        print("Partition Value :", pV)
            
        #get difference of each partition set based on sum//3
        diffA = abs(pV - calculateSum(A))
        diffB = abs(pV - calculateSum(B))
        diffC = abs(pV - calculateSum(C))
        difference = diffA+diffB+diffC
        
        #if all difference in all sets are set, return found
        if(difference == 0):
            print("Exact Solution found: " , setArr)
            print("Sum of A:",calculateSum(A),";","Sum of B:",calculateSum(B),";","Sum of C:",calculateSum(C) )
            Accuracy = accuracy(diffA ,diffB , diffC, pV)
            print("Accuracy:", Accuracy,"%")
            f.write(Accuracy+"\n")

        else:
            #loop 100 times until best solution is found
            for n in range(numOfchances):
                #get sets that will be swapped between their elements
                #getSwapSet returns the INDEX of the setArr, to keep track which sets are used to swapped
                
                #print("setArr=",setArr)

                #Make a copy of the list
                bestSetArr = copy.deepcopy(setArr)
                swapSet1, swapSet2, remainSet = getSwapSet(diffA, diffB, diffC, A, B, C)

                #local search
                setArr[swapSet1], setArr[swapSet2], found = localSearch(setArr[swapSet1], setArr[swapSet2], pV)
                #print("swapset=",setArr)

                #record difference of the set that gone through local search
                newdiffA = abs(pV - calculateSum(setArr[swapSet1]))
                newdiffB = abs(pV - calculateSum(setArr[swapSet2]))
                newdiffC = abs(pV - calculateSum(setArr[remainSet]))
                newdifference = newdiffA + newdiffB + newdiffC
                    
                #print("diff=",difference)
                #print("newdiff=",newdifference)

                #If the local search set has a smaller difference than the original set,
                #the local search set will be taken as the best solution
                if newdifference<difference:
                    bestSetArr = copy.deepcopy(setArr)
                    A,B,C = bestSetArr[0], bestSetArr[1], bestSetArr[2]
                    diffA = newdiffA
                    diffB = newdiffB
                    diffC = newdiffC
                    difference = newdifference
                    

                #Else the set remains the same
                else:
                    setArr = copy.deepcopy(bestSetArr)
                        
                #print("bestSetArr=",bestSetArr)

                #If the differences of the set and the target value is 0,
                #terminate this algorithm,else continue to loop
                if found == True:
                    print("Exact Solution found: " , bestSetArr)
                    print("Sum of A:",calculateSum(A),";","Sum of B:",calculateSum(B),";","Sum of C:",calculateSum(C) )
                    Accuracy = accuracy(diffA ,diffB , diffC, pV)
                    print("Accuracy:", Accuracy,"%")
                    f.write(Accuracy+"\n")
                    break

            #After looping, the differences between the set and the target value is still unable to reach 0,
            #print out the best solution
            if found == False:
                print("Best solution found: ", bestSetArr)
                print("Sum of A:",calculateSum(bestSetArr[0]),";","Sum of B:",calculateSum(bestSetArr[1]),";","Sum of C:",calculateSum(bestSetArr[2]) )
                #print(diffA)
                #print(newdiffA)
                Accuracy = accuracy(diffA ,diffB , diffC, pV)
                print("Accuracy:", Accuracy,"%")
                f.write(Accuracy+"\n")

            print("final=",difference)

        #Calculate duration
        end = time.perf_counter_ns()
        partition_duration = (end - start)
        print("Partition Duration=",partition_duration/1000000)
        elapsed_time = partition_duration
        
        print("\n----------------------------------------------")
        print("Time: ", (elapsed_time/1000000), "\n")
        print("----------------------------------------------\n")
        
        #f.write(str(elapsed_time/1000000)+"\n")
        f.close()
    
main()
