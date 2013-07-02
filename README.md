chained.py
=========

a simple python markov chain implementation

Usage
=====

a Markov chain is represented by the `Chain()` object. a `Chain()` is initialized 
with an order, which defines how many states into the past should be considered 
when choosing the next state. After the chain is initialized, sequences may be added
to it using `Chain.addSequence()`, and extracted from it (generated) using `Chain.getSequence()`

### example:
    from chained import Chain

    mychain = Chain(3)             # create an empty third order chain "mychain"
    mychain.addSequence(text)      # mychain will index characters in this string
    seq = mychain.getSequence()    # seq is now a list of characters generated from mychain