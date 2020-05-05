import sys
import socket
import asyncio

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from lru_cache import lru_cache
from BloomFilter import BloomFilter

BUFFER_SIZE = 1024
bloomfilter = BloomFilter(50,3)

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


hash_codes = set()


# put functionality
@lru_cache(5)
def put(key, value):
    print("BBLLOOOOOOMMMMMM")
    bloomfilter.add(key)
    print("keep in bloom filter")
    #return bloomfilter.add(key)
    #data_bytes, key = serialize_PUT(u)
    #response = ring.get_node(key).send(data_bytes)\
    #hash_codes.add(str(response.decode()))
    #return key


# get functonality
@lru_cache(5)
def get(key):
    print("get from LRu")


#delete functionality
@lru_cache(5)
def delete(key):
    print("in deleete")


def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    #hash_codes = set()
    # PUT all users.
    for u in USERS:
        #put(u, client_ring)
        data_bytes, key = serialize_PUT(u)
        put(key, u)
        response = client_ring.get_node(key).send(data_bytes)
        print(response)
        hash_codes.add(str(response.decode()))

    print(
        f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}"
    )

    # GET all users.
    for hc in hash_codes:
        print(hc)
        res = get(hc)
        if (res == -1):
            print("should check in bloom filter")
            print("If not in bloom filter not found")
        else:
            print("from LRU cache")
            print(res)
        #print(hc)
        #data_bytes, key = serialize_GET(hc)
        #response = client_ring.get_node(key).send(data_bytes)
        #print(response)

    #Delete all users
    for hc in hash_codes:
        delete(hc)
        """print(hc)
        data_bytes, key = serialize_DELETE(hc)
        server_details = client_ring.get_node(key)
        response = server_details.send(data_bytes)
        print(response)"""


if __name__ == "__main__":
    clients = [UDPClient(server['host'], server['port']) for server in NODES]
    process(clients)
