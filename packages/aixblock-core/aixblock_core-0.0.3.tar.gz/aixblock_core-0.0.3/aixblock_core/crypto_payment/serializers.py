from rest_framework import serializers


class CryptoRentSerializer(serializers.Serializer):
    # invoiceId = serializers.CharField(required=False)
    walletAddress = serializers.CharField(required=False)
    # amountUSD = serializers.FloatField(required=True)


class CryptoRefundSerializer(serializers.Serializer):
    history_id = serializers.CharField(required=False)
    walletAddress = serializers.CharField(required=True)
    # amountUSD = serializers.FloatField(required=True)

class ActiveComputeBuyByCryptoSerializer(serializers.Serializer):
    invoiceId = serializers.CharField(required=True)
    walletAddress = serializers.CharField(required=False)
    totalAmountUSD = serializers.FloatField(required=True)
    mintToken = serializers.FloatField(required=False)
    method = serializers.CharField(required=True)
    txnHash = serializers.FloatField(required=False)