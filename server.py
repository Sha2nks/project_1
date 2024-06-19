import socket
import json
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

class Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024)
            if not data:
                return
            
            request = json.loads(data)
            if isinstance(request, list):
                responses = self.executor.map(self.process_request, request)
                client_socket.sendall(json.dumps(list(responses)).encode())
            else:
                response = self.process_request(request)
                client_socket.sendall(json.dumps(response).encode())
        except json.JSONDecodeError:
            response = {"error code": 1}
            client_socket.sendall(json.dumps(response).encode())
        finally:
            client_socket.close()

    def process_request(self, request):
        response = {"id": request.get("id", None)}
        try:
            method = request["method"]
            result = subprocess.run(method, shell=True, capture_output=True, text=True)
            response.update({
                "result": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error code": 0
            })
        except KeyError:
            response["error code"] = 2
        except subprocess.CalledProcessError:
            response["error code"] = 3
        except Exception:
            response["error code"] = 4
        return response

    def run(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.run()
