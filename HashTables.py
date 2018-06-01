__author__ = 'Dennis Qiu'
import math
import time

load_factors = [0.5, 0.75]
loadFactor = load_factors[0]
ttl_time = 0
search_cnt = 0


def measure_search_time(isbn, hashtbl):
    global ttl_time
    global search_cnt
    start = time.clock()
    print('Searching ISBN {} in library'.format(isbn))
    if isbn in hashtbl:
        print(hashtbl.get(isbn))
        found=True
    else:
        print("Book with this ISBN number is not found in the library.")
        found=False
    stop = time.clock()
    elpSeconds = stop - start
    ttl_time += elpSeconds
    search_cnt += 1 
    print("Search took {:5f} seconds, found: {}, average: {:5f}".format(elpSeconds, found, ttl_time/search_cnt))
    return elpSeconds 
    
def main():
    """ This program hashes Books.txt.
        1. Change the hash function as indicated below.
        2. Change the rehash function as indicated below.
        3. How many times does this hash table make itself bigger (change its size)? 9
        4. Which load factor in the range .5 to .9 in steps of .25 is optimal in the sense
        of least time to build the hash table given a start size of 11 on Books.txt?  ->0.5
            0.5   - 5 second build time
            0.75  - 8 second build time
        5. Which hash works best? 
        The original with a load factor of .5 using  the first character key and linear probing
        or your modified/optimized with steps 1-4 hash?
            original, build:  search:
            modified, build: 5 (0.5 load factor) search average: 0.008853
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
    print("Building hash took {:5f} seconds with load factor of {}".format(stop-start, loadFactor))
    print("Times required to resize {:5d}".format(library.resizes))
    
                
    """
    isbn = 9780821336953
    print('You entered ISBN {}'.format(isbn))
    if isbn in library:
        print(library.get(isbn))
    else:
        print("I couldn't find a book with that ISBN number.'")
    #isbn = int(input('enter ISBN: '))
    isbn = 9781464802027 
    print('You entered ISBN {}'.format(isbn))
    if isbn in library:
        print(library.get(isbn))
    else:
        print("I couldn't find a book with that ISBN number.'")
    print('Return value for library.get({}) is "{}"'.format(isbn,library.get(isbn)))
    """
    
    
    isbns = [9780821336953, 9781464802027, 9781464802126, 9780821350164, 9781464899999] 
    for isbn in isbns:
        measure_search_time(isbn, library)
    
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
            self.resizes += 1
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
                #rehash_cnt = 0
                #nextslot = self.rehash(hashvalue,len(self.slots),rehash_cnt)
                nextslot = self.rehash(hashvalue,len(self.slots))
                #rehash_cnt += 1
                while self.slots[nextslot] != None and \
                                self.slots[nextslot] != key:
                    #nextslot = self.rehash(nextslot,len(self.slots), rehash_cnt)
                    nextslot = self.rehash(nextslot,len(self.slots))
                    #rehash_cnt += 1

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
        '''  
        '''
        s=str(key)
        #print("hashfunction: key {}, size {}, hash {}".format(key, size, (int(s[0]))%size))
        return (int(s[0]))%size
        """
        s1 = int(s[0:4])
        s2 = int(s[4:8])
        s3 = int(s[8:12])
        s = s1 + s2 + s3
        hash = (s1+s2+s3)%size
        #print("hashfunction: size {}, hash {}".format(size, hash))
        return hash 
        """
################################################################################


################################################################################
    ''' Rewrite this rehash function to use quadratic probing.
    '''
    def rehash(self,oldhash,size,rehash_cnt=0):
        return (oldhash+1)%size
        """
        #increments the hash value by 1, 3, 5, 7, 9, and so on
        increments = list(range(1,3*size+1,2)) 
        #print("rehash, cnt {}, size {}, list {}".format(rehash_cnt, size, increments))
        return (oldhash+increments[rehash_cnt])%size
        """
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
