#this represents the data that would be stored on the actual hard drive for example
physical_disk = {
    0x11010101: 0xFF00e0FF,
    0x10000001: 0xFF00FFFF, # For now all of our data will be exactly one word long
    0x10020001: 0xFF0000FF # For now all of our data will be exactly one word long

}

def print_disk_content(disk):
    print(" -------------------------")
    for key, value in disk.items():
        print("|",format(key,"#02x"),"|",format(value,"#02x"),"|")
    print(" -------------------------")

def print_cache(cache):
    print("v  ","tag        ","block")

    print()
    for i in range(len(cache)):
        print("|",cache[i][0],"|",cache[i][1],"|",cache[i][2],"|")

    print()

def load_from_disk(addr,cache):
    data = physical_disk[addr]
    off = (addr & 0b00000000000000000000000000011111)
    idx = (addr & 0b00000000000000000000111111100000)
    tag = (addr & 0b11111111111111111111000000000000)
    addr_to_proc_min = idx + tag
    addr_to_proc_max = addr_to_proc_min + 0b11111
    print("Loading block from",addr_to_proc_min,"to",addr_to_proc_max)
    for i in range(0b11111):
        val = physical_disk.get(addr_to_proc_min + i)
        # print(len(cache[idx >> 5][2]) - i,0b11111)
        if(val != None):
            cache[idx >> 5][2][i] = val
        else:
            cache[idx >> 5][2][i] = 0xFFFFFFFF

    cache[idx>>5][0] = 1 # set the valid bit
    cache[idx>>5][1] = tag >> (5 + 7) # set the tag


def load(addr, cache):
    print("Loading", format(addr,"#02x"), "from cache")
    off = (addr & 0b00000000000000000000000000011111)
    idx = (addr & 0b00000000000000000000111111100000) >> 5
    tag = (addr & 0b11111111111111111111000000000000) >> (5+7)
    # print("tag",tag)
    # print(cache[idx][1])
    if(cache[idx][0] == 0):
        print("invalid data... loading from disk")
        load_from_disk(addr,cache)
        return cache[idx][2][off]

    elif(cache[idx][1] == tag and cache[idx][0] == 1):
        print("matching tag... returning data")
        return cache[idx][2][off]
    else:
        print("wrong tag... loading from disk")
        load_from_disk(addr,cache)
        return cache[idx][2][off]


    # print(idx)

#We're going to do a word addressable cache

address_size = 32 # address length in bits
offset_size = 5 # bits 0-4
index_size = 7 # bits 5-10
tag_size = 20 # bits 31-11
valid_field_size = 1

block_size = pow(2,offset_size) # Block size in bytes
# block_size = (int)(block_size/2) # block size in words
number_blocks = pow(2,index_size) # Number of blocks in the cache    a =physical_disk[addr]

size_of_cache = number_blocks * (block_size + tag_size + valid_field_size)

testAddr = 0x10000001

cache = [[0,0,[0 for y in range(block_size)]] for x in range(number_blocks)]


#print_cache(cache)

print("Create a cache of:",size_of_cache,"bytes?")
print("--------------------------------------")
print("Cache Block/line Size:",block_size, "words")
print("Number of cache block/lines:",number_blocks, "blocks")
print()
print("Data stored on disk:")
print_disk_content(physical_disk)
print("---------Loading data from cache-----------")
print("Loading data from addr: ",format(testAddr,"#02x"))
print("Data loaded:",format(load(testAddr,cache),"#02x"))
print("Data loaded:",format(load(testAddr,cache),"#02x"))
print("Data loaded from diff addr:",format(load(0x11010101,cache),"#02x"))
print("Data loaded from different addr:",format(load(0x10020001,cache),"#02x")) # this is in the same block, so it has to dump the cache and reload data
print_cache(cache)
