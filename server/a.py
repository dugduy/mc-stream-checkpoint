from random import randint,choice
from opensimplex import OpenSimplex
from json import dump

Blocks={}
i=0

def spawn_block(block_type, position,block_name=None, investigator = "client"):
    global i
    if block_name is None:
        print(1)
        block_name = f"blocks_{i}"
    print(block_name)

    Blocks[block_name] = {
        "name" : block_name,
        'type':block_type,
        "pos" : position
    }
    dump(Blocks,open('../checkpoint.json','w'))
    i+=1

# tmp = OpenSimplex(0)
# # Create the world
# for x in range(32):
#     for z in range(32):

#         l = round(tmp.noise2(x = x / 5, y = z / 5))
#         print(l)

#         if l == -1: spawn_block("sand", (x, l, z), investigator = "server")
#         if l == 0: spawn_block("grass", (x, l, z), investigator = "server")
#         if l == 1: spawn_block("leave", (x, l, z), investigator = "server")

for x in range(10):
    for z in range(10):
        l = randint(-1,1)

        if l == -1: spawn_block(choice(("sand",'stone')), (x, l, z), investigator = "server")
        elif l == 0: spawn_block(choice(("grass",'stone')), (x, l, z), investigator = "server")
        elif l == 1: spawn_block(choice(("leave",'stone')), (x, l, z), investigator = "server")
        else:
            spawn_block(choice(("glass",'leave')), (x, l, z), investigator = "server")