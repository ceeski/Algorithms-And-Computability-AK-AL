from typing import List
import hashlib
import pathlib
import sys
from pathlib import Path

USAGE = f"Usage: python {sys.argv[0]} [filename | filename -a | filename -e]"

# Helper functions


def GenerateBaseSequence(size):
    return [i for i in range(size)]


def CreateSequences(sequencesList, baseSequence, firstElement=0):
    if firstElement == len(baseSequence):
        sequencesList.append(baseSequence)
    else:
        for i in range(firstElement, len(baseSequence)):
            baseSequence[i], baseSequence[firstElement] = baseSequence[firstElement], baseSequence[i]
            CreateSequences(sequencesList, baseSequence.copy(),
                            firstElement + 1)
            baseSequence[i], baseSequence[firstElement] = baseSequence[firstElement], baseSequence[i]


def GenerateMatrixFromSequenceCombination(matrix, sequence):
    returnedMatrix = [[0 for _ in range(len(sequence))]
                      for _ in range(len(sequence))]
    for i in range(len(sequence)):
        for j in range(len(sequence)):
            returnedMatrix[i][j] = matrix[sequence[i]][sequence[j]]
    return returnedMatrix

def RevertRearrangedMatrix(rearrangedMatrix, sequence):
    returnedMatrix = [[0 for _ in range(len(sequence))]
                      for _ in range(len(sequence))]
    for i in range(len(sequence)):
        for j in range(len(sequence)):
            returnedMatrix[sequence[i]][sequence[j]] = rearrangedMatrix[i][j]
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
    sequenceBigger = GenerateSequenceOfLabelsFromMaxDegree(
        matrixBigger, matrixBiggerSize)
    sequenceSmaller = GenerateSequenceOfLabelsFromMaxDegree(
        matrixSmaller, matrixSmallerSize)
    realSequence = [-1 for i in range(matrixBiggerSize)]
    for i, j in zip(sequenceSmaller, range(len(sequenceSmaller))):
        realSequence[i] = sequenceBigger[j]
    for i in range(len(sequenceSmaller), len(sequenceBigger)):
        realSequence[i] = sequenceBigger[i]
    return realSequence


# Read and Print
def ReadMatrices(path):
    file = open(path, "r")
    firstMatrixSize = int(file.readline().split(" ")[0])
    firstMatrix = []
    count = 0
    while count < firstMatrixSize:
        line = file.readline()
        firstMatrix.append([int(j) for j in line.split()])
        if not line:
            break
        count+=1
    secondMatrixSize = int(file.readline().split(" ")[0])
    secondMatrix = []
    while True:
        line = file.readline()
        secondMatrix.append([int(j) for j in line.split()])
        if not line:
            break
    file.close()

    if firstMatrixSize > secondMatrixSize:
        return (firstMatrix, firstMatrixSize, secondMatrix, secondMatrixSize)
    else:
        return (secondMatrix, secondMatrixSize, firstMatrix, firstMatrixSize)



def SaveAnswer(commonEdges, mappingSequence, graph, approximate):
    with open('answer.txt', 'w') as f:
        if approximate:
            f.write("APPROXIMATE"+ '\n')
        else:
            f.write("EXACT"+ '\n')
        f.write(str(commonEdges)+ '\n')
        f.write(" ".join(str(j) for j in mappingSequence)+ '\n\n')
        for row in graph:
            f.write(" ".join(str(item) for item in row) + '\n')
        graph2 = RevertRearrangedMatrix(graph, mappingSequence)
        f.write("\n")
        for row in graph2:
            f.write(" ".join(str(item) for item in row) + '\n')

def SaveAnswerWithNames(commonEdges, mappingSequence, graph, approximate, small, larger):
    with open('answer_named.txt', 'w') as f:
        if approximate:
            f.write("APPROXIMATE"+ '\n\n')
        else:
            f.write("EXACT"+ '\n\n')
        f.write("Common Edges\n"+str(commonEdges)+ '\n\n')
        f.write("Mapping Sequence\n"+" ".join(str(j) for j in mappingSequence)+ '\n')
        f.write("\nSmaller original graph\n")
        for row in small:
            f.write(" ".join(str(item) for item in row) + '\n')
        f.write("\nLarger original graph\n")
        for row in larger:
            f.write(" ".join(str(item) for item in row) + '\n')    
        f.write("Mapped Sequence on the Larger Graph\n")
        for row in graph:
            f.write(" ".join(str(item) for item in row) + '\n')
        graph2 = RevertRearrangedMatrix(graph, mappingSequence)
        f.write("\nCommon subgraph/supergraph on larger graph\n")
        for row in graph2:
            f.write(" ".join(str(item) for item in row) + '\n')

# Algorithm
def main(input_list: List[str]) -> None:
    if len(input_list) < 1:
        print(USAGE)
    else:
        opts = [opt for opt in input_list if opt.startswith("-")]
        input_file = Path(input_list[0])
        if not input_file.is_file():
            print("Wrong file!")        
        approximate = 0
        if "-a" in opts:
            approximate = 1

        (biggerMatrix, biggerMatrixSize, smallerMatrix,smallerMatrixSize) = ReadMatrices(input_file)

        sequenceList = []

        if approximate:
            sequenceList = [GenerateApproximateSequence(
                biggerMatrix, biggerMatrixSize, smallerMatrix, smallerMatrixSize)]
        else:
            CreateSequences(sequenceList, GenerateBaseSequence(biggerMatrixSize))

        mostMatchingSequence = []
        smallestCommonSupergaph = []
        mostMatchingEdges = 0

        for sequence in sequenceList:
            rearrangedMatrix = GenerateMatrixFromSequenceCombination(
                biggerMatrix, sequence)
            for i in range(smallerMatrixSize):
                for j in range(smallerMatrixSize):
                    rearrangedMatrix[i][j] += smallerMatrix[i][j]
            commonEdges = CalculateCommonEdges(rearrangedMatrix, smallerMatrixSize)
            if commonEdges > mostMatchingEdges:
                mostMatchingEdges = commonEdges
                mostMatchingSequence = sequence
                smallestCommonSupergaph = rearrangedMatrix

        SaveAnswer(mostMatchingEdges, mostMatchingSequence,
                smallestCommonSupergaph, approximate)
        SaveAnswerWithNames(mostMatchingEdges, mostMatchingSequence,
                smallestCommonSupergaph, approximate, smallerMatrix, biggerMatrix)

if __name__ == "__main__":
    main(sys.argv[1:])
