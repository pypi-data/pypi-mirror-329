"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.urls import path, include
from . import api

app_name = 'crypto_payment'

_api_urlpatterns = [
    path('create-order', api.CreateOrderAPI.as_view(), name='create-order'),
    path('refund-order', api.RefunedOrderAPI.as_view(), name='refund-order'),
    path('webhooks', api.ActiveComputeBuyByCrypto.as_view(), name='webhooks-order')
]

urlpatterns = [
    path('api/crypto-payment/', include((_api_urlpatterns, app_name), namespace='api-crypro')),
]
