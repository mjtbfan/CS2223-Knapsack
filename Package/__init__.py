# Nicholas Delli Carpini | 12/05/17
from time import perf_counter
import itertools
from itertools import combinations

# Converts the 2 lists read from the input file into a single tuple in the form (#, weight, value)
def itemTuple(weights, values):
    items = []
    for i in range(0, len(weights)):   
        items.append((i, weights[i], values[i]))
    return items
# Opens the file and builds 2 lists | Catches any errors when trying to open / converting to ints
def openFile(name):
    if (name == ""):
        name = "input.txt"
    try:
        with open (name) as f:                               
            try:
                inputFile = f.readlines()
                if (len(inputFile) != 3):
                    f.close()
                    print("Error: Input File is Invalid, Please Check that the Input is in the Form")
                    print("\nCarry Capacity\nweight1,weight2,weight3...\nvalue1,value2,value3...")
                    return 0
                mweight = int(inputFile[0])
                weights = []
                values = []
                weightsTemp = inputFile[1].split(",")
                for i in range(0, len(weightsTemp)):
                    weights.append(int(weightsTemp[i]))
                valuesTemp = inputFile[2].split(",")
                for j in range(0, len(valuesTemp)):
                    values.append(int(valuesTemp[j]))
                for k in range(0, len(weights)):
                    if (mweight < 0 or weights[k] < 0 or values[k] < 0):
                        print("Error: No Negative Values Allowed, Please Check the Input File")
                        return 0
                if (i != j):
                    print("Error: Not Every Object has its own Weight/Value, Please Check the Input File")
                    return 0
            except (ValueError, SyntaxError) as error:       
                f.close()
                print("Error: Input File is Invalid, Please Check that the Input is in the Form")
                print("Carry Capacity\nweight1,weight2,weight3...\nvalue1,value2,value3...")
                return 0
            f.close
            return mweight, itemTuple(weights, values)
    except FileNotFoundError:
        print("Error: File Not Found, Please Type the Correct Name / Make Sure the File is in the Same Folder as this File")
        return 0

# Prints the greeting an continually loops until the user gives it a valid file
def inputStatement():
    print("Welcome to the Knapsack Problem - Solved 3 Ways")
    print("Please Put Your Input File in the Same Folder as this .py File")
    print("What is the Exact Name of Your Input File?")
    print("(If the File is name 'input.txt', Just Press Enter)")

    name = input()
    
    while True:
        if (openFile(name) == 0):
            name = None
            name = input()
            continue
        else:
            points = openFile(name)
            return points
        
# Gets all possible combinations of items in the knapsack | Taken from stackoverflow
def makePowerset(items):
    x = list(items)
    return list(itertools.chain.from_iterable(combinations(x, i) for i in range(1, len(items) + 1)))

# Exhaustive Search 
def exhaustSearch(mweight, items):
    itemSet = ()
    weightArray = []
    maxValue = 0
    powerset = makePowerset(items)
    for i in range(0, len(powerset)):
        tempSize = 0
        for j in range(0, len(powerset[i])):
            tempSize += powerset[i][j][1]
        if (tempSize <= mweight):
            itemSet = itemSet + (powerset[i],)
            weightArray.append(tempSize)
    for k in range(0, len(itemSet)):
        tempValue = 0
        for l in range(0, len(itemSet[k])):
            tempValue += itemSet[k][l][2]
        if (tempValue > maxValue):
            maxValue = tempValue
            bestItems = itemSet[k]
    return maxValue, bestItems

# Dynamic Programming
def dynamic(mweight, items):
    bestItems = ()
    tempWeight = mweight
    length = len(items)
    dTable = [[0 for x in range(0, mweight + 1)] for x in range(0, length + 1)] 
    for k in range(0, length + 1):
        for l in range(0, mweight + 1):
            if (k == 0 or l == 0):
                dTable[k][l] = 0
            else:
                if (items[k - 1][1] <= l):
                    dTable[k][l] = max(items[k - 1][2] + dTable[k - 1][l - items[k - 1][1]], dTable[k - 1][l])
                else:
                    dTable[k][l] = dTable[k - 1][l]
    for m in range(length, 0 , -1):
        inD = dTable[m][tempWeight] != dTable[m - 1][tempWeight]
        if inD:
            bestItems = bestItems + (items[m - 1],)
            tempWeight -= items[m - 1][1]
    return dTable[length][mweight], bestItems

# Greedy Algorithm
def greedy(mweight, items):
    maxVal = 0
    tempWeight = mweight
    bestItems = ()
    weightVal = sorted(items, key=lambda tup: tup[1] / tup[2])
    for tup in weightVal:
        if (tempWeight >= tup[1]):
            bestItems = bestItems + (tup,)
            tempWeight -= tup[1]
            maxVal += tup[2]
    return maxVal, bestItems

# Prints the time in a more readable format using shorthand units and only 2 decimal places   
def printTime(ans): 
    if (ans > 1e-02):
        print ("Time: %.2f" % ans, "s")
    if (ans <= 0.01 and ans > 0.00001):
        ans = ans * 1000
        print ("Time: %.2f" % ans, "ms")
    if (ans <= 0.00001 and ans > 0.00000001):
        ans = ans * 1000000
        print ("Time: %.2f" % ans, "\u00B5s")
    if (ans <= 0.00000001):
        ans = ans * 1000000000
        print ("Time: %.2f" % ans, "ns")

# Prints the final results
def printResults(mweight, items):
    print("\nInput Max Weight:", mweight)
    print("Input Items:")
    print("%5s" % "Item" + "%8s" % "Weight" + "%8s" % "Value" )
    for i in range(0, len(items)):
        print("%5s" % items[i][0] + "%8s" % items[i][1] + "%8s" % items[i][2])
    
    print("\nUsing Exhaustive Search")
    start = perf_counter()
    maxValue, bestItems = exhaustSearch(mweight, items)          
    end = perf_counter()        
    time = end - start          
    printTime(time)
    sortBest = sorted(bestItems, key=lambda tup: tup[0])
    print("Max Value:", maxValue)
    print("Best Items:")
    print("%5s" % "Item" + "%8s" % "Weight" + "%8s" % "Value" )
    for j in range(0, len(bestItems)):
        print("%5s" % sortBest[j][0] + "%8s" % sortBest[j][1] + "%8s" % sortBest[j][2])
        
    print("\nUsing Dynamic Programming")
    start = perf_counter()
    maxValue, bestItems = dynamic(mweight, items)          
    end = perf_counter()        
    time = end - start          
    printTime(time)
    sortBest = sorted(bestItems, key=lambda tup: tup[0])
    print("Max Value:", maxValue)
    print("Best Items:")
    print("%5s" % "Item" + "%8s" % "Weight" + "%8s" % "Value" )
    for k in range(0, len(bestItems)):
        print("%5s" % sortBest[k][0] + "%8s" % sortBest[k][1] + "%8s" % sortBest[k][2])
    
    print("\nUsing Greedy Algorithm")
    start = perf_counter()
    maxValue, bestItems = greedy(mweight, items)          
    end = perf_counter()        
    time = end - start          
    printTime(time)
    sortBest = sorted(bestItems, key=lambda tup: tup[0])
    print("Max Value:", maxValue)
    print("Best Items:")
    print("%5s" % "Item" + "%8s" % "Weight" + "%8s" % "Value" )
    for l in range(0, len(bestItems)):
        print("%5s" % sortBest[l][0] + "%8s" % sortBest[l][1] + "%8s" % sortBest[l][2])

mweight, items = inputStatement()
printResults(mweight, items)
input("\nPress Enter to Exit")