# time_server.py
import socket
import time
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET 주소유형 Adress Family AF_INET16, AF_UNIX SOCK_STREAM TCP소켓 생성
# UDP소켓은 SOCK_DGRAM
address = ('', 5000) # 종단점. (host, port) IPv4에서는 ''등 빈 문자열 가능
sock.bind(address) # 소켓을 종단점과 결합
sock.listen(5) # 동시 연결 가능한 소켓 수 5
while True:
    client, addr = sock.accept() # 연결 허용하고 클라이언트 소켓과 주소 반환
    print("Connection requested from ", addr)
    client.send(time.ctime(time.time()).encode()) # byte형 메시지 전송
    # client.send('Hello'.encode())
    client.close()