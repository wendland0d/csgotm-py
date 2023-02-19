class Market():
    """
    Main class for touch CS:GO Market API    
    """
    ERROR_RESPONSE = 'Данные недоступны и/или отсутствуют. Проверьте API-ключ'
    PAYMENT_PASSWORD_ERROR = 'Необходимо использовать платежный пароль!'
    NULL_HISTORY_ERROR = 'История переводов недоступна - нет зафиксированных ранее переводов'
    INCORRECT_STEAM_KEY = 'Проверьте корректность Steam API ключа'
    INCORRECT_TRADE_LINK = 'Проверьте коррекстность трейд-ссылки'

    def __init__(self, token: str, payment_password: str = None) -> None:
        self.token = token
        self.payment_password = payment_password

        
