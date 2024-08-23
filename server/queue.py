

class Node():
    def __init__(self, content, nextNode=None):
        self.content = content
        self.next = nextNode


class Queue():
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def push(self, node: Node):
        if self.length == 0:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def pop(self) -> Node:
        if self.length == 0:
            return None 
        temp = self.head
        self.head = self.head.next
        self.length -= 1
        return temp

    def is_empty(self):
        return self.length == 0


if __name__ == "__main__":
    queue = Queue()
    queue.push(Node(0))
    queue.push(Node(1))
    queue.push(Node(2))
    queue.push(Node(3))
    queue.push(Node(2))
    queue.push(Node(1))
    
    t = queue.pop()
    while t is not None:
        print(t.content)
        t = queue.pop()