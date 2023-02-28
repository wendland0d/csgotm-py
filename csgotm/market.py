from csgotm.exceptions import *

from typing import Union
import requests

class Market():

    """
    Main class for touch CS:GO Market API    
    """
    def __init__(self, token: str, payment_password: Union[str, None] = None) -> None:
        self.token = token
        self.payment_password = payment_password

    """
    Methods for getting in-site information about items, buy-orders and sell-orders
    """
    @staticmethod
    def show_prices(currency: str = "USD") -> dict:
        """
        Returns `dict` object contains all market items
        
        :param currency: Takes chosen currency into GET-request
        :raises csgotm.exceptions.market_exceptions.CurrencyError: If chosen currency that not available now
        """

        if currency not in ['RUB', 'USD', 'EUR']:
            raise CurrencyError()
        
        response = requests.get(f'https://market.csgo.com/api/v2/prices/{currency}.json').json()
        return response
        
    @staticmethod
    def show_class_instance_price(currency: str = "USD") -> dict:
        """
        Returns `dict` object contains all market items with extended inforrmtion per item

        :param currency: Takes chosen currency into GET-request
        :raises csgotm.exceptions.market_exceptions.CurrencyError: If chosen currency that not available now
        """

        if currency not in ['RUB', 'USD', 'EUR']:
            raise CurrencyError()
        
        response = requests.get(f'https://market.csgo.com/api/v2/prices/class_instance/{currency}.json').json()
        return response
    
    @staticmethod
    def show_buy_orders(currency: str = "USD") -> dict:
        if currency not in ['RUB', 'USD', 'EUR']:
            raise CurrencyError()
        
        response = requests.get(f'https://market.csgo.com/api/v2/prices/orders/{currency}.json').json()

        return response


    """
    Personal account methods 
    """
    def ping(self) -> dict:
        """
        Returns `dict` object contains ping-pong status of account

        :raises csgotm.exceptions.DataOrApiKeyError: If got invalid token
        """
        response = requests.post(f'https://market.csgo.com/api/v2/ping?key={self.token}').json()

        if response['success'] == True:
            return response
        else:
            raise DataOrApiKeyError() 

    def get_money(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/get-money?key={self.token}').json()

        if response['success'] == True:
            return response
        else:
            raise DataOrApiKeyError()

    def go_offline(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/go-offline?key={self.token}').json()

        if response['success'] == True:
            return response
        else:
            raise DataOrApiKeyError()
        
    def update_inventory(self) -> dict:
        """
        POST Method 'update_inventory' refreshes the inventory cache (recommended to do after each accepted trade offer)
        """

        response = requests.post(f'https://market.csgo.com/api/v2/update-inventory/?key={self.token}').json()

        if response['success'] == True:
            return response
        else:
            raise DataOrApiKeyError()

    def get_my_steam_id(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/get-my-steam-id?key={self.token}').json()

        if response['success'] == True:
            return {'steamid32':response['steamid32'], 'steamid64':response['steamid64']}
        else:
            raise DataOrApiKeyError()
        
    def set_pay_password(self, new_password: Union[str, None] = None) -> dict:
        if self.payment_password == None:
            raise EmptyPaymentPasswordError()
        if new_password == None:
            raise NewPaymentPasswordError()
        
        response = requests.post(f'https://market.csgo.com/api/v2/set-pay-password?old_password={self.payment_password}&new_password={new_password}&key={self.token}').json()

        if response['success'] == True:
            self.payment_password = new_password
            return response
        else:
            return DataOrApiKeyError()
        
    def money_send(self, token_to: str, amount: str) -> str:
        if self.payment_password == None:
            raise EmptyPaymentPasswordError()
        
        response = requests.post(f'https://market.csgo.com/api/v2/money-send/{amount}/{token_to}?pay_pass={self.payment_password}&key={self.token}').json()
        curr = requests.post(f'https://market.csgo.com/api/v2/get-money?key={self.token}').json()['currency']

        if curr == 'RUB':
            amount_sep = 100
        else:
            amount_sep = 1000

        if response['success'] == True:
            return f'Successfully transferred {amount / amount_sep} {curr}!'
        else:
            raise DataOrApiKeyError()
        
    def money_send_history(self, page: str = '0', full_history: bool = False) -> dict:
            response = requests.post(f'https://market.csgo.com/api/v2/money-send-history/{page}?key={self.token}').json()

            checkup_list = [] # To Do - giga bicycle that needed to fix

            if response['success'] == True:
                if response['data'] == checkup_list:
                    raise NullHistoryError()
                else:
                    if full_history == False:
                        return {'To' : response['data'][0]['to'], 'Amount' : response['data'][0]['amount_from']}
                    else:
                        return response
            else:
                raise DataOrApiKeyError()
            
    def set_steam_api_key(self, steam_api_key: str) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/set-steam-api-key?key={self.token}&steam-api-key={steam_api_key}').json()

        if response['success'] == True:
            return {'success': True, 'steam_api': steam_api_key}
        else:
            raise IncorectSteamKeyError()
        
    def set_trade_link(self, link: str) -> dict:
        trade_token = link.split(sep='=')[2]

        response = requests.post(f'https://market.csgo.com/api/v2/set-trade-token?key={self.token}&token={trade_token}').json()

        if response['success'] == True:
            return {'success': True, 'link': link}
        else:
            raise InvalidSteamLinkError()
        
    def change_currency(self, new_currency: str = 'USD') -> dict:
        if new_currency not in ['RUB', 'USD', 'EUR']:
            raise CurrencyError()

        response = requests.post(f'https://market.csgo.com/api/v2/change-currency/{new_currency}?key={self.token}')

        if response['success'] == True:
            return {'success': True, 'actual_currency': new_currency}
        else:
            if response['error'] == 1001: # ToDo: here and below should change to exceptions
                raise ItemsOnSaleError()
            if response['error'] == 1003:
                raise ActiveWithdrawlsError()
            if response['error'] == 1004:
                raise CurrencySelectedError()
            if response['error'] == 1005:
                raise CurrencyError()
            if response['error'] == 1007:
                raise CurrencyDoubleChangeError()
            
    """
    Account's methods. Trades methods
    """

    def trade_request_take(self, bot_id: Union[int, None] = None) -> dict:
        request_link = f'https://market.csgo.com/api/v2/trade-request-take?key={self.token}'
        if bot_id != None:
            request_link += f'&bot={bot_id}'

        response = requests.post(request_link).json()

        if response['success'] == True:
            return response
        else:
            raise EmptyBotTrade()
        
    def trade_request_give(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/trade-request-give?key={self.token}').json

        if response['success'] == True:
            return response
        else:
            raise EmptyBotTrade()

    def trade_request_give_p2p(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/trade-request-give-p2p?key={self.token}').json()

        return response
    
    def trade_request_give_p2p_all(self) -> dict:
        response = requests.post(f'https://market.csgo.com/api/v2/trade-request-give-p2p-all?key={self.token}')

        return response
    
