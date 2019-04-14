import sys
import socket as _sock
from replica import Replica

sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

import replica_pb2
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint

def encode_varint(value):
    """ Encode an int as a protobuf varint """
    data = []
    _VarintEncoder()(data.append, value, False)
    return b''.join(data)


def decode_varint(data):
    """ Decode a protobuf varint to an int """
    return _DecodeVarint(data, 0)[0]

def recv_fun(client):
    data = b''
    while True:
        try:
            data += client.recv(1)
            size = decode_varint(data)
            break
        except IndexError:
            pass
    # if recv keeps throughing error. use data=[], in loop append to data received msg. Then ''.join(data)
    data = []
    while True:
        try:
            msg  = client.recv(size)
            data.append(msg)
            msg  = ''.join(data)
            init_msg = replica_pb2.ReplicaMessage()
            init_msg.ParseFromString(msg)
            break
        except:
            pass
    return init_msg


def handle_cord(cord_socket):
    while True:
        cmd = raw_input('\nEnter your command. For ex. GetKey / PutKey / exit(to stop the client) : ')
        if cmd.lower() == 'getkey':
            key   = int(raw_input('Please enter the key(should be between 0 and 255) : '))
            c_lev = raw_input('Please enter the consistency level (Quorum or one) : ')
            # take consistancy level as input too. later
            client_msg = replica_pb2.ReplicaMessage()
            client_msg.get_key.key          = key
            client_msg.get_key.from_client  = 1
            client_msg.get_key.consistency_level = c_lev.upper()
            serialized_client_msg           = client_msg.SerializeToString()
            # sending this msg to the cordinator
            size = encode_varint(len(serialized_client_msg))
            cord_socket.sendall(size+serialized_client_msg)

            cord_res        = recv_fun(cord_socket)
            c_response   = cord_res
            # See what to do with == 2 and 0 later
            if c_response.cord_response.value_present == 0:
                print('The value for your key : {} is not present on any of the replicas!'.format(key))

            elif c_response.cord_response.value_present == 1:
                print('The value corresponding to the key {} is : {}'.format(key,
                        c_response.cord_response.value))
            # value present on less than 3 servers. Through an error. Raise()
            elif c_response.cord_response.value_present == 2:
                print('The value for given key {} is present on less than recquired replicas'.format(key))


        elif cmd.lower() == 'putkey':
            key   = int(raw_input('Please enter the key(should be between 0 and 255) : '))
            value = raw_input('Please enter the value associated with this key : ')
            c_lev = raw_input('Please enter the consistency level (Quorum or one) : ')
            # take consistancy level as input too. later
            client_msg = replica_pb2.ReplicaMessage()
            client_msg.put_key.key          = key
            client_msg.put_key.value        = value
            client_msg.put_key.from_client  = 1
            client_msg.put_key.consistency_level = c_lev.upper()
            serialized_client_msg           = client_msg.SerializeToString()
            size = encode_varint(len(serialized_client_msg))
            # sending this msg to the cordinator
            cord_socket.sendall(size+serialized_client_msg)
            # use try cath block here in case the cordinator goes down before replying
            cord_res     = recv_fun(cord_socket)
            c_response   = cord_res
            # See what to do with this later
            if c_response.cord_response.ack == 0:
                print('Your write request was unsuccessful !')
                # raise error???????????
            elif c_response.cord_response.ack == 1:
                print('Your write request has been prosessed successfully with consistency level {}!'.format(
                                                                                                c_lev.upper()))

        elif cmd.lower() == 'exit':
            print('Client shutting down ......')
            sys.exit(1)

        else:
            print('Not a valid choice. please try again!')



if __name__ == '__main__':
    all_replicas = {}
    replica_list = []
    # Creating a server socket with soket_family AF_INET and socket_type SOCK_STREAM
    # since it is TCP i'm using SOCK_STREAM. for UDP use SOCK_DGRAM. the protocol is defaulted to 0(3rd parameter).
    c_socket = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
    # try catch block can be used if no port available. not the case here
    c_socket.bind(('', 0))
    # open the replicas.txt file and get the details about other_replicas to connect
    try:
        with open('replicas.txt', 'r') as f_handle:
            # readlines is slower useing this instead
            for line in f_handle:
                temp = line.split()
                rep  = Replica()
                rep.name = temp[0]
                rep.ip   = temp[1]
                rep.port = int(temp[2].rstrip('\n'))
                all_replicas[rep.name] = rep
                replica_list.append(rep.name)
    except IOError:
        print('No replicas.txt file to get replicas information from! \nShutting down ....')
        sys.exit(1)

    # Let client decide the co-ordiantor
    for i in range(len(replica_list)):
        print('Press {} to choose {} as the co-ordinator.'.format((i+1), replica_list[i]))
    # input from command line by client
    cord = (int(raw_input('Enter your choice here : ')) - 1)
    try:
        conn = _sock.create_connection((all_replicas[replica_list[cord]].ip,
                                        all_replicas[replica_list[cord]].port))
    except _sock.error:
        print('unable to create connection with selected co-ordinator.')
        print('Maybe the cordinator is down or you entered wrong choice.\nExiting ....')
        sys.exit(1)
    # handle communication to the cordinator
    handle_cord(conn)
