chained.py
=========

a simple python markov chain implementation

Usage
=====

a Markov chain is represented by the `Chain()` object. a `Chain()` is initialized 
with an order, which defines how many states into the past should be considered 
when choosing the next state. The order defaults to 1 if not specified. After the 
chain is initialized, sequences may be added to it using `Chain.addSequence()`, 
and extracted from it (generated) using `Chain.getSequence()`

### example:
    from chained import Chain

    mychain = Chain(3)             # create an empty third order chain "mychain"
    mychain.addSequence(text)      # mychain will index characters in this string
    seq = mychain.getSequence()    # seq is now a list of characters generated from mychain

This snippet will generate a sequence of characters from the text that fed to the chain with `Chain.addSequence()`. 

For example, using the raw string input:

    text = "I sent my representatives a form letter, and all I got back was a form letter. Should I be upset?"

the following output was generated using a third order markov chain:

    I sent my representatives a form letter. Should I got back was a form letter. Should I be upset?

... and from a second order chain:

    I sent be upsent back was and all I be upset?

... and a first order chain:

    I r. ba I uld my a lettack les ulentt a upser. bald ale Shor, ate fott?

