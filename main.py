#this represents the data that would be stored on the actual hard drive for example
physical_disk = {
    0x10000001: 0xFFFFFFFF # For now all of our data will be exactly one word long
}

#We're going to do a word addressable cache

address_size = 32 # address length in bits
offset_size = 5 # bits 0-4
index_size = 7 # bits 5-10
tag_size = 20 # bits 31-11
valid_field_size = 1

block_size = pow(2,offset_size) # Block size in bytes
block_size /= 2 # block size in words
number_blocks = pow(2,index_size) # Number of blocks in the cache

size_of_cache = number_blocks * (block_size + tag_size + valid_field_size)

testAddr = 0x10000001

print ("Create a cache of:",size_of_cache,"words")
print("--------------------------------------")
print ("Cache Block Size:",block_size, "words")
print ("Number of cache blocks:",number_blocks, "blocks")
