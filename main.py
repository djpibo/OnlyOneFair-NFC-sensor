import sys
import time
import socketio
import redis

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

r = redis.Redis(host='localhost', port=6379, db=0)

sio = socketio.Client()
sio.connect('http://localhost:5000', transports=['websocket'])

@sio.event
def connect():
    print("서버에 연결되었습니다!")

@sio.event
def disconnect():
    print("서버와의 연결이 끊어졌습니다!")


class PrintObserver(CardObserver):
    def update(self, observable, actions):
        (added_cards, removed_cards) = actions
        for card in added_cards:
            print("+Inserted: ", toHexString(card.atr))
            sio.emit('nfc_data', {'data': toHexString(card.atr)})

def main():

    if len(sys.argv) == 3: # 각 클래스 입장

        r.set('company', sys.argv[1].encode('utf-8'))
        stored_value1= r.get('company').decode('utf-8')
        print(f'저장된 값 1: {stored_value1}')

        r.set('enter', sys.argv[2].encode('utf-8'))
        stored_value2 = r.get('enter').decode('utf-8')
        print(f'저장된 값 2: {stored_value2}')

        card_monitor = CardMonitor()
        card_observer = PrintObserver()
        card_monitor.addObserver(card_observer)

        time.sleep(60 * 60 * 12)
        card_monitor.deleteObserver(card_observer)

if __name__ == "__main__":
    main()