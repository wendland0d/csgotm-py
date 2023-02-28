class CurrencyError(Exception):
    def __init__(self, text: str = 'Wrong currency selected') -> None:
        self.text = text

class DataOrApiKeyError(Exception):
    def __init__(self, text: str = 'Data not available and/or missing. Check API Key') -> None:
        self.text = text

class EmptyPaymentPasswordError(Exception):
    def __init__(self, text: str = 'You have not set a payment password') -> None:
        self.text = text

class NewPaymentPasswordError(Exception):
    def __init__(self, text: str = 'You have not entered a new payment password') -> None:
        self.text = text

class NullHistoryError(Exception):
    def __init__(self, text: str = 'There are no transaction records in the history') -> None:
        self.text = text
        
class IncorectSteamKeyError(Exception):
    def __init__(self, text: str = 'Check if the Steam API key is correct') -> None:
        self.text = text

class InvalidSteamLinkError(Exception):
    def __init__(self, text: str = 'Check if the trade link is correct') -> None:
        self.text = text

class ItemsOnSaleError(Exception):
    def __init__(self, text: str = 'You cannot change the currency while you have goods for sale. Wait until they are bought, or withdraw from sale.') -> None:
        self.text = text
    
class ActiveWithdrawlsError(Exception):
    def __init__(self, text: str = 'You cannot change the currency while you have active withdrawal requests. Wait until they are executed, or cancel them manually.') -> None:
        self.text = text

class CurrencySelectedError(Exception):
    def __init__(self, text: str = 'You already have this currency selected') -> None:
        self.text = text

class CurrencyDoubleChangeError(Exception):
    def __init__(self, text: str = 'You tried to send a currency change request two or more times.') -> None:
        self.text = text

class EmptyBotTrade(Exception):
    def __init__(self, text: str = 'Nothing to send or receive') -> None:
        self.text = text