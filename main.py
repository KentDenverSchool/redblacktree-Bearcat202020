class Node:
    def __init__(self, key, value, left, right, isBlack):
        self.left = left
        self.right = right
        self.black = isBlack
        self.key = key
        self.value = value
        self.size = 0
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def isBlack(self):
        return self.black
    def getKey(self):
        return self.key
    def getValue(self):
        return self.value
    def setLeft(self, left):
        self.left = left
    def setRight(self, right):
        self.right = right
    def setRed(self):
        self.black = False
    def setBlack(self):
        self.black = True
    def setKey(self, key):
        self.key = key
    def setValue(self, value):
        self.value = value
    def __repr__(self):
        color = ""
        if self.isBlack:
            color = "Black"
        else:
            color = "Red"
        return("Node{"+"key="+str(self.getKey())+", value="+str(self.getValue())+" color="+str(color)+"}")
    def setSize(self, newSize):
        self.size = newSize
    def getSize(self):
    	self.size = 1
    	if(self.getRight()!=None):
    		self.size += self.getRight().getSize()
    	if(self.getLeft()!=None):
    		self.size += self.getLeft().getSize()
    	return self.size




class RedBlackTree:
    def __init__(self):
        self.root = Node(None, None, None, None, True)


    def rotateRight(self, node):
        node2 = node.getLeft()
        node.setLeft(node2.getRight())
        node2.setRight(node)
        return node2


    def rotateLeft(self, node):
        node2 = node.getRight()
        node.setRight(node2.getLeft())
        node2.setLeft(node)
        return node2


    def isGParent(self, node):
        if(node.getLeft() != None):
            if(node.getLeft().getLeft() != None or node.getLeft().getRight() != None):
                return True
        elif(node.getRight() != None):
            if(node.getRight().getLeft() != None or node.getRight().getRight() != None):
                return True
        else:
            return False

    #counts how many black nodes there are on the right most path to check if all paths have same amount of blacks
    def blacksOnRightPath(self):
        node = self.root
        #root should be black so it already has 1 black
        amtOfBlacks = 1
        while(node.getRight() != None):
            if(node.getRight().isBlack()):
                amtOfBlacks += 1
            node = node.getRight()
        return amtOfBlacks

    def put(self, key, val):
        x = self.__recPut(self.root, key, val)
        self.root = x


    def __recPut(self, node, key, value):
        if(node.getKey() == None):
            self.root = Node(key, value, None, None, True)
            node = self.root
            return node;
            # node.setKey(key)
            # node.setValue(value)

        else:
            if(key >= node.getKey()):
                if (node.getRight()==None):
                    node.setRight(Node(key, value, None, None, True))
                    return node
                else:
                    node.setRight(self.__recPut(node.getRight(), key, value))
                    return node
            #this will check for all values less than
            else:
                if(node.getLeft()==None):
                    node.setLeft(Node(key, value, None, None, True))
                    return node
                else:
                    node.setLeft(self.__recPut(node.getLeft(), key, value))
                    return node

    def __repr__(self):
    	temp = self.__toString(self.root)
    	temp = temp[0:(len(temp)-2)]
    	return "{"+temp+"}"

    def __toString(self, node):
    	if(node==None):
    		return ""
    	else:
    		return str(self.__toString(node.getLeft())) + str(node.getKey()) + "=" + str(node.getValue()) + ", " + str(self.__toString(node.getRight()))




def isRBT(RBT):
    return (checkRuleOne(RBT.root) and checkRuleThree(RBT.root)) and (checkRuleFour(RBT.root, 0, RBT.blacksOnRightPath()) and checkIsBST(RBT.root))

def checkRuleOne(root):
    return root.isBlack()

def checkIsBST(node):
    if(node.getLeft() != None):
    	if(node.getLeft().getKey() >= node.getKey()):
    		return False
    	else:
    		checkIsBST(node.getLeft())
    if(node.getRight() != None):
    	if(node.getRight().getKey() < node.getKey()):
    		return False
    	else:
    		checkIsBST(node.getRight())
    if(node.getLeft() == None and node.getRight() == None):
    	pass
    return True

def checkRuleThree(node):
    if(node.getLeft() != None):
        if(not node.isBlack() and not node.getLeft().isBlack()):
            return False
        checkRuleThree(node.getLeft())
    if(node.getRight() != None):
        if(not node.isBlack() and not node.getRight().isBlack()):
            return False
        checkRuleThree(node.getRight())
    return True

    #recursive function
    #blacks starts at 0
    #counter starts at 0
    #takes in the BST, node it's on, number of black nodes so far, number to compare it to, and current counter
def checkRuleFour(node, blacks, num):
    if(node.isBlack()):
        blacks += 1
    if(node.getRight() != None):
        checkRuleFour(node.getRight(), blacks, num)
    if(node.getLeft() != None):
        checkRuleFour(node.getLeft(), blacks, num)
    if(blacks != num):
        return False
    return True


def main():

    RBT = RedBlackTree()
    RBT.put(1, 2)
    RBT.put(2, 5)
    RBT.put(3, 5)
    print("just put a couple in a redblack tree", RBT)
    RBT.root = RBT.rotateLeft(RBT.root)
    print("testing rotate left, should be the same as before" , RBT)
    RBT.root = RBT.rotateLeft(RBT.root)
    print("testing rotate right, should be the same as before" , RBT)
    RBT.put(4, 7)
    print("testing isGParent, should be True:", RBT.isGParent(RBT.root))

    newRBT = RedBlackTree()
    newRBT.put(2, 5)
    newRBT.put(1, 2)
    newRBT.put(3, 5)
    newRBT.root.getLeft().setRed()
    newRBT.root.getRight().setRed()
    print("testing is RBT, should be True:", isRBT(newRBT))
    newRBT.root.setRed()
    print("making it false.. it now violates rule 1, should be False:", isRBT(newRBT))
    newRBT.root.getRight().setBlack()
    print("making it false... it now violates rule 4, should be False", isRBT(newRBT))
    newRBT.root.setRed()
    newRBT.root.getRight().setRed()
    print("making it false... it now violates rule 3, should be False", isRBT(newRBT))



if __name__ == "__main__":
    main()
