import slack_sdk
import pyupbit
import time

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

slack_token = ''
client = slack_sdk.WebClient(token=slack_token)

buy_count = 0
buy_money = 5000

coin_name = 'KRW-MATIC'

first_buy_price = 0

profit_rate = 0.05
gap_rate = 0.02

location_number = 0

error_count = 0

while (buy_count <= 20):

    try:
        if buy_count == 0:
            upbit.buy_market_order(coin_name, buy_money)
            buy_count += 1
            balance = upbit.get_balances()

            for i in range(len(balance)):
                if balance[i]['currency'] == coin_name:
                    first_buy_price = float(balance[i]['avg_buy_price'])

            message = '[%s] | 현재 구매 횟수 : %i' % (coin_name, buy_count)
            client.chat_postMessage(channel='upbit', text=message)
            time.sleep(5)

        balance = upbit.get_balances()
        for i in range(len(balance)):
            if balance[i]['currency'] == coin_name:
                location_number = i

        if float(pyupbit.get_current_price(coin_name)) >= float(balance[location_number]['avg_buy_price']) * (1+profit_rate):
            upbit.sell_market_order(coin_name)
            message = '[%s] | 매도 개수 : %i' % (coin_name, buy_count)
            client.chat_postMessage(channel='upbit', text=message)
            buy_count = 0
            time.sleep(5)
        elif float(pyupbit.get_current_price(coin_name)) <= first_buy_price * (1-gap_rate*buy_count):
            upbit.buy_market_order(coin_name, buy_money)
            buy_count += 1
            message = '[%s] | 현재 구매 횟수 : %i' % (coin_name, buy_count)
            client.chat_postMessage(channel='upbit', text=message)
            time.sleep(5)

        time.sleep(5)

    except:
        error_count += 1
        if (error_count == 5):
            message = '에러발생!! 종료...'
            client.chat_postMessage(channel='upbit', text=message)
            break
        time.sleep(5)
