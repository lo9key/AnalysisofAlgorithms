<<<<<<< HEAD
import sys, re, time
=======
#!/usr/bin/python
'''
	CS 325 - Implementation 2
		Sequence alignment via dynamic programming

	Kyle Prouty, Levi Willmeth, Andrew Morrill
	Winter 2017
'''

import sys, re
>>>>>>> 0404bc8bdd747e9a9d205a4781cff61271b9bce3

DEBUGGING = False

costFile = 'imp2cost.txt'
seqFile = 'imp2input.txt'
outFile = 'imp2output.txt'

def readInputFile(cFile):
    ''' Read the input strings in from a file '''
    # Overwrite output file, if it exists
    open(outFile, 'w+').close()
    with open(cFile, 'r') as file:
        # Solve each line in the file.
        for line in file:
            a, b = line.split(',')
            align('-'+a, '-'+b[:-1])

def readCostFile(cFile):
    ''' Read the cost array into a dictionary of key:value pairs'''
    costs = {}
    with open(cFile, 'r') as file:
        chars = ''
        for f in file:
            f = f.strip('\n').split(',')
            if f[0] is '*':
                # Read in available chars but skip the leading *
                chars = f
                for k in f[1:]:
                    costs[k] = {}
            else:
                # Treat this line as costs for the far left char
                for i, c in enumerate(f):
                    costs[f[0]][chars[i]] = c
    return costs, chars[1:]

<<<<<<< HEAD
#@profile
=======
# @profile
>>>>>>> 0404bc8bdd747e9a9d205a4781cff61271b9bce3
def align(topWord, sideWord):
    def printArr(arr):
        ''' Display the array as it would appear on paper '''
        # Print the header
        print ' #',
        for x in topWord:
            # Pad each column to 2 spaces to fix large inputs
            print "{:>2}".format(x),
        print ''
        # Print each line
        for y in xrange(lenSide):
            for x in xrange(lenTop):
                if x is 0:
                    print "{:>2}".format(sideWord[y]),
                print "{:>2}".format(arr[x][y]),
            print ''

    def printCosts(arr):
        ''' Display the costs as an unsorted array '''
        # Print the header
        print ' #',
        for a in costs:
            # Pad each column to 2 spaces to fix large inputs
            print "{:>2}".format(a),
        print ''
        # Print each line
        for a in costs:
            print "{:>2}".format(a),
            for b in costs:
                print "{:>2}".format(costs[a][b]),
            print ''

    def getCost(a, b):
        ''' Returns cost to convert from one letter to another '''
        return int(costs[a][b])

    def walkHome():
        ''' Walk back to the beginning, creating the changed strings '''
        tW, sW = '', ''
        x, y = lenTop-1, lenSide-1
        while x > 0 or y > 0:
            if DEBUGGING: print x, y, B[x][y]
            if B[x][y] == '-':
                sW = '-'+sW
                tW = topWord[x]+tW
                x -= 1
            elif B[x][y] == '|':
                sW = sideWord[y]+sW
                tW = '-'+tW
                y -= 1
            else:
                sW = sideWord[y]+sW
                tW = topWord[x]+tW
                x -= 1
                y -= 1
        return tW, sW

    # Save word sizes for later
    lenTop = len(topWord)
    lenSide = len(sideWord)

    # Set up the (mostly empty) array
    A = [[0]*lenSide for y in xrange(lenTop)]
    B = [[0]*lenSide for y in xrange(lenTop)]
    # C = [[0 for x in xrange(lenSide)] for y in xrange(lenTop)]
    # D = [[0 for x in xrange(lenSide)] for y in xrange(lenTop)]

    for i in xrange(1,lenTop):
        A[i][0] = A[i-1][0] + getCost('-', topWord[i])
        B[i][0] = '-'
    for i in xrange(1, lenSide):
        A[0][i] = A[0][i-1] + getCost('-', sideWord[i])
        B[0][i] = '|'

    for x in xrange(1,lenTop):
        for y in xrange(1,lenSide):
            t, s = topWord[x], sideWord[y]
            A[x][y], B[x][y] = min(
                (A[x-1][y] + getCost('-', t), '-'),  # insert - into top word
                (A[x][y-1] + getCost(s, '-'), '|'),  # insert - into side word
                (A[x-1][y-1] + getCost(t, s), '\\')  # align characters
            )
    
    
    # Walk backwards through the array to find the two strings
    t, s = walkHome()

    if DEBUGGING:
        print "Calculating the alignment cost between:"
        print topWord
        print sideWord
        print '=== Cost Array ==='
        printCosts(costs)
        print 'The resulting array:'
        printArr(A)
        print '=== Path Home ==='
        printArr(B)
        print '=== Resulting Strings ==='
    # Append this result to the output file, or print it to screen
    with open(outFile, 'a') as out:
        out.write('{},{}:{}\n'.format(t, s, A[lenTop-1][lenSide-1]))

start = time.time()
# Read in the costs from file
costs, chars = readCostFile(costFile)
readInputFile(seqFile)

end = time.time()
print(end-start)