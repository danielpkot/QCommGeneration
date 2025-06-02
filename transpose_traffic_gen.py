import math
import random

def create_splice(qubits, oneInputGates,twoInputGates,oneInputChance,network,size,numOfQubits):
    spliceCoeff = random.randint(1,5)
    test = 0
    outputSplice = []
    while (test != spliceCoeff):
        qubitNum = random.randint(0,len(qubits)-1)
        chance = random.random()
        if (chance < oneInputChance and (qubits[qubitNum] != 1) and oneInputGates != 0):
            qubits[qubitNum] = 1
            outputSplice.append(f"({qubitNum})")
            oneInputGates -= 1
        elif((qubits[qubitNum] != 1) and twoInputGates != 0):
            qubits[qubitNum] = 1
            nodes = network.getNodes()
            x,y = getNodeCoordinates(qubitNum,size,numOfQubits)
            sourceNode = nodes[x][y]
            targetNode = nodes[y][x]
            # Calculate base index of qubits in targetNode
            targetNodeIndex = targetNode.getNodeNumber()
            qubitsPerNode = numOfQubits
            baseIndex = targetNodeIndex * qubitsPerNode
            # Choose a random qubit within that node
            offset = random.randint(0, qubitsPerNode - 1)
            targetQubit = baseIndex + offset
            if (qubits[targetQubit] != 1):
                outputSplice.append(f"({qubitNum} {targetQubit})")     
                qubits[targetQubit] = 1   
                twoInputGates -= 1
        test = random.randint(1,5)
    print(" ".join(outputSplice))

    return twoInputGates,oneInputGates

def getNodeCoordinates(qubitIndex, size, numOfQubits):
    nodeNumber = qubitIndex // numOfQubits
    row = nodeNumber // size
    col = nodeNumber % size
    return (row, col)

class Node:
    def __init__(self, nodeNumber,qbAmount,coordinates):
        self.nodeNumber = nodeNumber
        self.qbAmount = qbAmount
        self.coordinates = coordinates
        
    def getNodeNumber(self):
        return self.nodeNumber
    
    def getQbAmount(self):
        return self.qbAmount

    def getCoords(self):
        return self.coordinates
    
    def __str__(self):
        return f"ID: {self.nodeNumber} , Coords: {self.coordinates}"


class Network:
    def __init__(self,nodes,size):
        self.nodes = [[None for _ in range(size)] for _ in range(size)]
        self.size = size

    def addNode(self,node,x,y):
        self.nodes[x][y] = node

    def getNodes(self):
        return self.nodes


print("The Following Program Generates traffic for an n x n homogenous QC platform, to be tested with QComm")

size = int(input("Input an N value: " ))
numOfQubits = int(input("Input the number of Qubits per node: "))
oneInputChance = float(input("Enter a decimal 0 to 1 representing the % of  1 input gates: "))
twoInputChance = 1 - float(oneInputChance)
usedQubits = int(input(f"You have {size*size*numOfQubits} total qubits, enter the number of those you'd wish to use: "))
numOfGates = int(input("Enter The number of Gates you'd like to create: "))


network = Network([],size)

qubits = [0] * numOfQubits * size *size


for i in range(size):
    for j in range(size):
      network.addNode(Node(i*size+j,size,(i,j)),i,j)


for row in network.getNodes():
    for column in row:
         print(str(column)) 


oneInputGates = math.floor(oneInputChance*numOfGates)
twoInputGates = math.floor(twoInputChance*numOfGates)


while(twoInputGates != 0 or oneInputGates != 0):
    twoInputGates,oneInputGates = create_splice(qubits,oneInputGates,
                  twoInputGates,oneInputChance,network,size,numOfQubits)
    qubits = [0] * numOfQubits * size *size


