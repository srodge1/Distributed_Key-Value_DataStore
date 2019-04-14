import sys
import time
import socket as _sock
import threading as _thr
from datetime import datetime as _dt

sys.path.append('/home/vchaska1/protobuf/protobuf-3.5.1/python')

import replica_pb2
from google.protobuf.internal.encoder import _VarintEncoder
from google.protobuf.internal.decoder import _DecodeVarint


NUM_REPLICAS = 0        # number of all the key-value store replicas
KEYS_RANGE   = '0-255'  # lower-upper (keys range as a string)
REP_FACTOR   = 3        # Replication factor 3 in this case

class Replica():
    def __init__(self):
        self.kv_store       = {} # key(0-255):[value(string), timestamp(str)] ;in memory key-value store
        self.preference_list= {} # 'num-num'(keys_range string):[replica objects(resp for that key range)]
        self.all_replicas   = {} # replica_name:replica object
        self.hint           = {} # {rep_name:{ key:[value, timestamp] }}
        self.replica_list   = [] # To get replicas in order for partitioner_fun. {dict} has no order
        self.read_repair    = None# 0:hinted handoff ; 1:read_repair
        # for kv_store, hint and file data structures only
        self.kv_lock, self.h_lock, self.f_lock = _thr.Lock(), _thr.Lock(), _thr.Lock()
        self.name, self.ip, self.port = None, None, None

    def __str__(self):
        return 'name : {} ip : {} port : {}'.format(self.name, self.ip, self.port)

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


def partitioner_fun(all_replicas):
    """
    """
    if NUM_REPLICAS > 1:
        kr_lower, kr_upper  = int(KEYS_RANGE.split('-')[0]), int(KEYS_RANGE.split('-')[1])
        # getting upper limit of keys_range for the replica. Even distribution
        temp     = (kr_upper-kr_lower+1)//NUM_REPLICAS
        kr_upper = temp - 1

        for i in range(NUM_REPLICAS):
            # key 'kr_lower-kr_upper' for preference_list
            _ = str(kr_lower)+'-'+str(kr_upper)
            #print('\nin part fun low: {} ; up: {}\n'.format(kr_lower, kr_upper))
            # ensures equal and correct distribution of keys. preference_list creation
            for j in range(REP_FACTOR):
                try:
                    cur_replica.preference_list[_] += [cur_replica.all_replicas[
                                                        cur_replica.replica_list[(i+j) % NUM_REPLICAS]]]
                except KeyError:
                    cur_replica.preference_list[_] = [cur_replica.all_replicas[
                                                        cur_replica.replica_list[(i+j) % NUM_REPLICAS]]]
            # reset values of kr_lower and kr_upper
            kr_lower = kr_upper + 1
            kr_upper = kr_lower + temp -1

        #print(''.join('pref list {} : {}'.format(k, v) for k, v in cur_replica.preference_list.iteritems()))

    else:
        cur_replica.preference_list[KEYS_RANGE] = [cur_replica]

# responsible replica, for a particular key, finding function
def res_rep(k_pl):
    """
    input : int (key for preference_list)
    output: str ('int-int', key in preference_list responsible for key_input)
    """
    for each in cur_replica.preference_list:
        kr_low, kr_up = int(each.split('-')[0]), int(each.split('-')[1])
        if kr_low <= k_pl and k_pl <= kr_up:
            return each

# str to ReplicaMessage
def str_rm(r_str):
    """ str to ReplicaMessage """
    temp = replica_pb2.ReplicaMessage()
    temp.ParseFromString(r_str)
    return temp

# ReplicaMessage to string and send
def rm_str_send(r_msg, client):
    """"""
    sr_msg= r_msg.SerializeToString()
    size  = encode_varint(len(sr_msg))
    client.sendall(size+sr_msg)
    return (1)

# ordinary replica putkey (write) operation
def ord_rep_write(init_msg):
    """ input : ReplicaMessage object """
    # if key already exists at replica check timestamp and process
    key = init_msg.put_key.key
    with cur_replica.kv_lock:
        try:
            if cur_replica.kv_store[key][1] < init_msg.put_key.timestamp:
                # Populate write ahead logFile everytime
                with cur_replica.f_lock:
                    with open(cur_replica.name+'_log.txt', 'a') as f_handle:
                        f_handle.write(str(key)+':'+init_msg.put_key.value+'\n')
                    cur_replica.kv_store[key][1] = init_msg.put_key.timestamp
                    cur_replica.kv_store[key][0] = init_msg.put_key.value
                    #print('key: {} put at {} and value is: {}'.format(key, cur_replica.name,
                    #                                            init_msg.put_key.value))
        # elseif key doesn't exist no need to compare timestamp
        except KeyError:
            with cur_replica.f_lock:
                # Populate write ahead logFile everytime # lock is already acquired
                with open(cur_replica.name+'_log.txt', 'a') as f_handle:
                    f_handle.write(str(key)+':'+init_msg.put_key.value+'\n')
                cur_replica.kv_store[key] = [init_msg.put_key.value]
                cur_replica.kv_store[key].append(init_msg.put_key.timestamp)
                # releasing the lock acquired before exception
                #print('key: {} put at {} and value is: {}'.format(key, cur_replica.name,
                #                                        init_msg.put_key.value))
    # except FileNotFoundError should not happen unless some internel os error

# ordinary replica read function for get_key
def ord_rep_read(init_msg):
    """ returns [value, timestamp] if present else [] """
    key = init_msg.get_key.key
    with cur_replica.kv_lock:
        if key in cur_replica.kv_store:
            #print('key: {} read at {} and value is: {}'.format(key, cur_replica.name,
            #                                            cur_replica.kv_store[key]))
            return cur_replica.kv_store[key]
    return []


# cordinator to client response ######### use same for read as well with value=None passed
def cord_client_res(init_msg, n_acks, n_nacks, client, ret_value=[], neg_acks=None, mode='w'):
    """ """
    c_res = replica_pb2.ReplicaMessage()
    # use if mode == 'w' or == 'r' for put_key and get_key
    if mode == 'w':
        # == 2 should be (REP_FACTOR//2)+1 in other cases NUM_REPLICAS != 4
        if ((init_msg.put_key.consistency_level == 'QUORUM' and n_acks == 2) or (
            init_msg.put_key.consistency_level == 'ONE' and n_acks == 1)):
            c_res.cord_response.ack = 1
            return rm_str_send(c_res, client)
        # >= 2 should be (REP_FACTOR//2)+1 in other cases NUM_REPLICAS != 4
        elif ((init_msg.put_key.consistency_level == 'QUORUM' and n_nacks >= 2) or (
            init_msg.put_key.consistency_level == 'ONE' and n_nacks == 3)):
            c_res.cord_response.ack = 0
            return rm_str_send(c_res, client)
    # for get_key response to the client from cordinator
    elif mode == 'r':
        #print('Inside cord_client_res neg_acks: {}, acks: {}, nacks: {} at {}'.format(neg_acks, n_acks,
        #                                                            n_nacks, cur_replica.name))
        # == 2 should be (REP_FACTOR//2)+1 in other cases NUM_REPLICAS != 4
        if ((init_msg.get_key.consistency_level == 'QUORUM' and n_acks == 2) or (
            init_msg.get_key.consistency_level == 'ONE' and n_acks == 1)):
            c_res.cord_response.value_present = 1
            c_res.cord_response.value         = ret_value[0]
            return rm_str_send(c_res, client)
        # >= 2 should be (REP_FACTOR//2)+1 in other cases NUM_REPLICAS != 4
        elif ((init_msg.get_key.consistency_level == 'QUORUM' and n_nacks >= 2) or (
            init_msg.get_key.consistency_level == 'ONE' and n_nacks == 3 and n_acks == 0)):
            c_res.cord_response.value_present = 0
            return rm_str_send(c_res, client)
        # if value present in replicas less than consistency_level client should receive an exception
        elif ((init_msg.get_key.consistency_level == 'QUORUM' and neg_acks >= 2) or (
            init_msg.get_key.consistency_level == 'ONE' and neg_acks == 3 and n_acks == 0)):
            c_res.cord_response.value_present = 2
            return rm_str_send(c_res, client)
    return (0)

# Achieve eventual consistency by hinted handoff #assuming related replica doesn't go down
def hinted_handoff(r_name):
    #create a new connection so that a new thread is created at that replica and won't interfere
    h_socket = _sock.create_connection((cur_replica.all_replicas[r_name].ip,
                                        cur_replica.all_replicas[r_name].port))
    h_msg    = replica_pb2.ReplicaMessage()
    h_msg.put_key.from_rep      = cur_replica.name
    h_msg.put_key.from_client   = 0
    with cur_replica.h_lock:
        # getting keys and values from cur_replica hint and sending it to the cordinator invoking this
        for _ in cur_replica.hint[r_name]:
            h_msg.put_key.key       = _
            h_msg.put_key.value     = cur_replica.hint[r_name][_][0]
            h_msg.put_key.timestamp = cur_replica.hint[r_name][_][1]
            result = rm_str_send(h_msg, h_socket)
            h_res  = recv_fun(h_socket)
            # put request is succesful unless replica goes down again
            if h_res.replica_response.is_updated == 1:
                pass
        # remove this replicas name from the cur_replica's hint
        del cur_replica.hint[r_name]


# Achieve eventual consistency by read_repair
def read_repair(r_val, rr_list, k_pl, key):
    #print('======= inside read repair============')
    for _ in cur_replica.preference_list[k_pl]:
        if cur_replica.name != _.name:
            #create a new connection so that a new thread is created at that replica and won't interfere
            h_socket = _sock.create_connection((_.ip, _.port))
            h_msg    = replica_pb2.ReplicaMessage()
            h_msg.put_key.from_rep      = cur_replica.name
            h_msg.put_key.from_client   = 0
            h_msg.put_key.key       = key
            h_msg.put_key.value     = r_val[0]
            h_msg.put_key.timestamp = r_val[1]
            result = rm_str_send(h_msg, h_socket)
            h_res  = recv_fun(h_socket)
            # put request is succesful unless replica goes down again
            if h_res.replica_response.is_updated == 1:
                pass
        else:
            with cur_replica.kv_lock:
                try:
                    cur_replica.kv_store[key][0] = r_val[0]
                    cur_replica.kv_store[key][1] = r_val[1]
                except KeyError:
                    cur_replica.kv_store[key] = [r_val[0]]
                    cur_replica.kv_store[key].append(r_val[1])


def handle_msgs(client, addr):
    """
    """
    t_exit_loop = 0
    while True:
        try:
            init_msg = recv_fun(client)
        except:
            t_exit_loop = 1
        # if client terminated kill the thread
        if t_exit_loop == 1:
            break

        if init_msg.HasField('put_key'):
            # might need to use a lock, see later ("%d/%m/%y %H:%M:%S:%f")
            key = init_msg.put_key.key
            if init_msg.put_key.from_client == 1:
                # for corinator section # connect to all other replicas res for this key
                k_pl = res_rep(key)
                # put_key msg to be sent by cordinator to all the responsible replicas
                c_msg = replica_pb2.ReplicaMessage()
                c_msg.CopyFrom(init_msg)
                # timestamp in string can be compared well
                c_msg.put_key.timestamp   = _dt.now().strftime("%d/%m/%y %H:%M:%S:%f")
                c_msg.put_key.from_client = 0
                c_msg.put_key.from_rep    = cur_replica.name
                sc_msg                    = c_msg.SerializeToString()
                size                      = encode_varint(len(sc_msg))

                n_nacks, n_acks, res_sent = 0, 0, 0 # nacks when replicas are down
                for replica in cur_replica.preference_list[k_pl]:
                    if replica.name != cur_replica.name:
                        # check if the replica is up. if not see if consistancy level is achieved if yes send
                        # ...ack otherwise send nack
                        try:
                            c_socket = _sock.create_connection((replica.ip, replica.port))
                            c_socket.sendall(size+sc_msg)
                            sr_res   = recv_fun(c_socket)
                            r_res    = sr_res
                            ####################################################
                            # hints at this cordinator can also be checked and sent if present
                            # ...make a function
                            ####################################################
                            # don't even need to do this if statement
                            c_socket.close()
                            #print('----------received rep res : {}'.format(client))
                            if r_res.replica_response.is_updated == 1:
                                n_acks += 1
                                if res_sent == 0:
                                    # fun to prepare cord resp based on acks and nacks use in GetKey as well
                                    res_sent = cord_client_res(init_msg, n_acks, n_nacks, client)
                        except _sock.error:
                            # Store this in the hinted handoff data structure
                            if cur_replica.read_repair == 0:
                                with cur_replica.h_lock:
                                    if replica.name in cur_replica.hint:
                                        try:
                                            if cur_replica.hint[replica.name][key][1] < c_msg.put_key.timestamp:
                                                cur_replica.hint[replica.name][key][1] = c_msg.put_key.timestamp
                                                cur_replica.hint[replica.name][key][0] = c_msg.put_key.value
                                        except KeyError:
                                            cur_replica.hint[replica.name][key] = [c_msg.put_key.value,
                                                                                    c_msg.put_key.timestamp]
                                    else:
                                        cur_replica.hint[replica.name] = {key:[c_msg.put_key.value,
                                                                                    c_msg.put_key.timestamp]}

                            n_nacks += 1
                            # if consistency_level requirements are met send the acknowledgement
                            if res_sent == 0:
                                res_sent = cord_client_res(init_msg, n_acks, n_nacks, client)

                    elif replica.name == cur_replica.name:
                        ord_rep_write(c_msg)
                        n_acks += 1
                        # if consistency_level requirements are met send the acknowledgement
                        if res_sent == 0:
                            res_sent = cord_client_res(init_msg, n_acks, n_nacks, client)

            else:
                # should check if there are any hints in cur_replica for the coming cordinatormsg
                #......if yes send this value else pass (see carefully)
                if cur_replica.read_repair == 0:
                    if init_msg.put_key.from_rep in cur_replica.hint:
                        name = init_msg.put_key.from_rep
                        th  = _thr.Thread(target=hinted_handoff, args=(name,), name=('hh_'+cur_replica.name))
                        th.daemon = False
                        th.start()
                # for ordinary replica
                ord_rep_write(init_msg)
                # After write operation is done prepare ReplicaMessage to the cordinator
                r_msg = replica_pb2.ReplicaMessage()
                r_msg.replica_response.is_updated = 1
                sr_msg= r_msg.SerializeToString()
                size  = encode_varint(len(sr_msg))
                client.sendall(size+sr_msg)
                # kill the connection from cordinator, only client-cordinator con should be alive
                break


        elif init_msg.HasField('get_key'):
            # check if this msg is from client or other replica and work accordingly change for more replicas
            key = init_msg.get_key.key
            if init_msg.get_key.from_client == 1:
                # for corinator section # connect to all other replicas res for this key
                k_pl = res_rep(key)
                # get_key msg to be sent by cordinator to all the responsible replicas
                c_msg = replica_pb2.ReplicaMessage()
                c_msg.CopyFrom(init_msg)
                # timestamp in string can be compared well
                c_msg.get_key.from_client = 0
                c_msg.get_key.from_rep    = cur_replica.name
                sc_msg                    = c_msg.SerializeToString()
                size                      = encode_varint(len(sc_msg))
                # acks:if present ; nacks : not present ; neg_acks : replica down ; ret_value[val, time]:return val
                # rr_list stores replica names with consistent and inconsistent data
                n_nacks, n_acks, neg_acks, res_sent, ret_value, rr1, rr2 = 0, 0, 0, 0, [], [], []
                for replica in cur_replica.preference_list[k_pl]:
                    if replica.name != cur_replica.name:
                        # check if the replica is up. if not see if consistancy level is achieved if yes send
                        # ...ack otherwise send nack
                        try:
                            c_socket = _sock.create_connection((replica.ip, replica.port))
                            c_socket.sendall(size+sc_msg)
                            r_res   = recv_fun(c_socket)
                            c_socket.close()
                            #print('----------received rep res : {}'.format(client))
                            if r_res.replica_response.value_present == 1:
                                n_acks += 1
                                if ret_value == []:
                                    ret_value.append(r_res.replica_response.value)
                                    ret_value.append(r_res.replica_response.timestamp)
                                    rr1.append(r_res.replica_response.from_rep)
                                else:
                                    if ret_value[1] < r_res.replica_response.timestamp:
                                        ret_value[0] = r_res.replica_response.value
                                        ret_value[1] = r_res.replica_response.timestamp
                                        # add to rr2 since rr1 replicas are inconsistent
                                        for _ in rr1:
                                            rr2.append(_)
                                        # flush rr1 since inconsistent
                                        rr1 = [r_res.replica_response.from_rep]
                                    elif ret_value[1] > r_res.replica_response.timestamp:
                                        rr2.append(r_res.replica_response.from_rep)
                                    elif ret_value[1] == r_res.replica_response.timestamp:
                                        # for == append rep_name to rr_list
                                        rr1.append(r_res.replica_response.from_rep)

                            elif r_res.replica_response.value_present == 0:
                                n_nacks += 1
                                rr2.append(r_res.replica_response.from_rep)
                            # prepare for cordinator response on meeting recquirements
                            if res_sent == 0:
                                # fun to prepare cord resp based on acks and nacks use in GetKey as well
                                cord_client_res(init_msg, n_acks, n_nacks, client,
                                                ret_value=ret_value, neg_acks=neg_acks, mode='r')

                        except _sock.error:
                            neg_acks += 1
                            # if consistency_level requirements are met send the acknowledgement
                            if res_sent == 0:
                                res_sent = cord_client_res(init_msg, n_acks, n_nacks, client,
                                                ret_value=ret_value, neg_acks=neg_acks, mode='r')

                    elif replica.name == cur_replica.name:
                        #print('==== key {} requested at {} and kv_store'.format(key, cur_replica.name,
                        #                                            cur_replica.kv_store))
                        t_val = ord_rep_read(c_msg)
                        if t_val == []:
                            n_nacks += 1
                            rr2.append(cur_replica.name)
                            # value not present here and other replicas are down
                            neg_acks += 1
                        else:
                            n_acks += 1
                            if ret_value == []:
                                ret_value.append(t_val[0])
                                ret_value.append(t_val[1])
                                rr1.append(cur_replica.name)
                            else:
                                if ret_value[1] < t_val[1]:
                                    ret_value[0] = t_val[0]
                                    ret_value[1] = t_val[1]
                                    # add to rr2 since rr1 replicas are inconsistent
                                    for _ in rr1:
                                        rr2.append(_)
                                    # flush rr1 since inconsistent
                                    rr1 = []
                                # for >= and < append rep_name to rr_list
                                rr1.append(cur_replica.name)
                        # if consistency_level requirements are met send the acknowledgement
                        if res_sent == 0:
                            res_sent = cord_client_res(init_msg, n_acks, n_nacks, client,
                                            ret_value=ret_value, neg_acks=neg_acks, mode='r')

                ######################check here for read repair
                #print("rr1 : {}, rr2 : {}, ret_value : {}".format(rr1, rr2, ret_value))
                if (cur_replica.read_repair == 1 and ret_value != [] and rr2 != []):
                    th  = _thr.Thread(target=read_repair, args=(ret_value, rr2, k_pl, key),
                                        name=('rr_'+cur_replica.name))
                    th.start()

            else:
                #should check if there are any hints in cur_replica for the coming cordinatormsg
                #......if yes send those hints else pass (see carefully)
                if cur_replica.read_repair == 0:
                    if init_msg.get_key.from_rep in cur_replica.hint:
                        name = init_msg.get_key.from_rep
                        th  = _thr.Thread(target=hinted_handoff, args=(name,), name=('hh_'+cur_replica.name))
                        th.daemon = False
                        th.start()
                # for ordinary replica
                r_msg = replica_pb2.ReplicaMessage()
                t_val = ord_rep_read(init_msg)
                # After read operation is done prepare ReplicaMessage to the cordinator
                if t_val == []:
                    r_msg.replica_response.value_present = 0
                else:
                    r_msg.replica_response.value_present = 1
                    r_msg.replica_response.from_rep      = cur_replica.name
                    r_msg.replica_response.value         = t_val[0]
                    r_msg.replica_response.timestamp     = t_val[1]

                sr_msg= r_msg.SerializeToString()
                size  = encode_varint(len(sr_msg))
                client.sendall(size+sr_msg)
                # kill the connection from cordinator, only client-cordinator con should be alive
                break



if __name__ == '__main__':
    cur_replica = Replica() # on start before checking log file create the Replica object
    cur_replica.name = sys.argv[1]
    cur_replica.ip   = _sock.gethostbyname(_sock.gethostname())
    cur_replica.port = int(sys.argv[2])
    # 3rd argument is responsible for setting read_repair or hinted handoff
    if sys.argv[3] == 'r':
        cur_replica.read_repair = 1
    elif sys.argv[3] == 'h':
        cur_replica.read_repair = 0
    else:
        print('Provide 3rd arg as r for read_repair and h for hinted handoff and run again')
        sys.exit(1)
    #try openning corresponding logFile to recover if crashed else do nothing present means crashed recently
    file_name = cur_replica.name+'_log.txt'
    try:
        with open(file_name, 'r') as f_handle:
            # read from this file and populate the key-value data-structure pattern('key:value'\n)
            for _ in f_handle:
                line     = _.split(':')
                #print(line)
                key, val = int(line[0]), line[1].rstrip('\n')
                cur_replica.kv_store[key] = [val]
                cur_replica.kv_store[key].append('')
                #print(cur_replica.kv_store[key])
                #will store recent only since we are writting to file in append mode
    except IOError:
        pass
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
                cur_replica.replica_list.append(rep.name)
                cur_replica.all_replicas[rep.name] = rep
                NUM_REPLICAS += 1
    except IOError:
        print('No replicas.txt file to get replicas information from! \nShutting down ....')
        sys.exit(1)

    # calling partitioner_fun to distribute the keys evenly
    partitioner_fun(cur_replica.all_replicas)
    # create a socket and listen
    # since it is TCP i'm using SOCK_STREAM. for UDP use SOCK_DGRAM. the protocol is defaulted to 0(3rd parameter).
    l_socket = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
    l_socket.bind(('', cur_replica.port))
    l_socket.listen(5)
    # Until init msg is received main thread is blocked here.
    while True:
        client, addr = l_socket.accept()
        # Creating a thread to handle each received message
        th  = _thr.Thread(target=handle_msgs, args=(client, addr), name=('rt_'+cur_replica.name))
        th.daemon = True
        th.start()
        #handle_msgs(client, addr)
