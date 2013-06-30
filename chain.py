# coding: utf-8
from collections import defaultdict
import random

START = "<"
END   = ">"
NA    = "^"

class Chain(defaultdict):
    def __init__(self, order):
        self.order = order
        super(Chain, self).__init__(lambda: defaultdict(int))

    def choice(self, source):
        return random.choice(sum(([state]*instances for state, instances in source.items()),[]))

    def addNode(self, prev, next):
        self[tuple(prev)][next] += 1

    def addSequence(self, sequence):
        sequence = list(NA*self.order+START) + list(sequence) + list(END+NA*self.order)
        for idx in xrange(self.order, len(sequence)):
            self.addNode(sequence[idx-self.order:idx], sequence[idx])

    def getNode(self, state):
        return tuple(list(state[1:]) + [self.choice(self[tuple(state)])])

    def getSequence(self):
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
    a.addSequence(text)
    seq_a = a.getSequence()    
    out = "    "
    for i in seq_a: out += str(i)
    print out + "\n\n"

    print "    example output using a chain of words:\n"
    b = Chain(2)
    b.addSequence(text.split())
    seq_b = b.getSequence()
    out = "    "
    for i in seq_b: out += str(i)+" "
    print out