# ds_protocol.py

# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

import socket
import json
import time
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.

DataTuple = namedtuple('response', ['type','message'])

def extract_json(json_msg:str) -> DataTuple:
    """
    Call the json.loads function on a json string and convert it to a DataTuple object  
    """
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        msg = json_obj['response']['message']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(msg_type, msg)


def connect_to_server(host:str, port:int) -> socket.socket:
    """
    Create a socket object and connect to the server
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except:
        return None
    
    
class SMPProtocolError(Exception):
    pass


SMPConnection = namedtuple('SMPConnection',['socket','send','recv'])


def init(sock:socket):
    """
    The init method should be called for every program that uses the SMP Protocol.
    The calling program should first establish a connection with a socket object, then pass
    that open socket to init. init will then create file objects to handle input and output.
    """
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except:
        raise SMPProtocolError("Invalid socket connection")

    return SMPConnection(
        socket = sock,
        send = f_send,
        recv = f_recv
    )


def write_command(smp_conn: SMPConnection, cmd: str):
    """
    performs the required steps to send a message, including
    appending a newline sequence and flushing the socket to ensure
    the message is sent immediately.
    """
    try:
        smp_conn.send.write(cmd + '\n')
        smp_conn.send.flush()
    except:
        raise SMPProtocolError
        

def read_command(smp_conn: SMPConnection):
    """
    performs the required steps to receive a message. Trims the 
    newline sequence before returning
    """
    cmd = smp_conn.recv.readline()[:-1]
    return cmd
    
    
def join(conn_obj, usrn:str, pwd:str):
    """
    Get the username and password then initiate a connection with the ICS 32 DS server
    Return the json messsage and token from the server
    """
    # Initialize a dictionary that follows "join" format
    join_dict = {"join": {"username": usrn,"password": pwd, "token":""}}
    # Convert to string using json.dumps()
    json_join = json.dumps(join_dict)
    # Send the "string dictonary" to the DS server
    write_command(conn_obj, json_join)
    # Get the response
    json_msg = read_command(conn_obj)
    
    # Get the token if successfully connecting to the server
    # Return token = None if fail to connect to the server
    user_token = None
    try:
        json_obj = json.loads(json_msg)
        msg_type = json_obj['response']['type']
        if msg_type == "ok":
            user_token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    
    return json_msg, user_token


def directmessage(conn_obj, user_token:str, message:str, recipient:str):
    """
    Get the token, message and recipient then send the direct message to the ICS 32 DS server
    Return the json messsage 
    """
    dmsg_dict =  {"token": user_token, "directmessage": {"entry": message,"recipient": recipient, "timestamp": time.time()}}
    # Convert a dictionary to JSON
    json_dmsg = json.dumps(dmsg_dict)
    write_command(conn_obj, json_dmsg)
    json_msg = read_command(conn_obj)
    return json_msg


def dm_response(conn_obj, user_token:str, rsp_type:str):
    """
    Get the token, message and recipient then send the direct message to the ICS 32 DS server
    Return the json messsage 
    """
    dm_rsp_dict = {"token": user_token, "directmessage": rsp_type}
    # Convert a dictionary to JSON
    json_dm_rsp = json.dumps(dm_rsp_dict)
    write_command(conn_obj, json_dm_rsp)
    json_msg = read_command(conn_obj)
    return json_msg


def ok(json_msg:str):
    """
    Get the response from the server and output OK message
    """    
    datatuple = extract_json(json_msg)
    if datatuple.type == 'ok':
        output_msg = datatuple.type.upper() + '!! ' + datatuple.message
        print(output_msg)
        return True
    else:
        return False

        
def error(json_msg:str):
    """
    Get the response from the server and output ERROR message
    """    
    datatuple = extract_json(json_msg)
    if datatuple.type == 'error':
        output_msg = datatuple.type.upper() + '!! ' + datatuple.message
        print(output_msg)
        return True
    else:
        return False