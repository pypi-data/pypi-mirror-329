from utility.requesting import SyncRetryClient
import  requests

class GatewayHandler:
    def __init__(self, merchant_id, base_url: str):
        self.merchant_id = merchant_id
        self.base_url = base_url.rstrip('/')
        self.request = SyncRetryClient()

    def paylink(self, amount:int, callback_url: str, mobile: str, email: str, description=None)->requests.Response:
        
        '''
        Create a paylink
        :param amount: Amount in cents
        :param callback_url: Callback URL
        :param mobile: Mobile number
        :param email: Email address
        :param description: Description
        :return json:
            {
                    'status': True,
                    'data': {
                        'payment_url': payment_url,
                        'token': transaction.user_token,
                        'amount': float(transaction.amount),
                    },
                    'error': None
                }
        
        '''
        url = f'{self.base_url}/create/'
        headers = {
            'Authorization': f'Token {self.merchant_id}'
        }
        data = {
            'amount': amount,
            'callback_url': callback_url,
            'phone': mobile,
            'email': email,
            'description': description
        }
        return self.request.post(url, data, headers=headers)

    def verify(self, amount: int, token: str)->requests.Response:
        '''
        Verify a transaction
        :param amount: Amount in cents
        :param token: Transaction token
        :return json:
            {
                    'status': True,
                    'amount': float,
                    'error': None
                }
        '''
        url = f'{self.base_url}/verify/'
        headers = {
            'Authorization': f'Token {self.merchant_id}'
        }

        data = {
            'amount': amount,
            'token': token,
        }
        return self.request.post(url, data, headers=headers)
