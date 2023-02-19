import requests

from .market import Market

class Account(Market):

    AVAILABE_CURRENCY = ['RUB', 'USD', 'EUR']
    INCORRECT_CURRENCY = f'Неправильно выбрана валюта. Доступные сейчас {AVAILABE_CURRENCY}'


    def __init__(self, token: str) -> None:
        super().__init__(token)


    # POST Method 'ping'
    def ping(self):
        response = requests.post(f'https://market.csgo.com/api/v2/ping?key={self.token}').json()

        if response['success'] == True:
            print('PONG! Продажи включены')
        else:
            print(self.ERROR_RESPONSE)        


    # POST Method 'get_money' gives back your currency and amount of money on your account
    def get_money(self):
        response = requests.post(f'https://market.csgo.com/api/v2/get-money?key={self.token}').json()

        if response['success'] == False:
            print('Данные недоступны и/или отсутствуют. Проверьте API-ключ')
        else:
            print(f'Валюта: {response["currency"]}\nБаланс: {response["money"]}')


    # POST Metgod 'go_offline' turns down your sales
    def go_offline(self):
        response = requests.post(f'https://market.csgo.com/api/v2/go-offline?key={self.token}').json()

        if response['success'] == True:
            print('Продажи остановлены!')
        else:
            print(self.ERROR_RESPONSE)


    # POST Method 'update_inventory' refreshes the inventory cache (recommended to do after each accepted trade offer)
    def update_inventory(self):
        response = requests.post(f'https://market.csgo.com/api/v2/update-inventory/?key={self.token}').json()

        if response['success'] == True:
            print('Инвентарь обновлен!')
        else:
            print(self.ERROR_RESPONSE)


    # REMEMBER! THIS METHOD IS USELESS STILL DISCOUNT PROGRAMM REWORKING!
    # POST Method 'transef_discount' moves your discount to another account. 
    def transef_discount(self, his_secret_key: str):
        response = requests.post(f'https://market.csgo.com/api/v2/transfer-discounts?key={self.token}&to={his_secret_key}').json()

        if response['success'] == True:
            print('Скидка перенесена!')
        else:
            print(self.ERROR_RESPONSE)


    # POST Method 'get_my_steam_id' gives your STEAMID 32/64 
    def get_my_steam_id(self):
        response = requests.post(f'https://market.csgo.com/api/v2/get-my-steam-id?key={self.token}').json()

        if response['success'] == True:
            return print(f'SteamID32: {response["steamid32"]}\nSteamID64: {response["steamid64"]}')
        else:
            return print(self.ERROR_RESPONSE)


    # POST Method 'set_pay_password' is used to set-up your new payment password. 
    # Warning - if you have never use payment password - go through 'https://market.csgo.com/checkout/password' to make it once.
    def set_pay_password(self, new_password: str = None):
        if new_password == None or self.payment_password == None:
            return print('Вы не установили платежный пароль и/или не ввели новый платежный пароль')
        
        response = requests.post(f'https://market.csgo.com/api/v2/set-pay-password?old_password={self.payment_password}&new_password={new_password}&key={self.token}').json()

        if response['success'] == True:
            self.payment_password = new_password
            print('Установлен новый платежный пароль!')
        else:
            print(self.ERROR_RESPONSE)


    # POST Method 'money_send' used to transfer balance from one to another account.
    # Don't forget to choose correct amount of money (1 RUB = 100, 1 USD = 1000, 1 EUR = 1000)
    def money_send(self, token_to: str, amount: str):
        if self.payment_password == None:
            return print(self.PAYMENT_PASSWORD_ERROR)
        
        response = requests.post(f'https://market.csgo.com/api/v2/money-send/{amount}/{token_to}?pay_pass={self.payment_password}&key={self.token}').json()
        curr = requests.post(f'https://market.csgo.com/api/v2/get-money?key={self.token}').json()['currency']

        if curr == 'RUB':
            amount_sep = 100
        else:
            amount_sep = 1000

        if response['success'] == True:
            return print(f'Успешно переведено {amount / amount_sep} {curr}!')
        else:
            return print(self.ERROR_RESPONSE)


    # POST Method 'money_send_history' shows transfer balance history. 
    def money_send_history(self, page: str = '0'):
        response = requests.post(f'https://market.csgo.com/api/v2/money-send-history/{page}?key={self.token}').json()

        checkup_list = [] # To Do - giga bicycle that needed to fix

        if response['success'] == True:
            if response['data'] == checkup_list:
                return print(self.NULL_HISTORY_ERROR)
            else:
                return print(f'Последний трансфер\n'
                             f'Куда - {response["data"][0]["to"]}\n'
                             f'Сколько - {response["data"][0]["amount_from"]} {response["data"][0]["currency_from"]}')
        else:
            return print(self.ERROR_RESPONSE)


    # POST Method 'set_steam_api_key' links your account w/ SteamAPI by Steam API Key
    def set_steam_api_key(self, steam_api_key: str):
        response = requests.post(f'https://market.csgo.com/api/v2/set-steam-api-key?key={self.token}&steam-api-key={steam_api_key}').json()

        if response['success'] == True:
            return print(f'Steam API Key {steam_api_key} успешно привязан к вашему аккаунту!')
        else:
            return print(self.INCORRECT_STEAM_KEY)


    # POST Method 'set_trade_link' sets up new trade link w/ your account.
    # You can find your link here -> http://steamcommunity.com/profiles/YOUR-STEAM-ID/tradeoffers/privacy.
    def set_trade_link(self, link: str):
        trade_token = link.split(sep='=')[2]

        response = requests.post(f'https://market.csgo.com/api/v2/set-trade-token?key={self.token}&token={trade_token}').json()

        if response['success'] == True:
            return print('Ссылка успешно установлена!')
        else:
            return print(self.INCORRECT_TRADE_LINK)


    # POST Method 'change_currency' change your account currency. By default in method 'new_currency' set 'USD'
    def change_currency(self, new_currency: str = 'USD'):
        response = requests.post(f'https://market.csgo.com/api/v2/change-currency/{new_currency}?key={self.token}')

        if response['success'] == True:
            return print(f'Валюта аккаунта успешно изменена!')
        else:
            if response['error'] == 1001: # ToDo: here and below should change to exceptions
                return print('Нельзя менять валюту, пока у Вас выставлены товары на продажу. Дождитесь когда их купят, или снимите с продажи.')
            if response['error'] == 1003:
                return print('Нельзя менять валюту, пока у Вас есть активные заявки на вывод. Дождитесь когда они будут исполнены, или отмените их вручную.')
            if response['error'] == 1004:
                return print('У Вас уже выбрана данная валюта')
            if response['error'] == 1005:
                return print('Выбрана неверная валюта')
            if response['error'] == 1007:
                return print('Ошибка. Вы два или более раз попытались отправить запрос на смену валюты.')    