from asyncio.tasks import sleep
# from random import uniform
from time import *
from ursinanetworking import *
# from perlin_noise import PerlinNoise
from opensimplex import OpenSimplex
from ursina import Vec3, distance
import asyncio
from json import load, dump

print("Hello from the server !")

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)
state_dict=dict(load(open('../checkpoint.json')))
Blocks = state_dict


def Explosion(position):
    Server.broadcast("Explode", position)
    sleep(1)
    to_destroy = []
    for x in Blocks:
        a = tuple(Blocks[x]["pos"])
        b = tuple(position)
        if distance(Vec3(a), Vec3(b)) < 2:
            to_destroy.append(x)
    for x in to_destroy:
        destroy_block(x)


# Destroy Block Function
def destroy_block(Block_name):
    del Blocks[Block_name]
    # del state_dict[Block_name]
    # dump(state_dict,open('../checkpoint.json','w'))
    Easy.remove_replicated_variable_by_name(Block_name)

# Spawn Block Function
i = 0
def spawn_block(block_type, position,block_name=None, investigator = "client"):
    global i
    if block_name is None:
        print(1)
        block_name = f"blocks_{i}"
    print(block_name)
    Easy.create_replicated_variable(
        block_name,
        { "type" : "block", "block_type" : block_type, "position" : position, "investigator" : investigator}
    )
    
    if block_type == "tnt":
        threading.Thread(target = Explosion, args=(position,)).start()

    Blocks[block_name] = {
        "name" : block_name,
        "pos" : position
    }
    state_dict[block_name]={
        'name':block_name,
        'type':block_type,
        'pos':position
    }
    dump(state_dict,open('../checkpoint.json','w'))
    i += 1

# A little Hello
@Server.event
def onClientConnected(Client):
    Easy.create_replicated_variable(
        f"player_{Client.id}",
        { "type" : "player", "id" : Client.id, "position" : (0, 0, 0) }
    )
    print(f"{Client} connected !")
    Client.send_message("GetId", Client.id)

# A little goodbye
@Server.event
def onClientDisconnected(Client):
    Easy.remove_replicated_variable_by_name(f"player_{Client.id}")

# When a client destroy a block
@Server.event
def request_destroy_block(Client, Block_name):
    print(Block_name)
    destroy_block(Block_name)

# When a client place a block
@Server.event
def request_place_block(Client, Content):
    spawn_block(Content["block_type"], Content["position"])

# Update Player's position
@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)

# tmp = OpenSimplex(0)
# # Create the world
# for x in range(32):
#     for z in range(32):

#         l = round(tmp.noise2(x = x / 5, y = z / 5))

#         if l == -1: spawn_block("sand", (x, l, z), investigator = "server")
#         if l == 0: spawn_block("grass", (x, l, z), investigator = "server")
#         if l == 1: spawn_block("leave", (x, l, z), investigator = "server")


# load world from checkpoint
for k,v in state_dict.items():
    spawn_block(v['type'],v['pos'],k)

while True:
    Easy.process_net_events()