import sys
import socket
import asyncio

from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from lru_cache import lru_cache
from bloom_filter import BloomFilter

BUFFER_SIZE = 1024


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
itemCount = len(USERS)
bloomfilter = BloomFilter(itemCount, 0.05)


# put functionality
def put(key, value):
    bloomfilter.add(key)
    client_ring = NodeRing(clients)
    data_bytes, key1 = serialize_PUT(value)
    response = client_ring.get_node(key1).send(data_bytes)
    print(response)
    hash_codes.add(str(response.decode()))
    return response


# get functonality
@lru_cache(5)
def get(key):
    if (bloomfilter.is_member(key)):
        print("Found in bloom filter, fetching from server")
        data_bytes, key1 = serialize_GET(key)
        client_ring = NodeRing(clients)
        response = client_ring.get_node(key1).send(data_bytes)
        print(response)
        return response
    else:
        return None


#delete functionality
def delete(key):
    if (bloomfilter.is_member(key)):
        data_bytes, key1 = serialize_DELETE(key)
        client_ring = NodeRing(clients)
        server_details = client_ring.get_node(key1)
        response = server_details.send(data_bytes)
        #print(response)
        return response
    else:
        return None


def process(udp_clients):
    client_ring = NodeRing(udp_clients)
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        put(key, u)

    print(
        f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}"
    )

    # GET all users.
    for hc in hash_codes:
        print(hc)
        get(hc)

    #Delete all users
    for hc in hash_codes:
        delete(hc)


if __name__ == "__main__":
    clients = [UDPClient(server['host'], server['port']) for server in NODES]
    process(clients)
