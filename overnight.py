from datetime import datetime
from time import time
import ccxt
import telegram


def sendmessage(message):  # 텔레그램 메시지 보내기
    chat_token = "1552878152:AAEPeN6Cvya7gnPl0bJKOT2JEc3hAkDoEM4"  # 봇 토큰
    # 텔레그램에서 지정된 숫자형식 ID, @Overnight_Project_bot에 메시지를 보내면 https://api.telegram.org/bot1552878152:AAEPeN6Cvya7gnPl0bJKOT2JEc3hAkDoEM4/getUpdates 링크에서 ID가 조회 가능
    telegram_ID1 = "1528917019"  # 이민기
    telegram_ID2 = "1413615947"  # 조성화
    # telegram_ID3 = "" #백승헌
    telegram_ID4 = "1606164564"  # 지웅재
    bot = telegram.Bot(token=chat_token)
    bot.sendMessage(chat_id=telegram_ID1, text=message)  # 메시지 최대 문자 수는 4096자
    bot.sendMessage(chat_id=telegram_ID2, text=message)  # 메시지 최대 문자 수는 4096자
    # bot.sendMessage(chat_id=telegram_ID3, text=message)  # 메시지 최대 문자 수는 4096자
    bot.sendMessage(chat_id=telegram_ID4, text=message)  # 메시지 최대 문자 수는 4096자


def BlackLine(data):
    HighPoint = 0
    for i in range(1919):
        HighPoint = max(HighPoint, float(data[1918-i][2]))
    return HighPoint


def BlueLine(data):
    LowPoint = 999999999
    for i in range(1919):
        LowPoint = min(LowPoint, float(data[1918-i][3]))
    return LowPoint


api_key = '2bwHYfVsGBrM6GFfJ9Dki0fUaSfcg5DADBdUfWOscRmsYw5I2Cwprb3MkdpbvkpC'
sec_key = 'JDDBBqHnlV8CsORmcCDtEXssdXdWt5asni4v1WCwsztfiGADQ4WNNZ2bnpNoQdER'

# binance 호줄에 내 api와 sec키를 이용하여 잔고조회와 매도/매수 주문을 할 수 있게 함
binance = ccxt.binance({'apiKey': api_key, 'secret': sec_key, })


state = False  # 거래중이 아님

init = True

balance = binance.fetch_balance()

print(balance.keys())

# 자료 최초 저장
# since time 찍었을때 현재분봉 나오는지 이전에 확정된 분봉 나오는지 체크해봐야됨
data_temp_LINK = binance.fetch_ohlcv(
    'LINK/USDT', '1m', since=(int(time() - 1922 * 60)) * 1000, limit=1000)
data_temp1_LINK = binance.fetch_ohlcv(
    'LINK/USDT', '1m', since=(int(time() - 922 * 60)) * 1000, limit=921)
data_temp_LINK = data_temp_LINK + data_temp1_LINK
data_LINK = []

time_cursor = 1

while time_cursor < 1921:
    op = (float(data_temp_LINK[time_cursor-1][1]) +
          float(data_temp_LINK[time_cursor-1][4])) / 2
    hi = float(data_temp_LINK[time_cursor][2])
    lo = float(data_temp_LINK[time_cursor][3])
    cl = (float(data_temp_LINK[time_cursor][1]) + float(data_temp_LINK[time_cursor][2]) +
          float(data_temp_LINK[time_cursor][3]) + float(data_temp_LINK[time_cursor][4])) / 4
    data_LINK.append([data_temp_LINK[time_cursor][0], op, hi, lo, cl])
    time_cursor += 1


now = datetime.now()
minute_temp = now.minute
zerosum = True

while True:
    now = datetime.now()
    if now.minute == 0 and zerosum:
        minute_temp = -1
        zerosum = False
    if now.minute == 1 and zerosum is False:
        zerosum = True

    if now.minute > minute_temp:
        print(now.minute)
        minute_temp = now.minute

        # 하이킨아시 데이터 갱신
        data_temp_LINK = binance.fetch_ohlcv(
            'LINK/USDT', '1m', since=int(time() - 2*60) * 1000, limit=2)
        for x in range(1, 1920):
            data_LINK[x-1] = data_LINK[x]

        op = (float(data_temp_LINK[0][1]) + float(data_temp_LINK[0][4])) / 2
        hi = float(data_temp_LINK[1][2])
        lo = float(data_temp_LINK[1][3])
        cl = (float(data_temp_LINK[1][1]) + float(data_temp_LINK[1][2]) +
              float(data_temp_LINK[1][3]) + float(data_temp_LINK[1][4])) / 4
        data_LINK[1919] = [data_temp_LINK[1][0], op, hi, lo, cl]

        # 거래
        if BlackLine(data_LINK) < data_LINK[1919][2] and balance['USDT']['free'] > 10 and state is False:
            print('codeblack')
            if init:
                orderbook = binance.fetch_order_book('LINK/USDT')
                while balance['USDT']['free'] > orderbook['asks'][0] * orderbook['asks'][1]:
                    balance = binance.fetch_balance()
                    order = binance.create_market_buy_order(
                        'LINK/USDT', orderbook['asks'][0])
                    orderbook = binance.fetch_order_book('LINK/USDT')
                    message = '매수완료\n' + '주문코인: ' + \
                        order['symbol'] + '\n' + '주문번호: ' + order['orderId'] + '\n' + \
                        '매수단가: ' + order['price'] + \
                        '\n' + '수량: ' + order['amount']
                    sendmessage(message)
                balance = binance.fetch_balance()
                order = binance.create_market_buy_order(
                    'LINK/USDT', balance['USDT']['free'] / orderbook['asks'][0])
                message = '매수완료\n' + '주문코인: ' + \
                    order['symbol'] + '\n' + '주문번호: ' + order['orderId'] + '\n' + \
                    '매수단가: ' + order['price'] + '\n' + '수량: ' + order['amount']
                sendmessage(message)
            state = True

        elif BlueLine(data_LINK) > data_LINK[1919][3] and state:
            print('codeblue')
            balance = binance.fetch_balance()
            order = binance.create_market_sell_order(
                'LINK/USDT', balance['LINK']['free'])
            state = False
            init = True

            message = '매도완료\n' + '주문코인: ' + order['symbol'] + '\n' + '주문번호: ' + \
                order['orderId'] + '\n' + '매도단가: ' + \
                order['price'] + '\n' + '수량: ' + order['amount']
            sendmessage(message)
