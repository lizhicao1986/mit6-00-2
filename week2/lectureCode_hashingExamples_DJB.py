#! /usr/bin/env python

import random


class intDict(object):
    """A dictionary with integer keys"""
    
    def __init__(self, numBuckets):
        """Create an empty dictionary"""
        self.buckets = []
        self.numBuckets = numBuckets
        for i in range(numBuckets):
            self.buckets.append([])
            
    def addEntry(self, dictKey, dictVal):
        """Assumes dictKey an int.  Adds an entry."""
       # hashBucket = self.buckets[dictKey%self.numBuckets]
	hashBucket = self.buckets[DJBHash(dictKey)%self.numBuckets]
        for i in range(len(hashBucket)):
            if hashBucket[i][0] == dictKey:
                hashBucket[i] = (dictKey, dictVal)
                return
        hashBucket.append((dictKey, dictVal))
        
    def getValue(self, dictKey):
        """Assumes dictKey an int.  Returns entry associated
           with the key dictKey"""
       # hashBucket = self.buckets[dictKey%self.numBuckets]
	hashBucket = self.buckets[DJBHash(dictKey)%self.numBuckets]
        for e in hashBucket:
            if e[0] == dictKey:
                return e[1]
        return None
    
    def __str__(self):
        res = ''
        for b in self.buckets:
            for t in b:
                res = res + str(t[0]) + ':' + str(t[1]) + ','
        return '{' + res[:-1] + '}' 

def DJBHash(key):
	length = len(str(key))
	hash = 5381
	i = 0
	for i in range(length):
		hash = (hash << 5) + int(key[i])

	return hash


D = intDict(71)
for i in range(100):
    #choose a random int in range(10**5)
    key = str(random.choice(range(10**5)))
    D.addEntry(key,i)

print '\n', 'The buckets are:'
for hashBucket in D.buckets: #violates abstraction barrier
    print '  ', hashBucket

















