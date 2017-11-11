## Convert Celsius to Fahrenheit via Socket

### edmts_server.py
 - How to run server?
 ```bash
 python edmts_server.py <port>
 ```
 - Example: 
 ```bash
 python edmts_server.py 24459
 ```
 - Explaination:
   + Server will create and open a socket at localhost and a specified port
   + Server keep listening any request from client
   + Once a request come, server will analyze the request: if the request = 'Celsius' or 'Fahrenheit', a random Celsius temperature value will be generate then server will send a message 'Edmonton is at <temperature> <Celsius/Fahrenheit> at <current date time>' to client, else server will send a error message 'Wrong format request. The request should be Fahrenheit or Celsius'

### edmts_client.py
 - How to run client?
 ```bash
 python edmts_client.py <ip address> <port> <request message> 
 ```
 - Example: 
 ```bash
 ./edmts_client.py 192.168.186.1 24459 Celsius
 ```
 ```
 Result: Edmonton is at -2 Celsius at Sun Mar 6 22:48:13 2016
 ```
 - Explaination:
   + Server will create socket and connect to server at specified address/port
   + If the connection can be established, client will send a request message (from environment argument) to server and wait for server response
   + Once a response code, client print the result to the screen and close the connection.
