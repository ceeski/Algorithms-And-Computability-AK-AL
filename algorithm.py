APPROXIMATE = 1 #Maybe should be passed as an command line argument

# Helper functions
def GenerateBaseSequence(size):
    return [i for i in range(size)]

def CreateSequences(sequencesList, baseSequence, firstElement = 0):
    if firstElement == len(baseSequence):
        sequencesList.append(baseSequence)
    else:
        for i in range(firstElement, len(baseSequence)):
            baseSequence[i], baseSequence[firstElement] = baseSequence[firstElement], baseSequence[i]
            CreateSequences(sequencesList, baseSequence.copy(), firstElement + 1)
            baseSequence[i], baseSequence[firstElement] = baseSequence[firstElement], baseSequence[i]

def GenerateMatrixFromSequenceCombination(matrix, sequence):
    returnedMatrix = [[0 for _ in range(len(sequence))] for _ in range(len(sequence))]
    for i in range(len(sequence)):
        for j in range(len(sequence)):
            returnedMatrix[i][j] = matrix[sequence[i]][sequence[j]]
    return returnedMatrix

def CalculateCommonEdges(matrix, smallerMatrixSize):
    commonEdges = 0
    for i in range(smallerMatrixSize):
        for j in range(smallerMatrixSize):
            if matrix[i][j] == 2:
                commonEdges += 1
    return commonEdges

def CalculateRowDegree(matrix, rowNumber):
    row = matrix[rowNumber]
    sum = 0
    for i in row:
        if i > 0:
            sum += 1
    return sum

def FindMaxNotUsedDegree(matrix, matrixSize, sequence):
    maxDeg = -1
    index = -1
    for i in range(matrixSize):
        if i in sequence:
            continue
        deg = CalculateRowDegree(matrix, i)
        if deg > maxDeg:
            maxDeg = deg
            index = i
    return index

def GenerateSequenceOfLabelsFromMaxDegree(matrix, matrixSize):
    sequence = []
    while len(sequence) < matrixSize:
        sequence.append(FindMaxNotUsedDegree(matrix, matrixSize, sequence))
    return sequence

def GenerateApproximateSequence(matrixBigger, matrixBiggerSize, matrixSmaller, matrixSmallerSize):
    sequenceBigger = GenerateSequenceOfLabelsFromMaxDegree(matrixBigger, matrixBiggerSize)
    sequenceSmaller = GenerateSequenceOfLabelsFromMaxDegree(matrixSmaller, matrixSmallerSize)
    realSequence = [-1 for i in range(matrixBiggerSize)]
    for i, j in zip(sequenceSmaller, range(len(sequenceSmaller))):
        realSequence[i] = sequenceBigger[j]
    for i in range(len(sequenceSmaller), len(sequenceBigger)):
        realSequence[i] = sequenceBigger[i]
    return realSequence
 
 
# Read and Print
def ReadMatrices():
    biggerMatrix = [[0,1,0,0,1],
                    [1,0,1,0,1],
                    [0,1,0,1,0],
                    [0,0,1,0,1],
                    [1,1,0,1,0]]
    biggerMatrixSize = 5
    smallerMatrix = [[0,1,0,1],
                     [1,0,1,1],
                     [0,1,0,1],
                     [1,1,1,0]]
    smallerMatrixSize = 4
    return (biggerMatrix, biggerMatrixSize, smallerMatrix, smallerMatrixSize)

def SaveAnswer(commonEdges, mappingSequence, graph):
    if APPROXIMATE:
        print("APPROXMIATE")
    else:
        print("EXACT")
    print(commonEdges)
    print(mappingSequence)
    print(graph)


# Algorithm
def main():
    (biggerMatrix, biggerMatrixSize, smallerMatrix, smallerMatrixSize) = ReadMatrices()

    sequenceList = []

    if APPROXIMATE:
        sequenceList = [GenerateApproximateSequence(biggerMatrix, biggerMatrixSize, smallerMatrix, smallerMatrixSize)]
    else:
        CreateSequences(sequenceList, GenerateBaseSequence(biggerMatrixSize))

    mostMatchingSequence = []
    smallestCommonSupergaph = []
    mostMatchingEdges = 0

    for sequence in sequenceList:
        rearrangedMatrix = GenerateMatrixFromSequenceCombination(biggerMatrix, sequence)
        for i in range(smallerMatrixSize):
            for j in range(smallerMatrixSize):
                rearrangedMatrix[i][j] += smallerMatrix[i][j]
        commonEdges = CalculateCommonEdges(rearrangedMatrix, smallerMatrixSize)
        if commonEdges > mostMatchingEdges:
            mostMatchingEdges = commonEdges
            mostMatchingSequence = sequence
            smallestCommonSupergaph = rearrangedMatrix
            
    SaveAnswer(mostMatchingEdges, mostMatchingSequence, smallestCommonSupergaph)

if __name__ == "__main__":
    main()