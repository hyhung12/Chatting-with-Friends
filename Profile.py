# Profile.py
# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523
#
# ICS 32 Fall 2021
# Assignment #2: Journal
#
# Author: Mark S. Baldwin
#
# v0.1.7

import json, time, os
from pathlib import Path


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Message(dict):
    """ 
    The Message class is responsible for working with individual messages. It currently supports three features: 
    A timestamp property that is set upon instantiation and when the entry object is set
    An entry property that stores the DirectMessage's message
    A recipient property that stores the contact
    """
    def __init__(self, recipient:str = None, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_recipient(recipient)
        self.set_entry(entry)

        # Subclass dict to expose Message properties for serialization
        dict.__init__(self, recipient=self._recipient, entry=self._entry, timestamp=self._timestamp)
        
    def set_recipient(self, recipient):
        """Assign a value to the recipient"""
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)
        
    def get_recipient(self) -> str:
        """Return the recipient"""
        return self._recipient
    
    def set_entry(self, entry):
        """Assign a value to the entry"""
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self) -> str:
        """Return the entry"""
        return self._entry
        
    
    def set_time(self, time:float):
        """Assign a value to the timestamp"""
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self) -> float:
        """Return the timestamp"""
        return self._timestamp

    """
    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.
    """
    recipient = property(get_recipient, set_recipient)
    """The recipient"""
    entry = property(get_entry, set_entry)
    """The content of message"""
    timestamp = property(get_time, set_time)
    """The time as a floating point number expressed in seconds"""
    
    
class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server
    """
    def __init__(self, dsuserver:str=None, username:str=None, password:str=None):
        self.dsuserver = dsuserver # REQUIRED
        """The server address"""
        self.username = username # REQUIRED
        """ The username to join the server"""
        self.password = password # REQUIRED
        """ The username to join the server"""
        self._contacts = []       # OPTIONAL
        """ The list to store contacts"""
        self._msgs = []            # OPTIONAL
        """ The list to store Message objects"""

        

    def add_contact(self, contact: str) -> None:
        """
        add_conntact accepts a Message as parameter and appends it to the messages list
        """
        self._contacts.append(contact)

        
    def add_message(self, msg: Message) -> None:
        """
        add_message accepts a Message as parameter and appends it to the messages list. Messages are stored in a 
        list object in the order they are added. So if multiple Messages objects are created, but added to the 
        Profile in a different order, it is possible for the list to not be sorted by the Message.timestamp property
        """        
        self._msgs.append(msg)
        

    def get_contacts(self) -> list:
        """
        get_contacts returns the list object containing all messages that have been added to the Profile object
        """        
        return self._contacts 
    
    
    def get_messages(self) -> list:
        """
        get_messages returns the list object containing all messages that have been added to the Profile object
        """        
        return self._msgs
    
    
    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance of Profile to the file system.
        Raises DsuFileError
        """        
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")


    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data stored in a DSU file.
        Raises DsuProfileError, DsuFileError
        """
        # Empty the list of contacts before loading new profile to get rid of old contacts        
        while len(self._contacts) > 0:
            self._contacts.pop()
        # Empty the list of messages before loading new profile to get rid of old messges    
        while len(self._msgs) > 0:
            self._msgs.pop()
            
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self._contacts = obj['_contacts']
                for msg_obj in obj['_msgs']:
                    msg = Message(msg_obj['recipient'], msg_obj['entry'], msg_obj['timestamp'])
                    self._msgs.append(msg)
                f.close()
            except Exception as ex:
                raise DsuProfileError("An error occurred.")
        else:
            raise DsuFileError()