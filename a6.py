# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523
#
# a6.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.


import tkinter as tk
from tkinter import ttk, filedialog
from Profile import Message, Profile
import input_check
from ds_messenger import DirectMessenger

# USERNAME = 'a5ok'
# PASSWORD = '12'
PORT = 3021
HOST = "168.235.86.101"


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the contacts and Message objects available in the active DSU file
        self._messages = [Message]
        self._contacts = []
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def node_select(self, event):
        """
        Updates the entry_editor with the full message entry 
        when the corresponding node in the contacts_tree is selected.
        """
        # Source: https://www.pythontutorial.net/tkinter/tkinter-treeview/
        # The contact in the contact tree
        index = int(self.contacts_tree.selection()[0])
        contact = self.contacts_tree.item(index,"text")
        # Clear the entry widget
        self.entry_editor.delete(0.0, 'end')
        
        # Display messages of each contact
        for msg_obj in self._messages:
            if msg_obj.recipient == contact:
                self.set_text_entry(msg_obj.entry)

    def get_message_entry(self) -> str:
        """
        Returns the messge to send that is currently displayed in the message_editor widget.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        """        
        self.entry_editor.insert('0.0', text + '\n')

    def set_contacts(self, contacts:list):
        """
        Populates the self._contacts attribute with contacts from the active DSU file.
        """        
        # populate self._contacts with the contact data passed
        # in the contacts parameter and repopulate the UI with the new contact entries.
        self._contacts = contacts
        for idx, contact in enumerate(self._contacts):
            self._insert_contact_tree(idx, contact)
            
    def insert_new_contact(self, new_contact):
        """
        Inserts a single contact to the contact_tree widget.
        """        
        self._contacts.append(new_contact)
        id = len(self._contacts) - 1 #adjust id for 0-base of treeview widget
        self._insert_contact_tree(id, new_contact)

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.entry_editor.delete('0.0', 'end')
        self.entry_editor.insert('0.0', "")  
        self.entry_editor.configure(state=tk.NORMAL)
        self._contacts = []
        self._messages = []
        for item in self.contacts_tree.get_children():
            self.contacts_tree.delete(item)

    def _insert_contact_tree(self, idx, contact:str):
        """
        Inserts a contact entry into the contacts_tree widget.
        """
        # Since we don't have a title, we will use the first 24 characters of a
        # contact entry as the identifier in the contact_tree widget.
        if len(contact) > 25:
            contact = contact[:24] + "..."
        
        self.contacts_tree.insert('', idx, idx, text=contact)
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """        
        contacts_frame = tk.Frame(master=self, width=250)
        contacts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.contacts_tree = ttk.Treeview(contacts_frame)
        self.contacts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.contacts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)
        
        self.message_frame = tk.Frame(master=self, bg="")
        self.message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.message_editor = tk.Text(self.message_frame, height=3)
        self.message_editor.pack(fill=tk.BOTH, padx=1, pady=1)
        

class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """   
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """        
        if self._send_callback is not None:
            self._send_callback()

    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """        
        save_button = tk.Button(master=self, text="Send", width=20)
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=2, pady=2)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class.
    """    
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._profile_filename = None
        # Initialize a new Profile and assign it to a class attribute
        self._current_profile = Profile()
        # Initialize a new DirectMessenger and assign it to a class attribute
        self._dm_obj = None
        # To check if directmessage is sucessfully sent
        self._sent_ok = False
        # To check if profile is sucessfully loaded
        self._is_loaded = False
        # An attribute to keep track of currently added contact
        self._current_contact = ""
        # To store new contact
        self._recipient = ""
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def save_profile(self):
        """
        Creates a new DSU file when the 'Save' menu item is clicked.
        Then save all messages and contacts to that DSU file
        """        
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        
        if filename is None:
            self.footer.set_status('Invalid name. Unablle to save the profile')
        else:
            try:
                self._profile_filename = filename.name
                self._current_profile._msgs = self.body._messages
                self._current_profile._contacts = self.body._contacts
                self._current_profile.save_profile(self._profile_filename)
            except:
                self.footer.set_status('The extension has to be dsu. Unable to save to this file')
            else:
                # Update the status
                self.footer.set_status('Save successfully')

    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI. 
        """  
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        if filename is None:
            self.footer.set_status('Invalid name. Unablle to open the file')
        else:
            
            self._profile_filename = filename.name
            # load a profile
            try:
                self._current_profile.load_profile(self._profile_filename)
            except:
                self.footer.set_status('Invalid DSU file. Cannot open this file')
            else:
                self._is_loaded = True
                # Create a DirectMessenger object to retrieve new message
                self._dm_obj = DirectMessenger(self._current_profile.dsuserver,
                                               self._current_profile.username,
                                               self._current_profile.password)
                
                # reset the UI just in case a profile has already been loaded
                self.body.reset_ui()
                # update the UI with contacts and messages
                self.body.set_contacts(self._current_profile.get_contacts())
                self.body._messages = self._current_profile.get_messages()
                # Update the status
                self.footer.set_status('Load successfully')
     
    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """        
        self.root.destroy()
                                 
    def add_recipient(self):
        """
        Adds new contact to communicate with when the profile data is setup (dsuserver, username, password)
        and ready to connect to the DS server.
        Also, display all the messages of the added contact if it has already existed
        """       
        # Check if the profile data has been saved
        # If profile information has been loaded then can add new contact
        if self._is_loaded:
            is_valid_info = True
        else:
            try: 
                is_valid_info = self._dm_obj._is_connected
            except:
                is_valid_info = False
                self.new_contact_window.destroy()
            
        # If the user has not yet configure the account, new contact cannot be added    
        if not is_valid_info:
            self.footer.set_status('New contact can be added if only the server is connected ')
            print('Missing user inputs or invalid inputs. Cannot add new contact')
            self.new_contact_window.destroy()
        else:
            self._recipient = self.new_contact_window.get_new_contact()
            
        # Check if recipient is valid to send message    
        if input_check.is_valid_usr_pwd(self._recipient, "contact"):
            # Check if the recipient has already existed
            if self._recipient in self.body._contacts:
                self.footer.set_status('This contact has already existed')
            else:
                self.body.insert_new_contact(self._recipient)
            # When new contact is added, update the UI and delete all previous messages
            self.body.entry_editor.delete('0.0', 'end')
            self.body.entry_editor.insert('0.0', "")    
            self.new_contact_window.destroy()
            # Update the status
            self.footer.set_status('New contact is added')
            self._current_contact = self._recipient
        else:
            self.footer.set_status('This contact may have special character. Cannot add this contact')
            
        # Display all messages if the contact has already existed
        for msg_obj in self.body._messages:
            if msg_obj.recipient == self._recipient:
                self.body.set_text_entry(msg_obj.entry)
            
    def save_info(self):
        """
        Saves all the information that is entered when the 'Save info' menu item is clicked to
        the DirectMessenger object and the profile. This method also resets the UI
        """         
        self._dm_obj = DirectMessenger(self.config_account_window.get_server_address(),
                                       self.config_account_window.get_user_name(),
                                       self.config_account_window.get_pass_word())
        # Save user information (dsuserver, username, password) to the profile
        self._current_profile.dsuserver = self._dm_obj.dsuserver
        self._current_profile.username = self._dm_obj.username
        self._current_profile.password = self._dm_obj.password
        # Reset the UI just in case a profile has already been loaded
        # Remove the existing contacts and messages in the profile
        self.body.entry_editor.delete('0.0', 'end')
        self.body.entry_editor.insert('0.0', "")
        self.body.reset_ui()
        self._current_profile._contacts = []
        self._current_profile._msgs = []
        # Update the status
        self.footer.set_status('New profile has been created. All preivous contacts and messages are deleted')
        self.config_account_window.destroy()
    
    def send_directmessage(self):
        """
        Displays the message in the message_entry widget then send it to the recipient
        """
        msg_to_send = self.body.get_message_entry()
        # Create a DirectMessenger object to send the directmessage
        self._send_dm_obj = DirectMessenger(self._current_profile.dsuserver,
                                        self._current_profile.username,
                                        self._current_profile.password)
        
        self._sent_ok = self._send_dm_obj.send(msg_to_send, self._recipient)
        
        display_msg =  '[You]: ' + msg_to_send
    
        if self._sent_ok:
            # Display the message in the message_entry widget
            self.body.set_text_entry(display_msg)
            # Store the message in Message object then add it to the profile 
            sent_msg_obj = Message(recipient=self._recipient, entry=display_msg)
            self.body._messages.append(sent_msg_obj)
            # Update the status
            self.footer.set_status('Sent')
            # Remove the message in the message_entry widget     
            self.body.message_editor.delete('0.0', 'end')
        else:
            self.footer.set_status('Invalid user inputs. Cannot send this message')
     
    def check_new_dm(self):
        """
        Checks new direct messages every 2 seconds and send the retrieved messages to the UI.
        Also, add them to the "messages" attributes of Body class
        """
        # Check if the DirectMessenger is assigned
        if self._dm_obj is not None:
            self._msg_lst = self._dm_obj.retrieve_new()
            if self._msg_lst is None:
                self.footer.set_status('Invalid recipient. Cannot retrieve messages')
            else:
                self._display_save(self._msg_lst)
                                                            
        # Repeatedly execute check_new_dm() every 2 seconds            
        self.root.after(2000, self.check_new_dm)
        
    def _display_save(self, msg_lst:list):
        """
        Iterates through a list of DM objects and save messsages that are only sent to
        the recipient in the contact list. Then display them on the message_entry widget
        """
        for new_dmsg_obj in msg_lst:
            if new_dmsg_obj.recipient in self.body._contacts:                       
                recipient_msg = f'[{new_dmsg_obj.recipient}]: ' + new_dmsg_obj.message
                if self._current_contact == new_dmsg_obj.recipient:
                    # Add retrieved message to the UI
                    self.body.set_text_entry(recipient_msg)
                # Add it the "messages" attributes
                msg_obj = Message(recipient=new_dmsg_obj.recipient, entry=recipient_msg)
                self.body._messages.append(msg_obj)
     
    def prompt_new_contact(self):
        """
        Creates a window to add new contact
        """            
        self.new_contact_window = Window(self.root, ui_option=1, new_contact_callback=self.add_recipient)
        
    def configure_account(self):
        """
        Creates a window to display the previously saved information(dsuserver, usn, pwd) in
        the profile and update the new user inputs
        """  
        self.config_account_window = Window(self.root, ui_option=2, save_info_callback=self.save_info)
        # Check if the profile's attributes are None, 
        # if true then set them to empty string to avoid error
        #if self._dm_obj is not None:
        # Source: https://stackoverflow.com/questions/7338501/python-assign-value-if-none-exists
            # self._dsuserver = self._dm_obj.dsuserver or ""
            # self._username = self._dm_obj.username or ""
            # self._password = self._dm_obj.password or ""
            
        self._dsuserver = self._current_profile.dsuserver or ""
        self._username = self._current_profile.username or ""
        self._password = self._current_profile.password or ""            
    # Update the value in Configure DS Server
        self.config_account_window.server_entry.insert('0.0', self._dsuserver)
        self.config_account_window.usn_entry.insert('0.0', self._username)
        self.config_account_window.pwd_entry.insert('0.0', self._password)
                  
    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Save', command=self.save_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Add Contact', command=self.prompt_new_contact)
        menu_settings.add_command(label='Configure DS Server', command=self.configure_account)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, send_callback=self.send_directmessage)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
class Window(tk.Toplevel):
    """
    A subclass of tk.Toplevel that is responsible for drawing all of the widgets
    in the menu portion of the root frame.
    """
    # Source: https://www.pythontutorial.net/tkinter/tkinter-toplevel/
    def __init__(self, root, ui_option=None, new_contact_callback=None, save_info_callback=None):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self._new_contact = ""
        self._server_address = ""
        self._usn = ""
        self._pwd = ""
        self._new_contact_callback = new_contact_callback
        self._save_info_callback = save_info_callback
        # If '1' create the "Add Contact" window
        # If '2' create the "Config Account" window
        if ui_option == 1:
            self._draw_inputwindow()
        elif ui_option == 2:
            self._draw_configwindow()
            
                     
    def get_new_contact(self):
        """
        Collects the input contact
        """  
        self._new_contact = self.input_contact.get('1.0', 'end').rstrip()  
        return self._new_contact
     
    def get_server_address(self):
        """
        Collects the input server address
        """          
        self._server_address = self.server_entry.get('1.0', 'end').rstrip()
        return self._server_address 
    
    def get_user_name(self):
        """
        Collects the input username
        """         
        self._usn = self.usn_entry.get('1.0', 'end').rstrip()
        return self._usn
        
    def get_pass_word(self):
        """
        Collects the input password
        """           
        self._pwd = self.pwd_entry.get('1.0', 'end').rstrip()
        return self._pwd
    
    def save_info_click(self):
        """
        Calls the callback function specified in the save_info_callback class attribute, if
        available, when the save_info_button widget has been clicked.
        """          
        if self._save_info_callback is not None:
            self._save_info_callback()
            
    def ok_click(self):
        """
        Calls the callback function specified in the new_contact_callback class attribute, if
        available, when the ok_button widget has been clicked.
        """           
        if self._new_contact_callback is not None:
            self._new_contact_callback()
    
    def _draw_inputwindow(self):
        """
        Call only once upon initialization to add widgets to the menu
        """ 
        self.geometry('400x100')
        self.title('Input')
        
        self.input_label = tk.Label(master = self, text = 'What is the username of your new contact')
        self.input_label.pack()  
        self.input_contact = tk.Text(master = self, width=15, height=1)
        self.input_contact.pack()
        
        self.input_ok_button = tk.Button(master = self, text = 'OK', width=8)
        self.input_ok_button.configure(command=self.ok_click)
        self.input_ok_button.pack(side='left', anchor='ne', padx=8, pady=10, expand=True)
        
        self.input_cancel_button = tk.Button(master = self, text = 'Cancel',width=8)
        self.input_cancel_button.configure(command=self.destroy)
        self.input_cancel_button.pack(side='right', anchor='nw', padx=8, pady=10, expand=True)

    def _draw_configwindow(self):
        """
        Call only once upon initialization to add widgets to the menu
        """
        # Source: https://stackoverflow.com/questions/63547078/how-to-make-two-buttons-be-next-to-eachother-and-centered-in-python-tkinter
        self.geometry('400x180')
        self.title('Configure Account')
        
        self.server_label = tk.Label(master = self, text = 'DS Server Address')
        self.server_label.pack()
        self.server_entry = tk.Text(master = self, width=15, height=1)
        self.server_entry.pack()
        
        self.usn_label = tk.Label(master = self, text = 'Username')
        self.usn_label.pack()
        self.usn_entry = tk.Text(master = self, width=15, height=1)
        self.usn_entry.pack()
            
        self.pwd_label = tk.Label(master = self, text = 'Password')
        self.pwd_label.pack()
        self.pwd_entry = tk.Text(master = self, width=15, height=1)
        self.pwd_entry.pack()

        self.config_account_connect_button = tk.Button(master = self, text = 'Save Info', width=8)
        self.config_account_connect_button.configure(command=self.save_info_click)
        self.config_account_connect_button.pack(side='left', anchor='ne', padx=8, pady=10, expand=True)
        
        self.config_account_cancel_button = tk.Button(master = self, text = 'Cancel',width=8)
        self.config_account_cancel_button.configure(command=self.destroy)
        self.config_account_cancel_button.pack(side='right', anchor='nw', padx=8, pady=10, expand=True)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("The hardest assignment in ICS 32")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.after(2000, app.check_new_dm)
    main.mainloop()
