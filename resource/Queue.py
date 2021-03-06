from tabulate import tabulate
from .Mbox import Mbox
from .Public import global_
from .Upscale import getImgName_With_Ext

class Circular_Q:
    """
    Class for implementing circular queue, error ui will be thrown from here, except for the dequeue and get head.
    """
    def __init__(self, capacity):
        """
        Initialize the queue
        """
        if capacity > 200:
            capacity = 200
        
        if capacity < 1:
            capacity = 1

        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        self.capacity = capacity
        print(f"Queue has been created! With capacity of {self.capacity}")

    def is_Full(self):
        """Check if the queue is full

        Returns:
            [boolean]: [True] if full, [False] if not full
        """
        return self.size == self.capacity

    def is_Empty(self):
        """Check if the queue is empty

        Returns:
            [boolean]: [True] if empty, [False] if not empty
        """
        return self.size == 0

    def clear(self):
        """Clear the queue

        Returns:
            [boolean]: [True] if success, [False] if fail
        """
        is_Success = False
        try:
            self.queue = [None] * self.capacity
            self.head = 0
            self.tail = 0
            self.size = 0
            print("Queue has been cleared!")
            is_Success = True
            global_.statusChange(f"Cleared/Reseted Queue!")
        except Exception as e:
            print("Fail to clear Queue!\nReason: " + str(e))
            Mbox("Fail to clear Queue!", str(e), 2, global_.main_Frame)
        finally:
            return is_Success

    def get_Size(self):
        """Get the size of the queue

        Returns:
            [int]: size of the queue
        """
        return self.size

    def display(self):
        """
        Display the queue
        """
        queue_Data = ""
        head_Tail_Pos = ""
        tableDisplay = []

        # Display queue as table
        print("Current queue: ")
        for i in range(0, self.capacity):
            queue_Data = self.queue[i] if self.queue[i] is not None else "None"
            if i == self.head and i == self.tail:
                head_Tail_Pos = "Head-Tail"
            elif i == self.head:
                head_Tail_Pos = "Head"
            elif i == self.tail:
                head_Tail_Pos = "Tail"
            else:
                head_Tail_Pos = ""

            tableDisplay.append([i, head_Tail_Pos, queue_Data])

        # Table using tabulate
        print(tabulate(tableDisplay, headers=["index","Head/Tail", "Queue"]))

        print("Queue capacity\t:", self.capacity)
        print("Queue size\t:", self.size)
        print("Head position\t:", self.head)
        print("Tail position\t:", self.tail)

    def get_Queue(self):
        """Get the queue

        Returns:
            [list]: queue
        """
        return self.queue

    def enqueue(self, data):
        """Add the data to the tail of the queue

        Args:
            data (any): data to be added to the queue

        Returns:
            [boolean]: [True] if success, [False] if fail
        """
        is_Success = False
        try:
            # Check full
            if self.is_Full(): # size = capacity
                print("Queue is Full!")
                Mbox("Queue is Full!", "Queue is full! You cannot add any more item!", 1, global_.main_Frame)
                return is_Success

            # Store the data
            self.queue[self.tail] = data
            
            # Calculate the tail and size
            self.tail = (self.tail + 1) % self.capacity # Circular queue implementation
            self.size += 1

            print("Enqueued:", data)
            is_Success = True
            img_name_with_ext = getImgName_With_Ext(data[0])
            removeNoise = "with noise removal" if data[5] == True else "with no noise removal"
            modeandScale = f"{data[3]}_x{data[4]}" if data[3] != "None" else "no upscaling"

            global_.statusChange(f"Enqueued \"{img_name_with_ext}\" mode \"{modeandScale}\" {removeNoise}")
        except Exception as e:
            print("Fail to enqueue!\nReason: " + str(e))
            Mbox("Fail to enqueue!", "Fail to enqueue! Reason: " + str(e), 2, global_.main_Frame)
            global_.statusChange(f"Fail to enqueue!")
        finally:
            return is_Success
            
    def dequeue(self):
        """Dequeue the head data from the queue. Mbox handled in main.

        Returns:
            [boolean, dequeued_data]: [True, data] if success, [False, None] if fail
        """
        is_Success = False
        dequeued_Data = None
        try:
            # Check empty
            if self.is_Empty(): # self.size == 0
                print("Queue is Empty!")
                dequeued_Data = "Queue is empty!"
                return is_Success, dequeued_Data

            # Get the data
            data = self.queue[self.head]
            # Erase the data
            self.queue[self.head] = None
            
            # Calculate the head and size
            self.head = (self.head + 1) % self.capacity
            self.size -= 1

            print("Dequeued:", data)
            dequeued_Data = data
            is_Success = True
            img_name_with_ext = getImgName_With_Ext(dequeued_Data[0])
            global_.statusChange(f"Dequeued \"{img_name_with_ext}\"")
        except Exception as e: # Mbox handled in main
            print("Fail to dequeue!\nReason: " + str(e))
            dequeued_Data = str(e)
            global_.statusChange(f"Fail to dequeue!")
        finally:
            return is_Success, dequeued_Data

    def get_Head(self):
        """Get the data from the head of the queue

        Returns:
            [boolean, dequeued_data]: [True, data] if success, [False, reason] if fail
        """
        is_Success = False
        head_Data = None
        try:
            # Check empty
            if self.is_Empty(): # self.size == 0
                print("Queue is Empty!")
                head_Data = "Queue is empty!"
                return is_Success, head_Data

            # Get the data
            data = self.queue[self.head]
            
            print("Get head:", data)
            head_Data = data
            is_Success = True
        except Exception as e:
            print("Fail to get head data!\nReason: " + str(e))
            head_Data = str(e)
        finally:
            return is_Success, head_Data