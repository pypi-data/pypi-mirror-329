import threading
import json
import logging
import uuid

import requests
from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

from compute_marketplace.models import ComputeMarketplace, ComputeTimeWorking, Trade, ComputeGpuPrice, History_Rent_Computes, ComputeGPU
from compute_marketplace.serializers import HistoryRentComputeSerializer
from orders.models import Order, OrderComputeGPU

from crypto_payment import serializers
import drf_yasg.openapi as openapi
from compute_marketplace.plugin_provider import vast_provider, exabit_provider
from compute_marketplace.functions import notify_for_compute, check_compute_run_status

from configs.models import InstallationService
from core.settings.base import SERVICE_FEE, AIXBLOCK_IMAGE_NAME, ENVIRONMENT, MAIL_SERVER, EXABBIT_SHOW
from django.db.models import Q, OuterRef, Subquery

from plugins.plugin_centrifuge import publish_message
from compute_marketplace.self_host import update_notify_install
from aixblock_core.users.service_notify import send_email_thread
from aixblock_core.core.utils.nginx_server import NginxReverseProxy

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from aixblock_core.core.utils.params import get_env
from core.utils.convert_memory_to_byte import convert_gb_to_byte
from core.utils.docker_container_pull import dockerContainerPull
from core.utils.docker_container_action import dockerContainerStartStop
from core.utils.docker_kubernetes_info import checkDockerKubernetesStatus

CRYPTO_API = settings.CRYPTO_API


request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the token, e.g., 'US Dollar'",
        ),
        "token_symbol": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Symbol of the token, e.g., 'USD'",
        ),
        "price": openapi.Schema(
            type=openapi.TYPE_NUMBER,
            format="float",
            description="Price value, e.g., 0.117",
        ),
        "account": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Account ID, e.g., 2",
        ),
        "walletAddress":  openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Account ID, e.g., 2",
        ),
        "compute_gpus_rent": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Compute GPU ID"
                    ),
                    "hours": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Duration in hours for this GPU",
                    ),
                },
            ),
            description="List of compute GPU IDs with corresponding hours",
        ),
        "compute_rent_vast": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Vast contract ID"
                    ),
                    "hours": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Duration in hours for this contract",
                    ),
                },
            ),
            description="List of vast contract IDs with corresponding hours",
        ),
         "compute_cpus_rent": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_STRING, description="rent cpu. Compute ID (have is_using_cpu = True)"
                    ),
                    "hours": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Duration in hours for this contract",
                    ),
                },
            ),
            description="List of vast contract IDs with corresponding hours",
        ),
    },
    required=[
        "token_name",
        "token_symbol",
        "price",
        "account",
    ],
)

@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Crypto Payment"],
        operation_summary="Create crypto payment order",
        request_body=request_body,
    ),
)
class CreateOrderAPI(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.CryptoRentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = self.request.user.id

            compute_gpus_rent = self.request.data.get("compute_gpus_rent")
            compute_rent_vast = self.request.data.get("compute_rent_vast") 
            compute_rent_exabit = self.request.data.get("compute_rent_exabit") 

            price = self.request.data.get("price")
            token_symbol = self.request.data.get("token_symbol")
            token_name = self.request.data.get("token_name")
            walletAddress = self.request.data.get("walletAddress")

            type_payment = "crypto"

            def calculate_time_end(compute_id, hours):
                # Get the current time as the start time
                time_start = datetime.utcnow().replace(tzinfo=timezone.utc)           
                hours = int(hours)
                remaining_hours = hours
                time_working = ComputeTimeWorking.objects.filter(
                        Q(compute_id=compute_id), deleted_at__isnull=True
                    ).first()
                # Define variables for tracking the nearest future range
                min_start_day_future = None
                # Initialize max end day as the earliest possible datetime
                max_end_day = datetime.min.replace(tzinfo=timezone.utc)
                remaining_hours_future = remaining_hours
                day_ranges = time_working.day_range
                # Iterate through each day range and find the maximum end day
                for day_range in day_ranges:
                    end_day = datetime.fromisoformat(day_range["end_day"].rstrip("Z")).replace(tzinfo=timezone.utc)
                    if end_day > max_end_day:
                        max_end_day = end_day

                # Calculate the total hours within the provided day_ranges
                total_available_hours = sum((datetime.fromisoformat(dr["end_day"].replace("Z", "+00:00")) - 
                                    datetime.fromisoformat(dr["start_day"].replace("Z", "+00:00"))).total_seconds() / 3600 
                                    for dr in day_ranges)

                # If total hours exceed the provided day_ranges, return max end day
                if hours > total_available_hours:
                    return max_end_day.strftime("%Y-%m-%d %H:%M:%S%z")

                # Iterate through each day range and find applicable ranges
                for day_range in day_ranges:
                    start_day = datetime.fromisoformat(day_range["start_day"].rstrip("Z")).replace(tzinfo=timezone.utc)
                    end_day = datetime.fromisoformat(day_range["end_day"].rstrip("Z")).replace(tzinfo=timezone.utc)

                    # Check if the current time is within the range (present)
                    if start_day <= time_start <= end_day:
                        available_time = (end_day - time_start).total_seconds() / 3600
                        if remaining_hours <= available_time:
                            return (time_start + timedelta(hours=remaining_hours)).strftime(
                                "%Y-%m-%d %H:%M:%S%z"
                            )
                        remaining_hours -= available_time
                        time_start = end_day

                    # Check if the range is in the near future
                    elif time_start < start_day and start_day - time_start <= timedelta(days=7):
                        if min_start_day_future is None or start_day < min_start_day_future:
                            min_start_day_future = start_day
                            remaining_hours_future = remaining_hours

                    # Check if the range is in the distant future
                    elif time_start < start_day:
                        if min_start_day_future is None:
                            min_start_day_future = start_day
                            remaining_hours_future = remaining_hours

                # If there's a nearest future range, calculate remaining hours for it
                if min_start_day_future is not None:
                    return (
                        min_start_day_future + timedelta(hours=remaining_hours_future)
                    ).strftime("%Y-%m-%d %H:%M:%S%z")

                # If remaining hours exceed available ranges, return max end day
                return max_end_day.strftime("%Y-%m-%d %H:%M:%S%z") if max_end_day else None
                # create order, minus money from portfolio wallet, create History rent

            def process_payment(price, portfolio, token_symbol, user_id):
                # create order
                order_instance = Order.objects.create(
                        total_amount=1,
                        price=price,
                        unit=token_symbol,
                        status="pending",
                        user_id=user_id,
                    )

                order_instance.save()
                # fee = float(price) * float(SERVICE_FEE) / 100
                amount = float(price) 

                # Cập nhật trạng thái của order
                order_instance.status = "pending"
                order_instance.service_fee = SERVICE_FEE
                order_instance.save()
                order_id = order_instance.pk

                return {"amount": amount, "order_id": order_id}
            
            def create_trade_data(token_name, token_symbol, amount, price, compute_gpu_id, user_id, order_id, type_payment):
                trade_data = {
                        "token_name": token_name,
                        "token_symbol": token_symbol,
                        "amount": amount,
                        "price": price,
                        "type": "Market Fund",
                        "status": "completed",
                        "resource": "compute_marketplace",  # with cpu
                        "resource_id": compute_gpu_id,  # with cpu - using compute Id
                        "account_id": user_id,
                        "order": order_id,
                        "payment_method": type_payment
                    }
                
                Trade.objects.create(**trade_data)
            
            payment = process_payment(
                price, None, token_symbol, user_id
            )

            req = requests.post(
                CRYPTO_API + "/api/v1/sign-message/rent",
                headers={
                    # "Authorization": "Basic " + basic_token,
                    "Content-Type": "application/json",
                },

                data=json.dumps({
                    "invoiceId": f'{payment["order_id"]}',
                    "walletAddress": f'{walletAddress}',
                    "amountUSD": price
                })
            )

            data = req.json()

            if not req.ok:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            for compute_vast in compute_rent_vast:
                compute_vast_id = compute_vast["id"]
                compute_vast_hours = compute_vast["hours"]
                type = compute_vast["type"]
                vast_price = compute_vast["price"]
                disk_size  = compute_vast["diskSize"]
                # check exited and refund
                compute_existed = ComputeMarketplace.objects.filter(infrastructure_id=compute_vast_id, deleted_at__isnull=True).exists()
                if compute_existed:
                    # xử lý hoàn tiền. vì có compute vast đang trong trạng thái thuê
                    break

                compute = ComputeMarketplace.objects.create(
                    # name=response['instances']['public_ipaddr'],
                    status="rented_bought",
                    infrastructure_id=compute_vast_id,
                    infrastructure_desc=compute_vast_id,
                    owner_id=0,
                    author_id=user_id,
                    organization_id=self.request.user.active_organization_id,
                    config=json.dumps(
                        {
                            "cpu": "",
                            "ram": "",
                            "disk": "",
                            "diskType": "",
                            "os": "",
                        }
                    ),
                    # ip_address=response["instances"]["public_ipaddr"],
                    # port=response['instances']['ports'][f'{port_tem}/tcp'][0]["HostPort"],
                    type="MODEL-PROVIDER-VAST",
                    client_id="",
                    client_secret="",
                    ssh_key="",
                    price=0,
                    compute_type=type,
                    is_using_cpu=False,
                )

                compute_gpu = ComputeGPU.objects.create(
                    compute_marketplace=compute,
                    infrastructure_id=compute,
                    gpu_id=compute_vast_id,
                    gpu_name="",#response["instances"]["gpu_name"],
                    memory_usage="", #response["instances"]["mem_usage"],
                    gpu_memory="", #response["instances"]["gpu_mem_bw"],
                    gpu_tflops="", #response["instances"]["total_flops"],
                    status="renting",
                    disk=disk_size
                )

                OrderComputeGPU.objects.create(
                    order_id=payment["order_id"], compute_gpu_id=compute_gpu.id
                )

                ComputeGpuPrice.objects.create(compute_gpu_id=compute_gpu, token_symbol='usd', price=vast_price  , compute_marketplace_id=compute)
                time_start = timezone.now()
                time_end = time_start + timedelta(hours=compute_vast_hours)
                # time_end = time_start + timedelta(hours=1)
                # # time_end = calculate_time_end(compute.id, compute_vast_hours)

                history_vast = History_Rent_Computes.objects.create(
                    account_id=user_id,
                    compute_marketplace=compute,
                    compute_gpu=compute_gpu,
                    status="renting",
                    order_id=payment["order_id"],
                    rental_hours=compute_vast_hours,
                    time_start=time_start,
                    time_end=time_end,
                    compute_install=History_Rent_Computes.InstallStatus.WAIT_CRYPTO,
                    service_type = type
                )

                create_trade_data(token_name=token_name, token_symbol='usd', amount=vast_price*compute_vast_hours, price=vast_price, compute_gpu_id=compute_gpu.id, user_id=user_id, order_id=payment["order_id"], type_payment=type_payment)
            
            for compute_exabit in compute_rent_exabit:
                compute_exabit_id = compute_exabit["id"]
                compute_exabit_hours = compute_exabit["hours"]
                type = compute_exabit["type"]
                exabit_price = compute_exabit["price"]


                compute_existed = ComputeMarketplace.objects.filter(infrastructure_id=compute_exabit_id, deleted_at__isnull=True).exists()
                if compute_existed:
                    # xử lý hoàn tiền. vì có compute vast đang trong trạng thái thuê
                    break

                compute = ComputeMarketplace.objects.create(
                    # name=response['instances']['public_ipaddr'],
                    status="rented_bought",
                    infrastructure_id=compute_exabit_id,
                    infrastructure_desc=compute_exabit_id,
                    owner_id=0,
                    author_id=user_id,
                    organization_id=self.request.user.active_organization_id,
                    config=json.dumps(
                        {
                            "cpu": "",
                            "ram": "",
                            "disk": "",
                            "diskType": "",
                            "os": "",
                        }
                    ),
                    # ip_address=response["instances"]["public_ipaddr"],
                    # port=response['instances']['ports'][f'{port_tem}/tcp'][0]["HostPort"],
                    type=ComputeMarketplace.Type.PROVIDEREXABIT,
                    client_id="",
                    client_secret="",
                    ssh_key="",
                    price=0,
                    compute_type=type,
                    is_using_cpu=False,
                )

                compute_gpu = ComputeGPU.objects.create(
                    compute_marketplace=compute,
                    infrastructure_id=compute,
                    gpu_id=compute_exabit_id,
                    gpu_name="",#response["instances"]["gpu_name"],
                    memory_usage="", #response["instances"]["mem_usage"],
                    gpu_memory="", #response["instances"]["gpu_mem_bw"],
                    gpu_tflops="", #response["instances"]["total_flops"],
                    status="renting",
                )

                OrderComputeGPU.objects.create(
                    order_id=payment["order_id"], compute_gpu_id=compute_gpu.id
                )

                ComputeGpuPrice.objects.create(compute_gpu_id=compute_gpu, token_symbol='usd', price=exabit_price  , compute_marketplace_id=compute)
                time_start = timezone.now()
                time_end = time_start + timedelta(hours=compute_exabit_hours)
                # time_end = time_start + timedelta(hours=1)
                # # time_end = calculate_time_end(compute.id, compute_vast_hours)

                history_exabit = History_Rent_Computes.objects.create(
                    account_id=user_id,
                    compute_marketplace=compute,
                    compute_gpu=compute_gpu,
                    status="renting",
                    # order_id=payment["order_id"],
                    rental_hours=compute_exabit_hours,
                    time_start=time_start,
                    time_end=time_end,
                    compute_install=History_Rent_Computes.InstallStatus.WAIT_CRYPTO,
                    service_type = type 
                )

                create_trade_data(token_name=token_name, token_symbol='usd', amount=exabit_price*compute_exabit_hours, price=exabit_price, compute_gpu_id=compute_gpu.id, user_id=user_id, order_id=payment["order_id"], type_payment=type_payment)

            def install_and_buy_gpu(gpu_id, hours, type):
                compute_gpu_price = ComputeGpuPrice.objects.filter(compute_gpu_id=gpu_id).first() 
                try:
                    compute_gpu = ComputeGPU.objects.filter(
                        id=gpu_id, deleted_at__isnull=True
                    ).first()
                    
                    if compute_gpu is None:
                        return Exception({"error": "Compute Gpu Not found"}, status=400)
                    
                    if int(compute_gpu.user_rented) >= int(compute_gpu.max_user_rental):
                        return Exception(
                            {"error": "Compute gpu has reached its limit"}, status=400
                        )
                    
                    compute = ComputeMarketplace.objects.filter(
                        Q(id=compute_gpu.compute_marketplace_id), deleted_at__isnull=True
                    ).first()

                    compute.compute_type = type
                    compute.save()

                    if not compute:
                        return Exception({"error": "Compute not found"}, status=400)
                    
                except Exception as e:
                    return Response({"error": str(e)})

                OrderComputeGPU.objects.create(
                    order_id=payment["order_id"], compute_gpu_id=compute_gpu.id
                )

                create_trade_data(token_name=token_name, token_symbol='usd', amount=float(compute_gpu_price.price) * float(hours), price=float(compute_gpu_price.price), compute_gpu_id=compute_gpu.id, user_id=user_id, order_id=payment["order_id"], type_payment=type_payment)

                time_end = calculate_time_end(compute.id, hours)
                compute_gpu_rented = History_Rent_Computes.objects.filter(
                    Q(compute_gpu_id=gpu_id),
                    Q(status="renting"),
                    Q(account_id=user_id),
                    deleted_at__isnull=True,
                    deleted_by__isnull = True
                ).first()
                if compute_gpu_rented:
                    return Response({"detail": "Compute GPUs were rented"}, status=400)

                history = History_Rent_Computes.objects.create(
                    account_id=user_id,
                    compute_marketplace_id=compute_gpu.compute_marketplace_id,
                    compute_gpu_id=gpu_id,
                    status="renting",
                    rental_hours=hours,
                    time_end=time_end,
                    service_type = type if type else "full" if type == "all" else "full",
                    compute_install=History_Rent_Computes.InstallStatus.WAIT_CRYPTO,
                    ip_address = compute.ip_address,
                    container_network = f"aixblock_network_u{user_id}_g{gpu_id}_i{compute_gpu.gpu_index}",
                    order_id=payment["order_id"]
                )
                # save rented +1
                compute_gpu.user_rented +=1
                compute_gpu.save()

            for compute_gpu_rent in compute_gpus_rent:
                gpu_id = compute_gpu_rent["id"]
                hours = compute_gpu_rent["hours"]
                type = compute_gpu_rent["type"]
                thread = threading.Thread(
                    target=install_and_buy_gpu,
                    args=(gpu_id, hours, type),
                )
                thread.start()

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logging.error(e)
            return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Crypto Payment"],
        operation_summary="Refund Crypto Payment",
        request_body=serializers.CryptoRefundSerializer,
    ),
)
class RefunedOrderAPI(generics.CreateAPIView):
    # queryset = History_Rent_Computes.objects.all()
    serializer_class = HistoryRentComputeSerializer

    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id", None)
        history_id = request.data.get("history_id")
        
        instance = History_Rent_Computes.objects.filter(id=history_id).first()

        compute_marketplace = instance.compute_marketplace
        compute_gpu = instance.compute_gpu

        try:
            from ml.models import MLBackend, MLGPU, MLBackendStatus
            ml_gpu = MLGPU.objects.filter(compute_id=instance.compute_marketplace_id, deleted_at__isnull=True).first()
            if ml_gpu:
                ml_gpu.deleted_at = timezone.now()
                MLBackend.objects.filter(id=ml_gpu.ml_id, deleted_at__isnull=True).update(deleted_at=timezone.now())
                MLBackendStatus.objects.filter(ml_id=ml_gpu.ml_id, deleted_at__isnull=True).update(deleted_at=timezone.now())
                ml_gpu.save()
                # ModelMarketplace.objects.filter(id=ml_gpu.model_id).delete()
        
            def remove_proxy(compute_marketplace):
                if compute_marketplace:
                    nginx_proxy_manager = NginxReverseProxy(f'{settings.REVERSE_ADDRESS}', f'{compute_marketplace.ip_address}_{compute_marketplace.port}')
                    nginx_proxy_manager.remove_nginx_service()

                if compute_marketplace.api_port:
                    nginx_proxy_manager = NginxReverseProxy(f'{settings.REVERSE_ADDRESS}', f'{compute_marketplace.ip_address}_{compute_marketplace.api_port}')
                    nginx_proxy_manager.remove_nginx_service()

            thread = threading.Thread(target=remove_proxy, args=(compute_marketplace,))
            thread.start()
            
        except Exception as e:
            print(e)

        if project_id:
            try:
                notify_for_compute(request.user.uuid, "Success", "The compute has been successfully removed from project")
            except Exception as e:
                print(e)

            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.deleted_at = timezone.now()
        instance.deleted_by = History_Rent_Computes.DELETED_BY.MANUAL_USER
        instance.status = "completed"

        if instance.compute_gpu_id is not None:
            compute_gpu = ComputeGPU.objects.filter(id=instance.compute_gpu_id).first()
            compute_gpu.quantity_used = 0
            if compute_gpu.user_rented > 0:
                compute_gpu.user_rented -= 1
                compute_gpu.save()
            compute_gpu.status = ComputeGPU.Status.IN_MARKETPLACE
            _infrastructure_id = compute_marketplace.infrastructure_id

            if Trade.objects.filter(resource_id=compute_gpu.id, order=instance.order_id, payment_method="crypto"):
                import math
                try:
                    compute_price = ComputeGpuPrice.objects.filter(compute_gpu_id=compute_gpu.id).order_by("-id").first()
                    time_now = timezone.now()
                    time_end = instance.time_end

                    if instance.time_end or time_now >= time_end:
                        hours_remaining = (instance.time_end - timezone.now()).total_seconds() / 3600
                        refund_amount = hours_remaining * compute_price.price
                        amount = math.floor(refund_amount * 1000) / 1000

                        req = requests.post(
                            settings.CRYPTO_API + "/api/v1/sign-message/cancel",
                            headers={
                                # "Authorization": "Basic " + basic_token,
                                "Content-Type": "application/json",
                            },

                            data=json.dumps({
                                "invoiceId": f'{instance.order_id}',
                                "walletAddress": request.data["walletAddress"],
                                "amountUSD": amount
                            })
                        )

                        data = req.json()

                        if not req.ok:
                            return Response(data, status=status.HTTP_400_BAD_REQUEST)
                        
                        # return Response(data, status=status.HTTP_200_OK)
                
                except Exception as e:
                    logging.error(e)
                    # return Response({"message": e.__str__()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if instance.compute_marketplace.type == 'MODEL-PROVIDER-VAST':
                compute = ComputeMarketplace.objects.filter(
                    id=compute_gpu.compute_marketplace_id
                ).first()

                infrastructure_id = f"{compute_marketplace.infrastructure_id}-{uuid.uuid4()}"
                compute.infrastructure_id = infrastructure_id
                compute.deleted_at = timezone.now()
                compute.save()
                compute_gpu.infrastructure_id = compute
                compute_gpu.deleted_at = timezone.now()
                compute_gpu.save()

                # vast_service.delete_instance_info(instance.compute_marketplace.infrastructure_id)
                vast_provider.delete_compute(instance.compute_marketplace.infrastructure_id)

            elif instance.compute_marketplace.type == 'MODEL-PROVIDER-EXABIT':
                compute = ComputeMarketplace.objects.filter(
                    id=compute_gpu.compute_marketplace_id
                ).first()

                infrastructure_id = f"{compute_marketplace.infrastructure_id}-{uuid.uuid4()}"
                compute.infrastructure_id = infrastructure_id
                compute.deleted_at = timezone.now()
                compute.save()
                compute_gpu.infrastructure_id = compute
                compute_gpu.deleted_at = timezone.now()
                compute_gpu.save()

                if instance.compute_install != "failed":
                # vast_service.delete_instance_info(instance.compute_marketplace.infrastructure_id)
                    res = exabit_provider.delete_compute(instance.compute_marketplace.infrastructure_id)

                    if not res:
                        return Response(data={"message": "Instance is already in pending operation"}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                # pass
                try:
                    dockerContainerStartStop(
                        base_image='aixblock-platform',
                        action='delete', 
                        ip_address=compute_marketplace.ip_address,
                        gpu_id=compute_gpu.id,
                        user_id=self.request.user.id,
                        gpu_index=compute_gpu.gpu_index,
                        )
                    dockerContainerStartStop(
                        base_image='aixblock-minio',
                        action='delete', 
                        ip_address=compute_marketplace.ip_address,
                        gpu_id=compute_gpu.id,
                        user_id=self.request.user.id,
                        gpu_index=compute_gpu.gpu_index,
                        )
                    dockerContainerStartStop(
                        base_image="aixblock-postgres",
                        action="delete",
                        ip_address=compute_marketplace.ip_address,
                        gpu_id=compute_gpu.id,
                        user_id=self.request.user.id,
                        gpu_index=compute_gpu.gpu_index,
                    )
                except Exception as e:
                    print(f"An error occurred: {e}")

            compute_gpu.save()

        if instance is not None and instance.compute_gpu_id is None:
            compute = ComputeMarketplace.objects.filter(id=instance.compute_marketplace_id).first()
            _infrastructure_id = compute.infrastructure_id

            if compute is not None and compute.is_using_cpu:
                compute.author_id= compute.owner_id
                compute.status = ComputeGPU.Status.IN_MARKETPLACE
                compute.deleted_at = timezone.now()
                if compute.type == 'MODEL-PROVIDER-VAST':
                    # vast_service.delete_instance_info(compute.infrastructure_id)
                    vast_provider.delete_compute(compute.infrastructure_id)
                compute.save()
        

        try:
            notify_for_compute(request.user.uuid, "Success", "The compute has been successfully removed")
        except Exception as e:
            print(e)
            
        instance.save()

        return Response(data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Crypto Payment"],
        operation_summary="ActiveComputeBuyByCrypto",
        request_body=serializers.ActiveComputeBuyByCryptoSerializer,
    ),
)
class ActiveComputeBuyByCrypto(generics.CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = serializers.ActiveComputeBuyByCryptoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.data["invoiceId"]

        order_instance = Order.objects.filter(id=order_id)
        order_instance.status = "renting"

        history_instance = History_Rent_Computes.objects.filter(order_id=order_id)

        def send_mail_rent_compute(user, compute, model_endpoint, tensorboard, ddp_endpoint):
            send_to = user.username if user.username else user.email

            html_file_path =  './templates/mail/rent_compute_success.html'
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            html_content = html_content.replace('[user]', f'{send_to}')
            html_content = html_content.replace('xxx', f'{compute.id}')
            html_content = html_content.replace('[endpoint]', f'https://{compute.ip_address}:{model_endpoint}')
            html_content = html_content.replace('[tensorboard]', f'http://{compute.ip_address}:{tensorboard}')
            html_content = html_content.replace('[ddp]', f'{compute.ip_address}:{ddp_endpoint}')

            data = {
                "subject": "AIxBlock | Confirmation of Compute Rental",
                "from": "noreply@aixblock.io",
                "to": [f'{user.email}'],
                "html": html_content,
                "text": "Welcome to AIxBlock!",
                "attachments": []
            }

            docket_api = "tcp://69.197.168.145:4243"
            host_name = MAIL_SERVER

            email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
            email_thread.start()

        def send_mail_rent_compute_platform(user, compute, email_user, pass_user):
            send_to = user.username if user.username else user.email

            html_file_path =  './templates/mail/rent_compute_success_platform.html'
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            html_content = html_content.replace('[user]', f'{send_to}')
            html_content = html_content.replace('xxx', f'{compute.id}')
            html_content = html_content.replace('[domain]', f'https://{compute.ip_address}:{compute.port}')
            html_content = html_content.replace('[email]', email_user)
            html_content = html_content.replace('[pass]', pass_user)

            data = {
                "subject": "AIxBlock | Your Access Credentials to Your Private Platform",
                "from": "noreply@aixblock.io",
                "to": [f'{user.email}'],
                "html": html_content,
                "text": "Welcome to AIxBlock!",
                "attachments": []
            }

            docket_api = "tcp://69.197.168.145:4243"
            host_name = MAIL_SERVER

            def wait_platform(thread, url):
                import time
                while True:
                    try:
                        response = requests.get(url, verify=False)  # 'verify=False' bỏ qua SSL verification
                        if response.status_code == 200:
                            print("Response status code is 200: OK")
                            break
                        else:
                            print(f"Response status code is {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred: {e}")

                    time.sleep(10)

                thread.start()

            email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data))
            wait_platform = threading.Thread(target=wait_platform, args=(email_thread, f'https://{compute.ip_address}:{compute.port}/health'))
            wait_platform.start()
            # email_thread.start()

        def send_mail_s3(user, compute, email_user, pass_user, port_minio=None):
            compute = ComputeMarketplace.objects.filter(id = compute.id).first()
            html_file_path =  './templates/mail/s3_vast.html'
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # notify_reponse = ServiceSendEmail(DOCKER_API)
            html_content = html_content.replace('[user]', f'{user.email}')
            html_content = html_content.replace('xxx', f'{compute.id}')

            if not port_minio:
                html_content = html_content.replace('[endpoint_minio]', f'{compute.ip_address}:{compute.port}')
            else:
                html_content = html_content.replace('[endpoint_minio]', f'{compute.ip_address}:{port_minio}')

            try:
                nginx_proxy_manager = NginxReverseProxy(f'{settings.REVERSE_ADDRESS}', f'{compute.ip_address}_{compute.api_port}')
                nginx_proxy_manager.configure_reverse_proxy(f'{compute.ip_address}:{compute.api_port}', f'http://{compute.ip_address}:{compute.api_port}')
            except Exception as e:
                print(e)

            html_content = html_content.replace('[endpoint_minio_api]', f'http://{compute.ip_address}:{compute.api_port}')

            html_content = html_content.replace('[user_minio]', email_user)
            html_content = html_content.replace('[pass_minio]', pass_user)

            data = {
                "subject": f"AIxBlock | Confirmation of Compute Rental and Your Storage Access",
                "from": "noreply@aixblock.io",
                "to": [f"{user.email}"],
                "html": html_content,
                "text": "Remove compute!",
            }

            docket_api = "tcp://69.197.168.145:4243"
            host_name = MAIL_SERVER

            email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
            email_thread.start()
        
        def send_mail_refund(user, compute):
            send_to = user.username if user.username else user.email

            html_file_path =  './templates/mail/refund_compute.html'
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            html_content = html_content.replace('[user]', f'{send_to}')
            html_content = html_content.replace('xxx', f'{compute.id}')

            data = {
                "subject": "Compute Purchase Order Canceled and Refund Processed",
                "from": "noreply@aixblock.io",
                "to": [f'{user.email}'],
                "html": html_content,
                "text": "Compute Purchase Order Canceled!",
                "attachments": []
            }

            docket_api = "tcp://69.197.168.145:4243"
            host_name = MAIL_SERVER

            email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
            email_thread.start()
        
        def install_and_buy_vast(history_id, compute_vast_id, type, disk_size, user):
            user_id = user.id
            user_uuid = user.uuid

            if type == 'model-training':
                # status_install, response = vast_service.func_install_compute_vastai(compute_vast_id, "aixblock/template_ml", 'ml', user_id)
                status_install, response, errors = vast_provider.func_install_compute_vastai(compute_vast_id, "aixblock/template_ml", 'ml', user_id, disk_size=disk_size)
                port_tem = 9090

            elif type =="storage":
                # status_install, response = vast_service.func_install_compute_vastai(compute_vast_id, "quay.io/minio/minio:latest", 'storage', user_id)
                status_install, response, errors = (
                    vast_provider.func_install_compute_vastai(
                        compute_vast_id,
                        "quay.io/minio/minio:latest",
                        "storage",
                        user_id,
                        disk_size=disk_size
                    )
                )
                port_tem = 9001

            else:
                image_detail = InstallationService.objects.filter(
                environment=ENVIRONMENT, image=AIXBLOCK_IMAGE_NAME, deleted_at__isnull=True
                ).first()
                image_platform = AIXBLOCK_IMAGE_NAME + ":latest"
                if image_detail is not None: 
                    image_platform = str(image_detail.image) + ":" + str(image_detail.version)
                latest_history = History_Rent_Computes.objects.filter(
                    compute_marketplace=OuterRef('pk'),
                    service_type=History_Rent_Computes.SERVICE_TYPE.STORAGE
                ).order_by('-time_end').values('time_end')[:1]

                compute_minio = ComputeMarketplace.objects.filter(author_id =user_id, deleted_at__isnull = True,history_rent_computes__time_end__in=Subquery(latest_history) ).first()

                status_install, response, errors = vast_provider.func_install_compute_vastai(
                    compute_vast_id,
                    image_platform,
                    "full",
                    user_id,
                    compute=compute_minio,
                    disk_size=disk_size
                )
                port_tem = 8081

            if not status_install:
                # refund money
                install_logs = None
                if errors.get('error') == "insufficient_credit":
                    install_logs = f"Please contact webmaster. Key: {errors.get('error')}"
                else:
                    install_logs = f"{errors.get('msg')}"

                history = History_Rent_Computes.objects.filter(
                    id=history_id
                ).first()
                compute = ComputeMarketplace.objects.filter(infrastructure_id=response).first()

                history.compute_install="failed"
                history.install_logs=install_logs
                history.save()

                history_vast = History_Rent_Computes.objects.filter(
                    id=history_id
                ).first()
                if history:
                    update_notify_install(
                        install_logs,
                        user_id,
                        install_logs,
                        history.id,
                        "Failed to install compute.",
                        "danger",
                    )

                publish_message(
                    channel=f'{compute_vast_id}', data={"refresh": True}, prefix=True
                )

                notify_for_compute(user_uuid, "Danger", "Fail install compute, please contact webmaster.")

                # send_mail_refund(user, compute)

                return Response(
                    {"detail": f"Not available, please try again"}, status=400
                )

            ComputeMarketplace.objects.filter(
                infrastructure_id=response["instances"]["old_id"],
                deleted_at__isnull=True,
            ).update(
                name=response["instances"]["public_ipaddr"],
                status="rented_bought",
                infrastructure_id=response["instances"]["id"],
                owner_id= 0,  #response["instances"]["host_id"],
                author_id=user_id,
                organization_id=user.active_organization_id,
                ip_address=response["instances"]["public_ipaddr"],
                port=response["instances"]["ports"][f"{port_tem}/tcp"][0][
                    "HostPort"
                ],
                config=json.dumps(
                    {
                        "cpu": response["instances"]["cpu_name"],
                        "ram": response["instances"]["cpu_ram"],
                        "disk": response["instances"]["disk_space"],
                        "diskType": "SSD",
                        "os": "Linux",
                    }
                ),
                # ip_address=response["instances"]["public_ipaddr"],
                # port=port_tem,
                type="MODEL-PROVIDER-VAST",
                client_id="",
                client_secret="",
                ssh_key="",
                price=0,
                # compute_type="full",
                is_using_cpu=False,
            )

            compute = ComputeMarketplace.objects.filter(
                infrastructure_id=response["instances"]["id"], deleted_at__isnull=True
            ).first()

            effect_ram = 1
            if response["instances"]["cpu_cores"] and response["instances"]["cpu_cores_effective"]:
                effect_ram = response["instances"]["cpu_cores"]/response["instances"]["cpu_cores_effective"]

            ComputeGPU.objects.filter(compute_marketplace=compute).update(
                # compute_marketplace=compute,
                infrastructure_id=compute,
                gpu_id="0",
                gpu_name=response["instances"]["gpu_name"],
                memory_usage=response["instances"]["mem_usage"],
                gpu_memory=convert_gb_to_byte(int(response["instances"]["gpu_totalram"]/1000)),
                gpu_tflops=response["instances"]["total_flops"],
                internet_up_speed=response["instances"]["inet_down"],
                internet_down_speed=response["instances"]["inet_up"],
                max_cuda_version=response["instances"]["cuda_max_good"],
                gpu_memory_bandwidth=round(response["instances"]["gpu_mem_bw"],2),
                motherboard=response["instances"]["mobo_name"],
                number_of_pcie_per_gpu=f'{response["instances"]["pci_gen"]}.0,16x',
                per_gpu_pcie_bandwidth=response["instances"]["pcie_bw"],  # convert to GB
                eff_out_of_total_nu_of_cpu_virtual_cores=f'{round(response["instances"]["cpu_cores_effective"], 1)}/{response["instances"]["cpu_cores"]}',
                eff_out_of_total_system_ram=f'{int(round(response["instances"]["cpu_ram"]/1000, 0))}/{int(round(response["instances"]["cpu_ram"]/1000, 0)*effect_ram)}',
                reliability=round((response["instances"]["reliability2"]*100),2),  # %
                dl_performance_score=round(response["instances"]["dlperf_per_dphtotal"], 2),  # %
                dlp_score=round(response["instances"]["dlperf"], 2),  # DLP/$/hr,
                location_alpha2=response["instances"]["geolocation"],
                # location_id=response["instances"]["geolocode"],
                location_name=response["instances"]["geolocation"],
                datacenter="datacenter" if response["instances"]["hosting_type"] == 1 else None,
                status="renting",
            )

            ComputeGpuPrice.objects.filter(compute_marketplace_id=compute).update(price = round(response["instances"]["dph_total"], 3))

            # time_start = datetime.utcnow()
            # time_end = time_start + timedelta(hours=compute_vast_hours)
            # time_end = time_start + timedelta(hours=1)

            history_instance = History_Rent_Computes.objects.filter(id=history_id).update(
                                                compute_install="completed",
                                                # time_end=time_end,
                                                # rental_hours=compute_vast_hours,
                                                ip_address=response['instances']['public_ipaddr'],
                                                port=response['instances']['ports'][f'{port_tem}/tcp'][0]["HostPort"],
                                                )

            history_vast = History_Rent_Computes.objects.filter(id=history_id).first()
            update_notify_install("Compute installation completed.", user_id, "Compute installation completed.", history_vast.id, "Install Compute", "success")

            publish_message(
                    channel=compute_vast_id, data={"refresh": True}, prefix=True
                )

            notify_for_compute(user_uuid, "Success", "Compute installation completed.")

            def update_minio_info(compute, email_user, pass_user, minio_api_port):
                compute_marketplace = ComputeMarketplace.objects.filter(id = compute.id).first()
                compute_marketplace.set_password(pass_user)
                compute_marketplace.api_port = minio_api_port
                compute_marketplace.username = email_user
                compute_marketplace.save()
            if type == "storage":
                email_user = response["instances"]["extra_env"][2][1]
                pass_user = response["instances"]["extra_env"][3][1]
                minio_api_port = response["instances"]["ports"][f"9000/tcp"][0][
                        "HostPort"
                    ]
                update_minio_info(compute, email_user, pass_user, minio_api_port)
                send_mail_s3(user, compute, email_user, pass_user)
                
            elif type == 'model-training':
                model_endpoint = response["instances"]["ports"][f"9090/tcp"][0][
                        "HostPort"
                    ]

                tensorboard_endpoint = response["instances"]["ports"][f"6006/tcp"][0][
                        "HostPort"
                    ]

                ddp_endpoint = response["instances"]["ports"][f"23456/tcp"][0][
                        "HostPort"
                    ]

                send_mail_rent_compute(user, compute, model_endpoint, tensorboard_endpoint, ddp_endpoint)

            else:
                email_user = response["instances"]["extra_env"][4][1]
                pass_user = response["instances"]["extra_env"][6][1]
                send_mail_rent_compute_platform(user, compute, email_user, pass_user)
        
        def install_and_buy_exabit(history_id, compute_exabit_id, type, user):
                user_id = user.id
                user_uuid = user.uuid
                user_name = user.username
                user_email = user.email

                if type == 'model-training':
                    status_install, response, errors = exabit_provider.install_compute(compute_exabit_id, "aixblock/template_ml", 'ml', platform_username=user_name, platform_password=None, platform_email=user_email)
                    port_tem = 9090

                elif type =="storage":
                    # status_install, response = vast_service.func_install_compute_vastai(compute_exabit_id, "quay.io/minio/minio:latest", 'storage', user_id)
                    status_install, response, errors = (
                        exabit_provider.install_compute(
                            compute_exabit_id,
                            "quay.io/minio/minio:latest",
                            "storage",
                            platform_username=user_name, platform_password=None, platform_email=user_email
                        )
                    )
                    port_tem = 9001

                else:
                    image_detail = InstallationService.objects.filter(
                    environment=ENVIRONMENT, image=AIXBLOCK_IMAGE_NAME, deleted_at__isnull=True
                    ).first()
                    image_platform = AIXBLOCK_IMAGE_NAME + ":latest"
                    if image_detail is not None: 
                        image_platform = str(image_detail.image) + ":" + str(image_detail.version)
                    latest_history = History_Rent_Computes.objects.filter(
                        compute_marketplace=OuterRef('pk'),
                        service_type=History_Rent_Computes.SERVICE_TYPE.STORAGE
                    ).order_by('-time_end').values('time_end')[:1]

                    compute_minio = ComputeMarketplace.objects.filter(author_id =user_id, deleted_at__isnull = True,history_rent_computes__time_end__in=Subquery(latest_history) ).first()

                    status_install, response, errors = exabit_provider.install_compute(
                        compute_exabit_id,
                        image_platform,
                        "full",
                        platform_username=user_name, platform_password=None, platform_email=user_email, client_id=compute_minio.client_id, client_secret=compute_minio.client_secret
                    )
                    port_tem = 8081

                if not status_install:
                    install_logs = None
                    history = History_Rent_Computes.objects.filter(
                        id=history_id
                    ).first()
                    compute = ComputeMarketplace.objects.filter(infrastructure_id=response).first()
                    compute_gpu = ComputeGPU.objects.filter(id=history.compute_gpu_id).first()
                    compute.infrastructure_id=f"{response}-{uuid.uuid4()}"

                    history.compute_install="failed"

                    if errors == "You have insufficient balance":
                        install_logs = f"Please contact webmaster. Key: {errors}"

                        compute.deleted_at = timezone.now()
                        compute_gpu.infrastructure_id = compute
                        compute_gpu.deleted_at = timezone.now()
                        history.deleted_at = timezone.now()
                    else:
                        install_logs = f"{errors}"

                    history.install_logs=install_logs
                    history.save()
                    compute.save()
                    compute_gpu.save()

                    # history_exabit = History_Rent_Computes.objects.filter(
                    #     compute_marketplace__infrastructure_id=response,
                    #     compute_marketplace__deleted_at__isnull=True,
                    #     deleted_at__isnull=True,
                    #     deleted_by__isnull=True,
                    # ).first()
                    if history:
                        update_notify_install(
                            install_logs,
                            user_id,
                            install_logs,
                            history.id,
                            "Failed to install compute.",
                            "danger",
                        )

                    publish_message(
                        channel=compute_exabit_id, data={"refresh": True}, prefix=True
                    )

                    notify_for_compute(user_uuid, "Danger", f'{install_logs}')

                    send_mail_refund(user, compute)

                    return Response(
                        {"detail": f"Not available, please try again"}, status=400
                    )

                ComputeMarketplace.objects.filter(
                    infrastructure_id=response["data"]["old_id"],
                    deleted_at__isnull=True,
                ).update(
                    name=response["data"]["public_ip"],
                    status="rented_bought",
                    infrastructure_id=response["data"]["id"],
                    owner_id= 0,  #response["instances"]["host_id"],
                    author_id=user_id,
                    organization_id=user.active_organization_id,
                    ip_address=response["data"]["public_ip"],
                    # port=response["data"]["ports"]["9001"] if ,
                    # api_port=response["data"]["ports"]["9000"],
                    config=json.dumps(
                        {
                            "cpu": response["data"]["flavor"]["name"],
                            "ram": response["data"]["flavor"]["ram"],
                            "disk": response["data"]["flavor"]["disk"],
                            "diskType": "SSD",
                            "os": "Linux",
                        }
                    ),
                    # ip_address=response["instances"]["public_ipaddr"],
                    # port=port_tem,
                    type=ComputeMarketplace.Type.PROVIDEREXABIT,
                    client_id="",
                    client_secret="",
                    ssh_key="",
                    price=0,
                    # compute_type="full",
                    is_using_cpu=False,
                )

                compute = ComputeMarketplace.objects.filter(
                    infrastructure_id=response["data"]["id"], deleted_at__isnull=True
                ).first()

                effect_ram = 1
                # if response["data"]["flavor"]["cpu_cores"] and response["instances"]["cpu_cores_effective"]:
                #     effect_ram = response["instances"]["cpu_cores"]/response["instances"]["cpu_cores_effective"]

                if "info_compute" in response["data"] and response["data"]["info_compute"]:
                    effect_ram = response["data"]["info_compute"]["used_cores"]/response["data"]["info_compute"]["cpu_cores"]

                    ComputeGPU.objects.filter(compute_marketplace=compute).update(
                        # compute_marketplace=compute,
                        infrastructure_id=compute,
                        gpu_id="0",
                        gpu_name=response["data"]["flavor"]["gpu"],
                        # memory_usage=response["instances"]["mem_usage"],
                        gpu_memory=convert_gb_to_byte(int(response["data"]["info_compute"]["total_mem_mb"]/1000)),
                        gpu_tflops=response["data"]["info_compute"]["tflops"],
                        # internet_up_speed=response["instances"]["inet_down"],
                        # internet_down_speed=response["instances"]["inet_up"],
                        max_cuda_version=response["data"]["info_compute"]["cuda_version"],
                        gpu_memory_bandwidth=round(response["data"]["info_compute"]["mem_bandwidth_gb_per_s"],2),
                        # motherboard=response["instances"]["mobo_name"],
                        number_of_pcie_per_gpu=f'{response["data"]["info_compute"]["pcie_link_gen_max"]}.0,16x',
                        per_gpu_pcie_bandwidth=response["data"]["info_compute"]["pcie_link_width_max"],  # convert to GB
                        eff_out_of_total_nu_of_cpu_virtual_cores=f'{round(response["data"]["info_compute"]["used_cores"], 1)}/{response["data"]["info_compute"]["cpu_cores"]}',
                        eff_out_of_total_system_ram=f'{int(round(response["data"]["info_compute"]["ram_info"]["used_ram_mb"]/1000, 0))}/{int(round(response["data"]["info_compute"]["ram_info"]["total_ram_mb"]/1000, 0)*effect_ram)}',
                        # reliability=round((response["instances"]["reliability2"]*100),2),  # %
                        # dl_performance_score=round(response["instances"]["dlperf_per_dphtotal"], 2),  # %
                        # dlp_score=round(response["instances"]["dlperf"], 2),  # DLP/$/hr,
                        # location_alpha2=response["instances"]["geolocation"],
                        # # location_id=response["instances"]["geolocode"],
                        location_name=response["data"]["region"]["name"],
                        datacenter="datacenter",
                        status="renting",
                    )
                else:
                    ComputeGPU.objects.filter(compute_marketplace=compute).update(
                        # compute_marketplace=compute,
                        infrastructure_id=compute,
                        gpu_id="0",
                        gpu_name=response["data"]["flavor"]["gpu"],
                        # memory_usage=response["instances"]["mem_usage"],
                        # gpu_memory=convert_gb_to_byte(int(response["instances"]["gpu_totalram"]/1000)),
                        # gpu_tflops=response["instances"]["total_flops"],
                        # internet_up_speed=response["instances"]["inet_down"],
                        # internet_down_speed=response["instances"]["inet_up"],
                        max_cuda_version="12.2",
                        # gpu_memory_bandwidth=round(response["instances"]["gpu_mem_bw"],2),
                        # motherboard=response["instances"]["mobo_name"],
                        # number_of_pcie_per_gpu=f'{response["instances"]["pci_gen"]}.0,16x',
                        # per_gpu_pcie_bandwidth=response["instances"]["pcie_bw"],  # convert to GB
                        # eff_out_of_total_nu_of_cpu_virtual_cores=f'{round(response["instances"]["cpu_cores_effective"], 1)}/{response["instances"]["cpu_cores"]}',
                        # eff_out_of_total_system_ram=f'{int(round(response["instances"]["cpu_ram"]/1000, 0))}/{int(round(response["instances"]["cpu_ram"]/1000, 0)*effect_ram)}',
                        # reliability=round((response["instances"]["reliability2"]*100),2),  # %
                        # dl_performance_score=round(response["instances"]["dlperf_per_dphtotal"], 2),  # %
                        # dlp_score=round(response["instances"]["dlperf"], 2),  # DLP/$/hr,
                        # location_alpha2=response["instances"]["geolocation"],
                        # # location_id=response["instances"]["geolocode"],
                        location_name=response["data"]["region"]["name"],
                        datacenter="datacenter",
                        status="renting",
                    )

                ComputeGpuPrice.objects.filter(compute_marketplace_id=compute).update(price = round(response["data"]["fee"]['price'], 3))

                # time_start = datetime.utcnow()
                # time_end = time_start + timedelta(hours=compute_exabit_hours)
                # time_end = time_start + timedelta(hours=1)

                history_instance = History_Rent_Computes.objects.filter(id=history_id).update(
                                                    compute_install="completed",
                                                    # time_end=time_end,
                                                    # rental_hours=compute_exabit_hours,
                                                    ip_address=response["data"]["public_ip"],
                                                    # port=response["data"]["ports"]["9090"],
                                                    )

                history_exabit = History_Rent_Computes.objects.filter(id=history_id).first()
                update_notify_install("Compute installation completed.", user_id, "Compute installation completed.", history_exabit.id, "Install Compute", "success")

                publish_message(
                        channel=compute_exabit_id, data={"refresh": True}, prefix=True
                    )

                notify_for_compute(user_uuid, "Success", "Compute installation completed.")

                def update_minio_info(compute, email_user, pass_user, minio_api_port):
                    compute_marketplace = ComputeMarketplace.objects.filter(id = compute.id).first()
                    compute_marketplace.set_password(pass_user)
                    compute_marketplace.api_port = minio_api_port
                    compute_marketplace.username = email_user
                    compute_marketplace.save()

                if type == "storage":
                    email_user =response["data"]["info"]["user_email"]
                    pass_user =response["data"]["info"]["user_password"]
                    # minio_api_port = response["data"]["ports"]["9000"]

                    compute.port = response["data"]["ports"]["9001"]
                    compute.api_port = response["data"]["ports"]["9000"]
                    compute.set_password(pass_user)
                    compute.username = email_user
                    history_exabit.port = response["data"]["ports"]["9000"]
                    compute.save()
                    history_exabit.save()
                        
                    # update_minio_info(compute, email_user, pass_user, minio_api_port)
                    send_mail_s3(user, compute, email_user, pass_user)

                elif type == 'model-training':
                    model_endpoint = response["data"]["ports"]["9090"]

                    tensorboard_endpoint = response["data"]["ports"]["6006"]

                    ddp_endpoint = response["data"]["ports"]["23456"]
                    compute.port = model_endpoint
                    history_exabit.port = response["data"]["ports"]["9090"]
                    history_exabit.save()
                    compute.save()

                    send_mail_rent_compute(user, compute, model_endpoint, tensorboard_endpoint, ddp_endpoint)

                else:
                    email_user = response["data"]["info"]["user_email"]
                    pass_user = response["data"]["info"]["user_password"]

                    compute.port = response["data"]["ports"]["8081"]
                    compute.api_port = response["data"]["ports"]["9000"]
                    compute.set_password(pass_user)
                    compute.username = email_user
                    history_exabit.port = response["data"]["ports"]["8081"]
                    history_exabit.save()
                    compute.save()

                    send_mail_s3(user, compute, email_user, pass_user, response["data"]["ports"]["9001"])
                    send_mail_rent_compute_platform(user, compute, email_user, pass_user)
                    # update_minio_info(compute, email_user, pass_user)

        def install_and_buy_gpu(history_id, gpu_id, type, user):
            user_id = user.id
            user_uuid = user.uuid
            user_name = user.username
            user_email = user.email

            compute_gpu_price = ComputeGpuPrice.objects.filter(compute_gpu_id=gpu_id).first() 
            compute_gpu = ComputeGPU.objects.filter(
                    id=gpu_id, deleted_at__isnull=True
                ).first()
            
            compute = ComputeMarketplace.objects.filter(
                    Q(id=compute_gpu.compute_marketplace_id), deleted_at__isnull=True
                ).first()
            
            compute_gpu_rented = History_Rent_Computes.objects.filter(
                id=history_id
            ).first()


            # check docker running on server ip address
            # if not running - remove compute in marketplace
            try:
                status = checkDockerKubernetesStatus(
                    ip_address=compute.ip_address, port=compute.docker_port
                )
                if not status:
                    raise Exception("Service check failed")
            except Exception as e:
                # change status = suspend - require owner of compute
                compute.status = "suspend"
                compute.save()
                return Response(
                    {"detail": f"Docker does not run on {compute.ip_address}"}, status=400
                )

            # create order, minus money from portfolio wallet, create History rent

            access_token = get_env("MASTER_TOKEN", "")
            if access_token != "":
                endpoint = get_env("MASTER_NODE", "https://app.aixblock.io")
                headers = {f"Authorization": "Token {access_token}"}
                response = requests.patch(
                    f"{endpoint}/api/model_marketplace/rent/", headers=headers
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    return Response(
                        {
                            "error": "Failed to rent compute in the marketplace",
                        },
                        status=response.status_code,
                    )

            token = Token.objects.get(user=user)

            # install docker
            compute_install = "completed"
            minio_user_email = None
            try:
                _port, minio_port, user_email, password , minio_user_username, minio_password, network_name, minio_api_port = dockerContainerPull(
                    compute.compute_type,
                    compute.ip_address,
                    compute.client_id,
                    compute.client_secret,
                    token,
                    user_id=user_id,
                    gpu_id=gpu_id,
                    gpu_index=compute_gpu.gpu_index,
                    history_id=history.id
                )
                minio_user_email = minio_user_username
                compute.port = f"{_port}"
                compute.save()
                history.port = _port
                history.compute_install = compute_install
                history.save()
            except Exception as e:
                compute_install = "failed"
                history.compute_install = compute_install
                history.save()

            check_compute_run_status(history.id)

            compute_gpu_id = gpu_id

            compute_gpu = ComputeGPU.objects.filter(id=compute_gpu_id).first()
            if compute_gpu:
                if ComputeMarketplace.objects.filter(
                    id=compute_gpu.compute_marketplace_id, owner_id=user_id
                ).exists():
                    return Response(
                        {"detail": "You cannot rent your own compute"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                # compute_gpu.status = "renting"
                compute_gpu.owner_id = compute.owner_id
                compute_gpu.save()
                # update status install compute
                history.compute_install = compute_install
                history.save()

            else:
                return Response({"detail": "Compute GPU not found"}, status=404)
            compute_gpu_in_marketplace = ComputeGPU.objects.filter(
                status="in_marketplace", compute_marketplace_id=compute.id
            ).first()
            #  change status compute marketplace to 'rented_bought' if all compute has been rented
            if compute_gpu_in_marketplace is None:
                compute.status = "rented_bought"
                compute.save()

            if compute.type == "MODEL-SYSTEM":
                create = ComputeMarketplace.objects.create(
                    name=compute.name,
                    infrastructure_id=compute.infrastructure_id,
                    owner_id=compute.owner_id,
                    author_id=compute.author_id,
                    catalog_id=compute.catalog_id,
                    organization_id=compute.organization_id,
                    order=compute.order,
                    config=compute.config,
                    infrastructure_desc=compute.infrastructure_desc,
                    ip_address=compute.ip_address,
                    port=compute.port,
                    docker_port=compute.docker_port,
                    kubernetes_port=compute.kubernetes_port,
                    is_scale=True
                )
                return Response(
                    {"id": create.id, "name": create.name, "author_id": create.author_id},
                    status=201,
                )
            
            try:
                user_email = user.email
                if type == "storage":
                    # send_mail_s3_full(user, compute)
                    send_mail_s3(user, compute, minio_user_email, minio_password)
                elif type == 'model-training':
                    send_mail_rent_compute(user, compute, minio_port, user_email)
                else:
                    # send_mail_rent_compute_full_platform(user, compute, user_email, password, minio_user_email=minio_user_email, minio_password=minio_password )
                    send_mail_rent_compute_platform(user, compute, user_email, password)
                    if minio_user_email:
                        send_mail_s3(user, compute, minio_user_email, minio_password)
            except Exception as e:
                pass

            try:
                update_notify_install("Compute installation completed.", user_id, "Compute installation completed.", history.id, "Install Compute", "success")
                notify_for_compute(user_uuid, "Success", "Compute installation completed.")
            except Exception as e:
                pass
        
        for history in history_instance:
            history.compute_install = History_Rent_Computes.InstallStatus.INSTALLING
            history.save()
            publish_message(
                channel=f'{history.compute_marketplace.infrastructure_id}', data={"refresh": True}, prefix=True
            )

            user = history.account

            if history.compute_marketplace.type == ComputeMarketplace.Type.PROVIDERVAST:
                thread = threading.Thread(target=install_and_buy_vast,  args=(history.id, history.compute_marketplace.infrastructure_id, history.service_type, history.compute_gpu.disk, user))
                thread.start()
            elif history.compute_marketplace.type == ComputeMarketplace.Type.PROVIDEREXABIT:
                thread = threading.Thread(target=install_and_buy_exabit,  args=(history.id, history.compute_marketplace.infrastructure_id, history.service_type, user))
                thread.start()
            else:
                thread = threading.Thread(target=install_and_buy_gpu,  args=(history.id, history.compute_gpu_id, history.service_type, user))
                thread.start()

        return Response(status=200)
        