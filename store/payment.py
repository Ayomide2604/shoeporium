import requests
from django.conf import settings
import json


class PaystackPayment:
    @staticmethod
    def initialize_payment(order):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": order.email,
            "amount": int(order.total_order() * 100),  # Convert to kobo/cents
            "reference": str(order.id),
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response_data['status']:
                return {
                    'status': True,
                    'payment_url': response_data['data']['authorization_url'],
                    'reference': response_data['data']['reference']
                }
            return {
                'status': False,
                'message': response_data['message']
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }

    @staticmethod
    def verify_payment(reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()

            if response_data['status']:
                return {
                    'status': True,
                    'payment_status': response_data['data']['status'],
                    'amount': response_data['data']['amount'],
                    'reference': response_data['data']['reference']
                }
            return {
                'status': False,
                'message': response_data['message']
            }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
