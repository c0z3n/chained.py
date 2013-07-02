# coding: utf-8
from collections import defaultdict
import random

START = "<"
END   = ">"
NA    = "^"

class Chain(defaultdict):
    def __init__(self, order=1):
        self.order = order
        self.runningState = tuple((NA*(order-1)) + START)
        super(Chain, self).__init__(lambda: defaultdict(int))

    def choice(self, source):
        """choose a key from a dictionary based on the value associated therewith.
            source -- a dictionary of keypairs where keys are items in the Chain() and values are instances of that item 
            for a given node
        """
        return random.choice(sum(([state]*instances for state, instances in source.items()),[]))

    def addNode(self, prev, next):
        """add a node (instance) of a state to the Chain()
        prev -- a list or tuple of a length determined by self.order in which each item descrives a previous state of the 
        Chain(), [0] being furthest in the past and [-1] being the state immediately previous
        next -- the value that follows the series of states described in prev.
        """
        self[tuple(prev)][next] += 1

    def addSequence(self, sequence):
        """scans through a sequence and adds it all to the Chain(). also store the start and end of the sequence with 
        special symbols
        sequence -- a list or tuple of any length longer than self.order, from which to draw state information for the Chain()
            sequence may also be a string, if you wish to index character information
        """
        sequence = list(NA*self.order+START) + list(sequence) + list(END+NA*self.order)
        for idx in xrange(self.order, len(sequence)):
            self.addNode(sequence[idx-self.order:idx], sequence[idx])

    def getNode(self, state):
        """return the next node (state) for a given input state
        state -- a list or tuple of a length determined by self.order in which each item descrives a previous state of the
        Chain(), [0] being furthest in the past and [-1] being the state immediately previous
        """
        return tuple(list(state[1:]) + [self.choice(self[tuple(state)])])

    def getNextNode(self):
        self.runningState = self.getNode(self.runningState)
        return self.runningState[-1]

    def getSequence(self):
        """return a sequence chosen from the Chain()
        this starts with a state comprised of special characters NA (n/a) and START which represent nodes we don't yet care 
        about and the start of a sequence, respectively. as the sequence is generated we keep a running window of the last 
        (self.order) nodes we chose and use that to generate next states until we encounter a END symbol
        """
        state = self.getNode(list(NA*(self.order-1)+START))
        sequence = list()
        while state[-1] != END:
            sequence.append(state[-1])
            state = tuple(list(state[1:]) + [self.choice(self[state])])
        return sequence

# test/example

if __name__ == "__main__":
    text = "I sent my representatives a form letter, and all I got back was a form letter. Should I be upset? You would have sent yourself back a form letter. They're just representing you."

    print "    example output using a chain of individual letters:\n"
    a = Chain(3) # create an empty chain of a given order
    a.addSequence(text) # this chain will index characters, because we're just passing in a string
    seq_a = a.getSequence()    
    out = "    "
    for i in seq_a: out += str(i)
    print out + "\n\n"

    print "    example output using a chain of words:\n"
    b = Chain(2)
    b.addSequence(text.split()) # this chain will index words, because we're passing it a list of words
    seq_b = b.getSequence()
    out = "    "
    for i in seq_b: out += str(i)+" "
    print out