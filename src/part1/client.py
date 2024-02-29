import socket
import json
import sys
import time

def queryToy(serverIP, serverPort, toy_name):
    
    # Create a client socket to connect to the server and fetch information of the toy 
    try:
        with socket.socket() as sock:
            sock.connect((serverIP, serverPort))
            request = json.dumps({'Query': toy_name})
            startTime =time.time()
            sock.sendall(request.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            latency = time.time() - startTime
            print(f"Price of {toy_name}: {data}, Request Latency: {latency} seconds")
            return latency
    except Exception as e:
        print(f"Error querying toy: {e}")
        return None

if __name__ == '__main__':

    # Parse through the command line arguments to get the ip, port and toy names
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])
    toyNames = sys.argv[3].split(",")

    latencyList = []

    # Iterate through every toy in the list of toys
    for toy in toyNames:
        latency = queryToy(serverIP, serverPort, toy)
        latencyList.append(latency)
    
    # Append the average latency to the file
    if latencyList is not None:
        avgLatency = sum(latencyList)/len(latencyList)
        with open('latencies.txt', 'a') as file:
            file.write(f"{avgLatency}\n")
