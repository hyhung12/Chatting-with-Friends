# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

from ds_messenger import DirectMessage, DirectMessenger
import unittest

"""
This module includes tests to verify that the ds_messenger module is functioning properly
"""
# Constants for testing
HOST = "168.235.86.101"
PORT = 3021
USERNAME = "test12"
PASSWORD = "12"
RECIPIENT = "test12"

"""Tests"""
class test_ds_messenger(unittest.TestCase):
    """
    Check if the type of newly created object is DirectMessage 
    """
    def test_directmessage_obj(self):
        directmessage_obj = DirectMessage(recipient=RECIPIENT, message="Test 1 ok")
        self.assertIsInstance(directmessage_obj, DirectMessage)
        
        
    """
    Check if the newly created DirectMessager is able to send directmessage to the DS server
    The DS server sends OK response if the directmessage is succesfully received
    """        
    def test_dm_send(self):
        dm_obj = DirectMessenger(dsuserver=HOST, username=USERNAME, password=PASSWORD)
        message = "Test 2 ok"
        is_sent_ok = dm_obj.send(message=message, recipient=RECIPIENT)
        self.assertEqual(is_sent_ok, True)
        
        
    """
    Check if the newly created DirectMessager object is able to retrieve new directmessages from the DS server
    If retrieve_new works, it will return a list of DirectMessage objects containing all new messages
    """         
    def test_dm_retrieve_new(self):
        dm_obj = DirectMessenger(dsuserver=HOST, username=USERNAME, password=PASSWORD)
        message = "Test 3 ok"
        dm_obj.send(message=message, recipient=RECIPIENT)
        new_messages_lst = dm_obj.retrieve_new()
        is_directmessage_obj = False
        if new_messages_lst:
            is_directmessage_obj = all(type(message) == DirectMessage for message in new_messages_lst)
        self.assertEqual(is_directmessage_obj , True)
        
        
    """
    Check if the newly created DirectMessager object is able to retrieve all directmessages from the DS server
    If retrieve_all works, it will return a list of DirectMessage objects containing all messages
    """                      
    def test_dm_retrieve_all(self):
        dm_obj = DirectMessenger(dsuserver=HOST, username=USERNAME, password=PASSWORD)
        message = "Test 4 ok"
        dm_obj.send(message=message, recipient=RECIPIENT)
        all_messages_lst = dm_obj.retrieve_all()
        is_directmessage_obj = False
        if all_messages_lst:
            is_directmessage_obj = all(type(message) == DirectMessage for message in all_messages_lst)
        self.assertEqual(is_directmessage_obj , True)


if __name__ == '__main__':
    unittest.main()