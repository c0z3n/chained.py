# coding: utf-8
from collections import defaultdict
import random

START = "<"
END   = ">"
NA    = "^"

class Chain(defaultdict):
    def __init__(self, order=1):
        self.order = order
        self.startState = tuple((NA*(order-1)) + START)
        self.endState = tuple(END + NA*(order-1))
        self.runningGetState = self.startState
        self.runningAddState = self.startState
        super(Chain, self).__init__(lambda: defaultdict(int))


    def choice(self, source):
        """choose a key from a dictionary based on the value associated therewith.
            source -- a dictionary of keypairs where keys are items in the Chain() and values are instances of that item 
            for a given node
        """
        return random.choice(sum(([state]*instances for state, instances in source.items()),[]))

    def addNode(self, prev, next):
        """add a node (instance) of a state to the Chain()
        prev -- a list or tuple of a length determined by self.order in which each item describes a previous state of the 
        Chain(), [0] being furthest in the past and [-1] being the state immediately previous
        next -- the value that follows the series of states described in prev.
        """
        self[tuple(prev)][next] += 1

    def addNextNode(self, value):
        """add the "next" node, which is the node that follows the last node that was added using addNextNode(). the Chain()
        keeps track of the previous n nodes added (where n is the order of the chain) in self.runningAddState. if 
        addNextNode() has never been called before on a given instance of a Chain(), it is assumed that the node to add is
        the beginning of a sequence.
        """
        self.addNode(self.runningAddState, value)
        self.runningAddState = tuple(list(self.runningAddState[1:]) + [value])

    def addSequence(self, sequence):
        """scans through a sequence and adds it all to the Chain(). also store the start and end of the sequence with 
        special symbols
        sequence -- a list or tuple of any length longer than self.order, from which to draw state information for the Chain()
            sequence may also be a string, if you wish to index character information
        """
        sequence = list(self.startState) + list(sequence) + list(self.endState)
        for idx in xrange(self.order, len(sequence)):
            self.addNode(sequence[idx-self.order:idx], sequence[idx])

    def getNode(self, state):
        """return the next node (state) for a given input state
        state -- a list or tuple of a length determined by self.order in which each item describes a previous state of the
        Chain(), [0] being furthest in the past and [-1] being the state immediately previous
        """
        return tuple(list(state[1:]) + [self.choice(self[tuple(state)])])

    def getNextNode(self):
        """get the "next" node, which is the node that follows the last node that was fetched using addNextNode(). The Chain()
        keeps track of the previous n nodes fetched (where n is the order of the chain) in self.runningGetState. If 
        getNextNode() has never been called before on a given instance of a Chain(), it is assumed that the node to get should
        be the first in a sequence.
        """
        self.runningGetState = self.getNode(self.runningGetState)
        if (self.runningGetState[-1] == END) or not self[self.runningGetState] or len(self[self.runningGetState])<1:
            self.runningGetState = self.getNode(self.startState)
        return self.runningGetState[-1]

    def getSequence(self):
        """return a sequence chosen from the Chain()
        this starts with a state comprised of special characters NA (n/a) and START which represent nodes we don't yet care 
        about and the start of a sequence, respectively. as the sequence is generated we keep a running window of the last 
        (self.order) nodes we chose and use that to generate next states until we encounter a END symbol
        """
        state = self.getNode(list(self.startState))
        sequence = list()
        while (state[-1] != END) and self[state] and len(self[state]) > 0:
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