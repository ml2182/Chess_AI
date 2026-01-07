class Node:
    def __init__(self, data=None):
        self.__data = data
        self.__next = None

    def get_data(self):
        return self.__data
    
    def set_data(self, data):
        self.__data = data

    def get_next(self):
        return self.__next
    
    def set_next(self,next):
        self.__next = next

class Stack:
    def __init__(self):
        self.__top = None

    def push(self, data): # add a new node to the top of the stack
        if self.__top is None:
            self.__top = Node(data)
        else:
            new_node = Node(data)
            new_node.set_next(self.__top)
            self.__top = new_node

    def pop(self): # remove the top node from the stack and return its data
        if self.__top is None:
            return None
        else:
            popped_node = self.__top
            self.__top = self.__top.get_next()
            popped_node.set_next(None)
            return popped_node.get_data()

    def peek(self): # return the data of the top node in the stack
        return self.__top.get_data() if self.__top is not None else None
    
    def length(self): # return the number of nodes in the stack
        current = self.__top
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count
    
    def is_empty(self): # return True if the stack is empty, False otherwise
        return self.__top is None