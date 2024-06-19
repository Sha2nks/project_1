import socket
import json
import uuid

class Client:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        try:
            self.client_socket.sendall(json.dumps(request).encode())
            response = self.client_socket.recv(1024)
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error code": 1}
        finally:
            self.client_socket.close()

    def request(self, method):
        request_object = {
            "method": method,
            "id": str(uuid.uuid4())
        }
        self.connect()
        return self.send_request(request_object)

    def batch_request(self, methods):
        request_objects = [
            {"method": method, "id": str(uuid.uuid4())} for method in methods
        ]
        self.connect()
        return self.send_request(request_objects)

if __name__ == "__main__":
    client = Client()
    response = client.request("echo Hello World")
    print(response)

    batch_response = client.batch_request(["date","uptime", "hostname","ping -c 4 127.0.0.1"])
    print(batch_response)
