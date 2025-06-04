import math
import random
import bitlist
from bitlist import bitlist


def create_splice(qubits, oneInputGates,twoInputGates,oneInputChance,network,size,numOfQubits,usedQubits):
    spliceCoeff = random.randint(1,5)
    test = 0
    outputSplice = []
    while (test != spliceCoeff):
        qubitNum = random.randint(0,usedQubits-1)
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
            sourceBits = bitlist(sourceNode.getNodeNumber(),4)
            print(f"Source :{sourceBits}")
            targetBits = sourceBits[-1:] + sourceBits[:-1]  
            print(f"Target : {targetBits} ")
            targetNodeIndex = int(targetBits)
            # Calculate base index of qubits in targetNode
            qubitsPerNode = numOfQubits
            stride = size * size
            offset = random.randint(0, qubitsPerNode - 1)
            targetQubit = targetNodeIndex + stride * offset
            if ( (targetQubit < usedQubits) and qubits[targetQubit] != 1):
                outputSplice.append(f"({qubitNum} {targetQubit})")     
                qubits[targetQubit] = 1   
                twoInputGates -= 1
        test = random.randint(1,5)
    

    return twoInputGates,oneInputGates,outputSplice

def generateCircuit(oneInputGates,twoInputGates,qubits,numOfQubits,Size,usedQubits,name):
    with open(name,"w") as file:
        while(twoInputGates != 0 or oneInputGates != 0):
            twoInputGates,oneInputGates,outputSplice = create_splice(qubits,oneInputGates,
                        twoInputGates,oneInputChance,network,size,numOfQubits,usedQubits)
            qubits = [0] * usedQubits
            if outputSplice:
                file.write(" ".join(outputSplice))
                file.write(" \n")

def getNodeCoordinates(qubitIndex, size, numOfQubits):
    nodeNumber = qubitIndex % (size*size)
    row = nodeNumber // size
    col = nodeNumber % size
    return (row, col)

def attainParamaters():
    with open ("architecture","r") as file:
        numbers = [int(word) for line in file for word in line.split() if word.isdigit()]
    return numbers[1],numbers[3]

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

size, numOfQubits = attainParamaters()
oneInputChance = float(input("Enter a decimal 0 to 1 representing the % ofs  1 input gates: "))
twoInputChance = 1 - float(oneInputChance)
usedQubits = int(input(f"You have {size*size*numOfQubits} total qubits, enter the number of those you'd wish to use: "))
numOfGates = int(input("Enter The number of Gates you'd like to create: "))
name = input("Enter File name: ")
#Create Network
network = Network([],size)
for i in range(size):
    for j in range(size):
      network.addNode(Node(i*size+j,size,(i,j)),i,j)
qubits = [0] * usedQubits
oneInputGates = math.floor(oneInputChance*numOfGates)
twoInputGates = math.floor(twoInputChance*numOfGates)
generateCircuit(oneInputGates,twoInputGates,qubits,numOfQubits,size,usedQubits,name)



  