import slack_sdk
import pyupbit
import time
import requests

access = "Access key"
secret = "Secret key"
upbit = pyupbit.Upbit(access, secret)

buy_count = 0
buy_money = 5000

slack_token = 'bot_tokenn'
client = slack_sdk.WebClient(token=slack_token)

while (upbit.get_balance('KRW') > (buy_money * 0.0005)):

    # KRW-BTC가 0원이면 시장가 매수
    if upbit.get_balance("KRW-BTC") == 0:
        upbit.buy_market_order("KRW-BTC", buy_money)
        buy_count += 1

        # 현재 수익률
        rate_of_return = upbit.get_balance("KRW-BTC")/(buy_money * buy_count)

        message = "현재 구매 횟수 : %i , 현재 수익률 : %i, 현재 잔액 : %i" % (
            buy_count, rate_of_return, upbit.get_balance('KRW'))

        client.chat_postMessage(channel='upbit', text=message)

        time.sleep(5)

    url = "https://api.upbit.com/v1/trades/ticks?market=KRW-BTC&count=1"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    # 6% 이상 이익
    if float(pyupbit.get_current_price('KRW-BTC')) * 1.06 <= float(upbit.get_balances()[0]['avg_buy_price']):
        upbit.sell_market_order("KRW-BTC", buy_count)
        buy_count = 0

        # 현재 수익률
        rate_of_return = upbit.get_balance("KRW-BTC")/(buy_money * buy_count)

        message = "현재 구매 횟수 : %i , 현재 수익률 : %i, 현재 잔액 : %i" % (
            buy_count, rate_of_return, upbit.get_balance('KRW'))

        client.chat_postMessage(channel='upbit', text=message)

        time.sleep(5)

    # 6% 이상 손해
    elif float(response.text.split(',')[4].split(':')[1]) * 0.94 >= float(pyupbit.get_current_price('KRW-BTC')):
        upbit.buy_market_order("KRW-BTC", buy_money)
        buy_count += 1

        # 현재 수익률
        rate_of_return = upbit.get_balance("KRW-BTC")/(buy_money * buy_count)

        message = "현재 구매 횟수 : %i , 현재 수익률 : %i, 현재 잔액 : %i" % (
            buy_count, rate_of_return, upbit.get_balance('KRW'))

        client.chat_postMessage(channel='upbit', text=message)

        time.sleep(5)

    time.sleep(5)
