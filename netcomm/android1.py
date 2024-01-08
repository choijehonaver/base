import asyncio
from bleak import BleakClient

# 위에서 얻은 BLE 장치의 주소
# address = "00:1a:7d:da:71:15" # device not found
# address = "5c:cb:99:bd:8e:cc" # device not found
# address = "B2:22:7A:9D:68:A6" # connected
address="7E:6A:F5:96:79:3A" # connected  연결된 디바이스의 공통점은, 안드로이드 블루투스 검색에서는 보이지 않고 blueSPP에서 검색시에만 나타남.
# address=" FC:03:9F:EF:A2:C3" # device not found
# address=" 5A:AF:32:7B:14:AD" # device not found
# 장치와 연결 해제시 발생하는 콜백 이벤트
def on_disconnect(client):
    print("Client with address {} got disconnected!".format(client.address))

async def run(address):
    # 장치 주소를 이용해 client 클래스 생성
    client = BleakClient(address)
    try:
        # 장치 연결 해제 콜백 함수 등록
        client.set_disconnected_callback(on_disconnect)
        # 장치 연결 시작
        await client.connect()
        print('connected')
    except Exception as e:
        # 연결 실패시 발생
        print('error: ', e, end='')
    finally:
        print('start disconnect')
        # 장치 연결 해제
        await client.disconnect()
loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')





