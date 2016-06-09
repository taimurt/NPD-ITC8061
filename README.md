# NPD-ITC8061
Network Chat Application developed by Taimur Tufail, Tiziano Contaldo & Kristen Kivimaa.

The application has been developed with python 3.5

Run the application by command line (with pithon 3.5)
with two arguments:
- uuid: String of 4 character (identifier)
- port: number that identifies the port of the application 
   (it could be any port number)

>python chat.py uuid port

Example:
>python chat.py abcd 2222

Note: This application can run directly on Mac OS X, Linux and Windows but you have to write the command " alias python='python3' " when ever you open a new terminal window to set it default to python 3.5 version (only if it is not set to version 3 by default).

After run the application a window appears.

In the botton there is a text box where to write the message
In the menu bar (Commands) there is the command menu with the following commands:

Commands Menu:

- Add peer: Command to add a neighbour. You should know ip address and port number of the peer you want to connect. Write in the textbox these information in this format: ipaddress:portnumber

  Example:  127.0.0.1:2222   (peer in local host)

  Note: You can run more peers in your localhost with different port numbers. Also please wait for about 15 seconds for rounting table to update properly.

- Show Routing Table: This command has been introduced to show the routing tables of the node just to verify that the protocol reach the task.

- Show Users: Show the users linked with you application


Sending A Message:

To send a message you have to write something and specify the receiver (uuid)
Both must be entered in the textbox on the botton of the chat in that format:  "message":>"uuid receiver"
	
Example: "aaaa" wants to write "hello" to "bbbb" 
	In the textbox of aaaa: hello>bbbb
If you want to write a message to everyone in the chat just write ALL as receiver
	Example: hello>ALL



Running Multiple Applications:
You can run multiple applications in the same computer by just changing the uuid and port number to check the rounting table and neiboring table working properly.

For example: 
Application 1: 
>python chat.py aaaa 1111

Commands Menu: Add Peer: 127.0.0.1:2222


Application 2: 
>python chat.py bbbb 2222

Commands Menu: Add Peer: 127.0.0.1:3333


Application 3: 
>python chat.py cccc 3333


- You can check by sending from user "aaaa" to "cccc" by typing "test message>cccc" to send individualy or "test message>ALL" to send    all of the users.
- If you quite application 3 and then check from the command "Show users" in Application 1 and 2 then the user "cccc" will be removed from their routing table respectively.



Close the application.
When you close a peer some thread could be still running so please close the terminal to stop all processes.
