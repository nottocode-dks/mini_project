import socket
import operator
import threading

new_dict = {}


class Client(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, clientAddress):
        threading.Thread.__init__(self)
        self.conn = connection
        self.clientAddress = clientAddress

    def run(self):
        (ipOfClient, port) = self.clientAddress

        while True:
            filename = open("iplist.txt", "w")
            data = self.conn.recv(10).decode()

            if data == "":
                data = "100"

            print(ipOfClient + " " + str(data))
            new_dict[ipOfClient] = data

            Client.lock.acquire()
            print(len(new_dict))
            sorted_dict = sorted(new_dict.items(), key=operator.itemgetter(1))
            for key, value in sorted_dict:
                filename.write(key + " " + value + "\n")
            Client.lock.release()
            if(data == "100"):
                break


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('', 10001)
sock.bind(serverAddress)
sock.listen(10)

while True:
    print("Waiting for Connections")
    connection, clientAddress = sock.accept()
    thread = Client(connection, clientAddress)
    thread.start()
