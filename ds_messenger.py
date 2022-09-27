import input_check
import ds_protocol
import json
PORT = 3021

class DirectMessage:
    def __init__(self, recipient=None, message=None, timestamp=None):
        self.recipient = recipient
        """The recipient"""
        self.message = message
        """The message to communicate between users"""
        self.timestamp = timestamp
        """The time as a floating point number expressed in seconds"""


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        """Token is available if sucessfully connecting to the server. It is used for send(), retrieve_new(), retrieve_all()"""
        self.dsuserver = dsuserver
        """The server location to connect"""
        self.username = username
        """The username to join the server"""
        self.password = password
        """The password to join the server"""
        self._is_connected = False
        """The attribute to check if sucessfully connecting to the server"""
        self._conn_obj = None
        """The object to set-up the connection with the server"""
        self._join_server(dsuserver, username, password)
        """Private method to join the server"""
        
        
    def _join_server(self,dsuserver:str, username:str, password:str):
        """Check if the user inputs are valid then join the server and get the token"""
        # Check if user inputs are valid
        # Return True/False
        server_bool = input_check.is_valid_ip(dsuserver)
        usn_bool = input_check.is_valid_usr_pwd(username, 'username')
        pwd_bool = input_check.is_valid_usr_pwd(password, 'password')
        
        is_valid_user_inputs = all([server_bool, usn_bool, pwd_bool])
        
        # If all user inputs are valid then set-up a connection to the server
        if is_valid_user_inputs:
            try:
                # Create a socket object then connection object
                sock = ds_protocol.connect_to_server(dsuserver, port=3021)
                conn_obj = ds_protocol.init(sock)
                # Join the server
                join_rsp, token = ds_protocol.join(conn_obj, username, password)
                # Check if the type of response is ok
                if ds_protocol.ok(join_rsp) and (not ds_protocol.error(join_rsp)):
                    self.token = token
                    self._conn_obj = conn_obj
                    self._is_connected = True
            except:
                print('One of the information you provide is not in the correct form to connect to the server')
                
        
    def send(self, message:str, recipient:str)-> bool:
        """Send a directmessage wih a recipient to the server"""
        if ((self.token is not None) and (self._is_connected == True)):
            try:   
                # Send the input message to the server
                direct_msg_rsp = ds_protocol.directmessage(self._conn_obj, self.token, message, recipient)
                # Check if the type of response is ok
                if ds_protocol.ok(direct_msg_rsp) and (not ds_protocol.error(direct_msg_rsp)): 
                        return True
                else:
                    return False
            except:
                print('One of the information you provide is not correct. Unable to send the message')
                return False
        else:
            return False
    
    
    def retrieve_new(self) -> list:
        """ Get new directmessages and store each directmessage in a DirectMessage object. Return a list of DirectMessage objects""" 
        new_msg_lst = []
        if ((self.token is not None) and (self._is_connected == True)):
            try:   
                new_msg_rsp = ds_protocol.dm_response(self._conn_obj, self.token, "new")
                # Convert the response object to a dictionary
                json_obj = json.loads(new_msg_rsp)
                # Check if the type of response is ok
                if json_obj['response']['type'] == 'ok': 
                    new_messages = json_obj['response']['messages']
                    # store each directmessage in a DirectMessage object
                    # then group all that objects in a list
                    for msg in new_messages:
                        dm_obj = DirectMessage(recipient=msg['from'],message=msg['message'],timestamp=msg['timestamp'])
                        new_msg_lst.append(dm_obj)
                        
                return new_msg_lst
            except:
                print('One of the information you provide is not correct or the connection to server cannot be established. Unable to retrieve the message') 
            
            
    def retrieve_all(self) -> list:
        """ Get all directmessages and store each directmessage in a DirectMessage object. Return a list of DirectMessage objects""" 
        all_msg_lst = []
        if ((self.token is not None) and (self._is_connected == True)):
            try:   
                all_msg_rsp = ds_protocol.dm_response(self._conn_obj, self.token, "all")
                # Convert the response object to a dictionary
                json_obj = json.loads(all_msg_rsp)
                # Check if the type of response is ok
                if json_obj['response']['type'] == 'ok': 
                    all_messages = json_obj['response']['messages']
                    # store each directmessage in a DirectMessage object
                    # then group all that objects in a list   
                    for msg in all_messages:
                        dm_obj = DirectMessage(recipient=msg['from'],message=msg['message'],timestamp=msg['timestamp'])
                        all_msg_lst.append(dm_obj)
                        
                return all_msg_lst
            except:
                print('One of the information you provide is not correct or the connection to server cannot be established. Unable to retrieve the message') 