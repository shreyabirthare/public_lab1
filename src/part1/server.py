import socket
import threading
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Toy Store Catalog
catalog = {
    'Tux': {'price': 25, 'stock': 10},
    'Whale': {'price': 10, 'stock': 5}
}

class RequestQueue:
    def __init__(self):
        self.requestQueue = []
        self.lock = threading.Lock()
        self.queueData = threading.Condition(self.lock)

    def insertRequest(self, item):
        with self.lock:
            self.requestQueue.append(item)
            self.queueData.notify()

    def removeRequest(self):
        with self.lock:
            while not self.requestQueue:
                self.queueData.wait()
            return self.requestQueue.pop(0)

class ThreadPool:
    def __init__(self, threadCount):
        self.requests = RequestQueue()
        self.workers = [threading.Thread(target=self.worker) for _ in range(threadCount)]

        for worker in self.workers:
            worker.start()

    def worker(self):
        while True:
            client, address = self.requests.removeRequest()
            self.processRequest(client, address)

    def addRequest(self, task):
        self.requests.insertRequest(task)

    def processRequest(self, client, address):
        try:
            data = client.recv(1024).decode('utf-8')
            logging.info(f"Received request from {address}: {data}")
            request = json.loads(data)
            
            if 'Query' in request:
                toyName = request['Query']
                toyInfo = self.Query(toyName)
                client.sendall(json.dumps(toyInfo).encode('utf-8'))
            else:
                logging.error(f"Invalid method name given")
                client.sendall(json.dumps({'error': 'Invalid method'}).encode('utf-8'))
        except Exception as e:
            logging.error(f"Error handling request: {e}")
        finally:
            client.close()

    def Query(self, toyName):
        toy = catalog.get(toyName)
        if toy:
            return {'price': toy['price']} if toy['stock'] > 0 else {toyName: "Out of Stock"}
        return {toyName: "Does Not exist in Catalog"}

def startServer(host='128.119.243.168', port=8888, threadCount=3):
    serverSocket = socket.socket()
    serverSocket.bind((host, port))
    serverSocket.listen(5)
    logging.info(f"Server listening on {host}:{port}")

    pool = ThreadPool(threadCount)

    try:
        while True:
            client, address = serverSocket.accept()
            logging.info(f"Connected to {address} client!")
            pool.addRequest((client, address))
    except KeyboardInterrupt:
        logging.info("Keyboard Interrupt! Closing Server")
    finally:
        serverSocket.close()

if __name__ == '__main__':
    startServer()
