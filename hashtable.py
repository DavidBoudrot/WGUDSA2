class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, key):
        return sum([ord(c) for c in key]) % self.size




    # Takes the sum of ascii values then mods by size of table
    # That gives us the index of the value to lookup
# So here is the insert method that will insert a key value pair into the table
# If they key already exists the value will be replaced.
# Because we are looping through the list its O(n) for the worst case.
# The bucket is the list at the index of the hash key
# This makes it so we can have multiple values at the same index


    #Big O is O(n)


    def insert(self, key, value):
        hash_key = self.hash(key)
        bucket = self.table[hash_key]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    #Big O is O(n)
    def lookup(self, key):
        hash_key = self.hash(key)
        bucket = self.table[hash_key]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    #Big O is O(n)
    def contains(self, address):
        for i in range(len(self.table)):
            if self.table[i] == address:
                return True

    def __iter__(self):
        for bucket in self.table:
            for k, v in bucket:
                yield v



