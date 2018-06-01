__author__ = 'Dennis Qiu'
import math
import time

load_factors = [0.5, 0.75]
loadFactor = load_factors[0]
total_time = 0
search_count = 0

def search_time(isbn, hash_table):
    global total_time
    global search_count
    start = time.clock()
    print('Searching ISBN {} in library'.format(isbn))
    if isbn in hash_table:
        print(hash_table.get(isbn))
        found = True
    else:
        print("Book with this ISBN number is not found in the library.")
        found = False
    stop = time.clock()
    elpSeconds = stop - start
    total_time += elpSeconds
    search_count += 1
    print('Search took {:5f} seconds, found: {}, average: {:5f}'.format(elpSeconds, found, total_time / search_count))
    return elpSeconds

def main():
    """ This program hashes Books.txt.
        1. Change the hash function as indicated below.
        2. Change the rehash function as indicated below.
        3. How many times does this hash table make itself bigger (change its size)?
        4. Which load factor in the range .5 to .9 in steps of .25 is optimal in the sense
        of least time to build the hash table given a start size of 11 on Books.txt?
        5. Which hash works best?
        The original with a load factor of .5 using  the first character key and linear probing
        or your modified/optimized with steps 1-4 hash?
        6. Write a function(s) that run after main is done to prove your conclusions for steps 5 & 6.
    """
    start = time.clock()
    d = []
    library = HashTable()
    with open('Books.txt', 'r', encoding='utf-8') as f:
        for line in f:
            d.append(line.strip())
            if len(d) == 3:
                library.put(int(d[2]), Book(d[0], d[1], d[2]))
                d = []
    stop = time.clock()
    print('Building hash took {:5f} seconds with load factor of {}'.format(stop-start, loadFactor))
    print('Times required to resize:{:5d}\n'.format(library.resizes))

    #isbn = 9780821336953
    #print('You entered ISBN {}'.format(isbn))
    #if isbn in library:
    #    print(library.get(isbn))
    #else:
    #    print("I couldn't find a book with that ISBN number.'")
    #isbn = int(input('enter ISBN: '))
    #print('You entered ISBN {}'.format(isbn))
    #if isbn in library:
    #    print(library.get(isbn))
    #else:
    #    print("I couldn't find a book with that ISBN number.'")
    #print('Return value for library.get({}) is "{}"'.format(isbn, library.get(isbn)))

    isbns = [9780821336953, 9781464802027, 9781464802126, 9780821350164, 9781464899999]
    for isbn in isbns:
        search_time(isbn, library)
        print('\t')

    print('ANSWERS\nQuestion 3: 0 times\nQuestion 4: load factor of 0.5\nQuestion 5: Modified Hash')

class Book:
    def __init__(self, n, a, i):
        self.name = n
        self.author = a
        self.isbn = i

    def __str__(self):
        return self.name + '\n' + self.author + '\n' + self.isbn
    
class HashTable:
    def __init__(self):
        self.size = 11  # the capacity of the list
        self.count = 0  # the number of elements inserted into the hash table
        self.slots = [None] * self.size
        self.data = [None] * self.size
        self.resizes = 0

    def __contains__(self, b):
        return b in self.slots
    
    def put(self,key,data):
        # make the hash table bigger
        if self.count / self.size > loadFactor:
            nextPrime = findNextPrime(2*self.size + 1)
            oldslots = self.slots[:]
            olddata = self.data[:]

            self.size = nextPrime
            self.count = 0
            self.slots = [None] * self.size
            self.data = [None] * self.size
            for index in range(len(oldslots)):
                if oldslots[index] != None:
                    self.put(oldslots[index], olddata[index])
        hashvalue = self.hashfunction(key,len(self.slots))

        if self.slots[hashvalue] == None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
            self.count += 1
        else:
            if self.slots[hashvalue] == key:
                self.data[hashvalue] = data  #replace
            else:
                nextslot = self.rehash(hashvalue,len(self.slots))
                while self.slots[nextslot] != None and \
                                self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot,len(self.slots))

                if self.slots[nextslot] == None:
                    self.slots[nextslot]=key
                    self.data[nextslot]=data
                    self.count += 1
                else:
                    self.data[nextslot] = data #replace
################################################################################
    ''' Rewrite this hash function to fold the key by making groups of 4 (the first 4 digits,
        the second 4 digits, and the third 4 digits, adding them together, and then dividing
        by the length of the hash table.
    '''
    def hashfunction(self,key,size):
        ''' Change this!!!! 
        '''
        s=str(key)
        a, b, c = int(s[:4]), int(s[4:8]), int(s[8:12])
        return (a + b + c)%size
################################################################################

################################################################################
    ''' Rewrite this rehash function to use quadratic probing.
    '''
    def rehash(self,oldhash,size, rehCount=0):
        count = list(range(1, 3 * size + 1, 2))
        return (oldhash+count[rehCount])%size
################################################################################

    def get(self,key):
        startslot = self.hashfunction(key,len(self.slots))

        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and \
                not found and not stop:
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position=self.rehash(position,len(self.slots))
                if position == startslot:
                    stop = True
        return data

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,data):
        self.put(key,data)

    def __len__(self):
        return self.count

def isPrime(n):
    ''' Returns True if n is a prime number.  False, otherwise.
    '''
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt = math.sqrt(n)
    for div in range(3, int(sqrt + 1), 2):
        if n % div == 0:
            return False
    return True

def findNextPrime(n):
    ''' Finds the next prime number >= n.
    '''
    if n % 2 == 0:
        n += 1
    while not isPrime(n):
        n += 2
    return n

if __name__ == '__main__':
    main()
