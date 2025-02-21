from rest_framework import serializers
from .models import Order, OrderComputeGPU
from compute_marketplace.models import Trade, History_Rent_Computes
from compute_marketplace.serializers import HistoryRentComputeSerializer, ComputeGPUSerializer
import django_filters
from django.db.models import Q

class OrderSerializer(serializers.ModelSerializer):
    history_order = serializers.SerializerMethodField()
    gpu_info = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = "__all__"
    
    def get_history_order(self, obj):
        # Extract the last ID from `model_new_id`
        order_id = obj.id
        history_instance = History_Rent_Computes.objects.filter(order_id=order_id).first()
        if history_instance:
            return HistoryRentComputeSerializer(history_instance).data
        else:
            return None

    def get_gpu_info(self, obj):
        order_id = obj.id
        order_gpu_instance = OrderComputeGPU.objects.filter(order_id=order_id).first()
        if order_gpu_instance:
            return ComputeGPUSerializer(order_gpu_instance.compute_gpu).data
        else:
            return None

class OrderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.CharFilter(lookup_expr="icontains")
    catalog_id = django_filters.NumberFilter()
    all = django_filters.CharFilter(method="filter_all")

    class Meta:
        model = Order
        fields = ["total_amount", "status", "unit", "all"]

    def filter_all(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(name__icontains=value) | Q(status__icontains=value)
            )
        return queryset


class TradePaymentSerializer(serializers.Serializer):
    class Meta:
        model = Trade
        fields = "__all__"
