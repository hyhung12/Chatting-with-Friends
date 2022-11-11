**# NAME: Hung Nguyen**
<br>**# EMAIL: hunghn4@uci.edu**


### Chatting with Friends

This project includes the following starter files:

* __a6.py__:  The main module.
* __ds_messenger.py__: Contains DirectMessage and DirectMessenger classes.
* __ds_protocol.py__: Contains commands to send as well as retrieve directmessage to/from the DS Server.
* __input_check.py__: Contains functions to check if the user's information is valid (dsuserver, username, password).
* __Profile.py__: Same as Profile.py in previous assignment but with some modifications. Used to store data locally.
* __test_ds_message_protocol.py__: Contains tests to verify that messages are being processed as expected.
* __test_ds_messenger.py__: Contains tests to verify that the ds_messenger module is functioning properly.
* __a6.html__: The html version of the main module.
* __ds_messenger.html__: The html version of the ds_messenger module.
* __ds_protocol.html__: The html version of the ds_protocol module.
* __Profile.html__: The html version of the Profile module.

### Notes:
- There may be some commands like this displayed in the terminal
- They do not have any impacts on the GUI but they are quite annoyed<br><br>
invalid command name "2072391482112check_new_dm"<br>
    while executing<br>
"2072391482112check_new_dm"<br>
    ("after" script)<br><br>
    
- **New class:** Message in Profile.py<br>
- **Flourish:** User can change the dsuserver/username/password in 'Settings' -> 'Configure DS Server'

### How the program works:
- In order to send and receive the messages, the user firstly needs to setup the contact and the profile information.
(This can be done in 'Settings' menu)
- A Profile object is initialized when the GUI is opened so there is no need to create a new DSU file to start.
- In the 'Files' menu, there are 2 options which are 'Save' and 'Open'.
>'Save' is for saving the current conversations as well as the profile information to the DSU file.<br>
> 'Open' is for loading the Profile and displaying messages without connecting to the DSP server
- When opening a profile, the profile information is loaded so there is no need to setup them again.
- If the profile information is already setup, the user only needs to 'Add Contact' to send and receive the messages.
> In other words, to send and receive messages with previous contact (not recently added contact), 'Add Contact' needed to be clicked instead of the name of previous contact in the contact tree
- User can change the profile information by clicking 'Save Info' in 'Configure DS Server' however this also means all previous messages and contacts will be deleted

**References:**<br>
https://stackoverflow.com/questions/63547078/how-to-make-two-buttons-be-next-to-eachother-and-centered-in-python-tkinter<br>
https://www.pythontutorial.net/tkinter/tkinter-treeview/<br>
https://www.pythontutorial.net/tkinter/tkinter-toplevel/<br>
https://stackoverflow.com/questions/7338501/python-assign-value-if-none-exists

