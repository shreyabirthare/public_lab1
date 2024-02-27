import socket
import json
import sys

def queryToy(serverIP, serverPort, toy_name):
    try:
        with socket.socket() as sock:
            sock.connect((serverIP, serverPort))
            request = json.dumps({'Query': toy_name})
            sock.sendall(request.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            print(f"Price of {toy_name}: {data}")
    except Exception as e:
        print(f"Error querying toy: {e}")

if __name__ == '__main__':
    serverIP = sys.argv[1]
    serverPort = int(sys.argv[2])
    toyNames = sys.argv[3].split(",")

    for toy in toyNames:
        queryToy(serverIP, serverPort, toy)
