# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

import ds_protocol
import json
import unittest

"""
This module includes tests to verify that direct_messages are being processed as expected
"""
# Constants for testing
HOST = "168.235.86.101"
PORT = 3021
USERNAME = "a6test12"
PASSWORD = "12"
RECIPIENT = "fptest12"
# These functions are from a3
# Setup a connection to the DS server and join it
SOCK = ds_protocol.connect_to_server(HOST, PORT)
CONN_OBJ = ds_protocol.init(SOCK)
join_rsp, TOKEN = ds_protocol.join(CONN_OBJ, USERNAME, PASSWORD)

"""Tests"""
class test_ds_message_protocol(unittest.TestCase):
    """
    If direct message is successfully sent
    Server responses OK
    """
    def test_directmessage(self):
        message = "Test OK"
        sent_rsp = ds_protocol.directmessage(CONN_OBJ, TOKEN, message, RECIPIENT)
        sent_rsp_type = json.loads(sent_rsp)['response']['type']
        self.assertEqual(sent_rsp_type, "ok")
 

    """
    If successfully retrieve new messages
    Server responses OK
    """
    def test_response_new(self):
        new_rsp = ds_protocol.dm_response(CONN_OBJ, TOKEN, "new")
        new_rsp_type = json.loads(new_rsp)['response']['type']
        self.assertEqual(new_rsp_type, "ok")

        
    """
    If successfully retrieve all messages
    Server responses OK
    """        
    def test_response_all(self):
        all_rsp = ds_protocol.dm_response(CONN_OBJ, TOKEN, "all")
        all_rsp_type = json.loads(all_rsp)['response']['type']
        self.assertEqual(all_rsp_type, "ok")

        
if __name__ == '__main__':
    unittest.main()