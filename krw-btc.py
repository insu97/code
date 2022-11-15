import slack_sdk
import pyupbit
import time
import requests

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

buy_count = 0
buy_money = 5000

slack_token = ''
client = slack_sdk.WebClient(token=slack_token)

total_money = 100000
buy_money = 5000
buy_count = 0
location_coin = 0
funds_price = 0

error_count = 0

while (total_money > buy_money * 1.0005):

    try:

        if (buy_count == 0):
            upbit.buy_market_order("KRW-BTC", buy_money)
            buy_count += 1
            recent_uuid = upbit.get_order("KRW-BTC", state="done")[0]['uuid']
            order = upbit.get_order(recent_uuid)
            recent_price = float(order['trades'][0]['price'])
            total_money -= buy_money
            message = "현재 구매 횟수 : %i , 현재 잔액 : %i" % (buy_count, total_money)
            client.chat_postMessage(channel='upbit', text=message)
            time.sleep(5)

        for i in range(len(upbit.get_balances())):
            if upbit.get_balances()[i]['currency'] == 'BTC':
                locaion_coin = i

        if float(pyupbit.get_current_price('KRW-BTC')) >= float(upbit.get_balances()[location_coin]['avg_buy_price']) * 1.06:
            upbit.sell_market_order("KRW-BTC")
            recent_uuid = upbit.get_order("KRW-BTC", state="done")[0]['uuid']
            order = upbit.get_order(recent_uuid)
            funds_price = float(order['trades'][0]['funds'])
            total_money += funds_price
            message = "매도 개수 : %i , 현재 잔액 : %i" % (buy_count, total_money)
            client.chat_postMessage(channel='upbit', text=message)
            buy_count = 0
            time.sleep(5)

        elif float(pyupbit.get_current_price('KRW-BTC')) <= recent_price * 0.98:
            print(upbit.buy_market_order("KRW-BTC", buy_money))
            buy_count += 1
            recent_uuid = upbit.get_order("KRW-BTC", state="done")[0]['uuid']
            order = upbit.get_order(recent_uuid)
            recent_price = float(order['trades'][0]['price'])
            total_money -= buy_money
            print(buy_count, '회 매수')
            message = "현재 구매 횟수 : %i , 현재 잔액 : %i" % (buy_count, total_money)
            client.chat_postMessage(channel='upbit', text=message)
            time.sleep(5)

    except:
        error_count += 1
        if (error_count == 5):
            print('5회 오류 발생--> 종료!')
            break
        time.sleep(5)
