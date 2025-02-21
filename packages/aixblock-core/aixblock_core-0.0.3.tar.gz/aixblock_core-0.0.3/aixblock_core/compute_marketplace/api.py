import logging
import subprocess
import requests
import regex
import json
import threading
import time
import string
from django.core.serializers import serialize
from aixblock_core.core.utils.params import get_env
from .gpu_util import GpuUtil
from django.db.models import Max
from .models import (
    ComputeMarketplace,
    CatalogComputeMarketplace,
    ComputeGPU,
    ComputeTimeWorking,
    ComputeGpuPrice,
    Trade,
    History_Rent_Computes,
    Portfolio,
    Computes_Preference,
)
from ml.models import MLBackend, MLGPU, MLBackendStatus, MLNetwork, MLNetworkHistory
from model_marketplace.models import ModelMarketplace, History_Rent_Model
from projects.models import Project
from orders.models import Order, OrderComputeGPU
from .serializers import (
    ComputeMarketplaceSerializer,
    ComputeMarketplaceUserCreateSerializer,
    CatalogComputeMarketplaceSerializer,
    ComputeMarketUserCreateFullSerializer,
    ComputeMarketFilter,
    ComputeMarketplaceDetailSerializer,
    ComputeTimeWorkingSerializer,
    HistoryRentComputeSerializer,
    ComputeMarketplaceRentSerializer,
    TradeResourceSerializer,
    ComputeMarketplaceRentedSerializer,
    ComputesPreferenceSerializer,
    AutoMergeCardSerializer,
    ComputeRentSerializer,
    ComputeMarketplaceRentedCardSerializer,
    ComputeMarketplaceRentV2Serializer,
    ComputeGpuRelateSerializer,
)
from django.utils import timezone
from core.permissions import ViewClassPermission, all_permissions
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError as RestValidationError
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi as openapi
from oauth2_provider.models import get_application_model
from core.utils.paginate import SetPagination
from projects.services.project_nginx_proxy import NginxReverseProxyManager
import random
import docker
import os
import uuid
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from core.utils.docker_container_pull import dockerContainerPull
from rest_framework.authtoken.models import Token
from core.filters import filterModel
from core.swagger_parameters import (
    page_parameter,
    search_parameter,
    field_search_parameter,
    sort_parameter,
    type_parameter,
    field_query_parameter,
    query_value_parameter
)

from django.conf import settings
from core.utils.docker_kubernetes_info import checkDockerKubernetesStatus
from core.utils.docker_container_create import createDocker
from django.db.models import (
    Q,
    Count,
    Prefetch,
    Exists,
    Subquery,
    OuterRef,
    F,
    JSONField,
    Value,
    Func,
    CharField,
    ExpressionWrapper,
    Case, When, IntegerField
)
from django.db.models.functions import Concat
from django.db import transaction
from aixblock_core.users.service_notify import get_data, send_email_thread
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.pagination import PageNumberPagination

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from collections import defaultdict
from django.db import models
from aixblock_core.core.utils.nginx_server import NginxReverseProxy

from datetime import datetime, timedelta
from dateutil import parser
from django.utils import timezone
from users.models import User
from django.db.models import FloatField
from django.db.models.functions import Cast
from rest_framework import filters
from core.settings.base import SERVICE_FEE, AIXBLOCK_IMAGE_NAME, ENVIRONMENT, MAIL_SERVER, EXABBIT_SHOW
from configs.models import InstallationService
import re
from core.utils.docker_container_action import dockerContainerStartStop
from django.db import OperationalError
from django.http import FileResponse, Http404
from .functions import  run_event_loop_in_thread, notify_for_compute
import asyncio
from plugins.plugin_centrifuge import publish_message

# from calflops import calculate_flops
# from torchvision import models
# import torch
from projects.calc_flops_mem import (
    calc_time_neeed_nlp,
    calc_mem_pytorch_images,
    calc_time_neeed_pytorch_images,
    calc_mem_tf,
    calc_mem_gpu_tf,
    calc_only_time_need,
    calc_param_from_tflop,
    calc_tflop_from_param
)
from model_marketplace.calc_transformer_mem import (
    config_parser as config_cacl_mem,
    calc_mem,
)
from model_marketplace.calc_transformer_flops import config_parser, calc_params
from aixblock_core.model_marketplace.calc_transformer_flops import (
    convert_flops_float,
)
# from .vastai_func import vast_api_offer, vast_api_offer_old, func_install_compute_vastai, delete_instance_info, get_instance_info
from .vastai_func import vast_service
from .plugin_provider import vast_provider, exabit_provider
# from .schedule_func import start_threaded_cron_jobs

from compute_marketplace.self_host import (
    _check_compute_verify,
    _update_server_info,
    _update_compute_gpus,
    _handle_install_compute,
    _handle_service_type,
    _handle_cuda,
    update_notify_install
)

from plugins.plugin_centrifuge import (
    generate_centrifuge_jwt,
    connect_to_server,
    subscribe_to_channel,
    publish_message,
    run_centrifuge,
)

from core.utils.convert_memory_to_byte import convert_mb_to_byte,convert_mb_to_gb,convert_gb_to_byte , convert_byte_to_gb, convert_byte_to_mb
from users.models import Organization
IN_DOCKER = bool(os.environ.get("IN_DOCKER", True))
DOCKER_API = "tcp://108.181.196.144:4243" if IN_DOCKER else "unix://var/run/docker.sock"
IMAGE_TO_SERVICE = {
    "huggingface_image_classification": "computer_vision/image_classification",
    "huggingface_text_classification": "nlp/text_classification",
    "huggingface_text2text": "nlp/text2text",
    "huggingface_text_summarization": "nlp/text_summarization",
    "huggingface_question_answering": "nlp/question_answering",
    "huggingface_token_classification": "nlp/token_classification",
    "huggingface_translation": "nlp/translation",
}
NUM_GPUS = int(os.environ.get("NUM_GPUS", 1))


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get Compute Marketplaces",
        operation_description="Get List Compute Marketplaces",
        manual_parameters=[
            page_parameter,
            search_parameter,
            field_search_parameter,
            sort_parameter,
            type_parameter,
            openapi.Parameter(
                "min_price",
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Minimum price",
            ),
            openapi.Parameter(
                "max_price",
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Maximum price",
            ),
            openapi.Parameter(
                "startDate",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="startDate",
            ),
            openapi.Parameter(
                "endDate",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="endDate",
            ),
        ],
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Post actions",
        operation_description="Perform an action with the selected items from a specific view.",
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Post actions",
        operation_description="Perform an action with the selected items from a specific view.",
    ),
)
class ComputeMarketplaceAPI(generics.ListCreateAPIView):
    serializer_class = ComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
        POST=all_permissions.annotations_view,
    )
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComputeMarketFilter

    def get_queryset(self):
        user_id = self.request.user.id
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        compute_gpu_id = ComputeGpuPrice.objects.values("compute_gpu_id")

        if min_price is not None:
            compute_gpu_id = compute_gpu_id.filter(price__gte=min_price)

        if max_price is not None:
            compute_gpu_id = compute_gpu_id.filter(price__lte=max_price)

        # Get all ComputeMarketplaces that are not deleted
        queryset = (
            ComputeMarketplace.objects.filter(
                Q(deleted_at__isnull=True) | Q(gpu_prices__type="cpu")
            )
            .annotate(
                has_compute_gpus=Exists(
                    ComputeGPU.objects.filter(
                        deleted_at__isnull=True,
                        status="in_marketplace",
                        id__in=ComputeGpuPrice.objects.filter(
                            compute_gpu_id=OuterRef("id"),
                        ).values("compute_gpu_id"),
                    )
                ),
                has_compute_cpu_price=Exists(
                    ComputeGpuPrice.objects.filter(
                        compute_marketplace_id=OuterRef("id"), type="cpu"
                    )
                ),
            )
            .filter(
                Q(has_compute_gpus=True)
                | (Q(is_using_cpu=True) & Q(has_compute_cpu_price=True))
            )
            .prefetch_related(
                Prefetch(
                    "compute_gpus",
                    queryset=ComputeGPU.objects.filter(id__in=compute_gpu_id)
                    .exclude(status="renting")
                    .prefetch_related("prices"),
                ),
            )
            .distinct()
        )

        queryset = queryset.filter(status="in_marketplace")

        queryset = filterModel(self, queryset, ComputeMarketplace)

        compute_type = self.request.query_params.get("type")

        if compute_type is not None:
            queryset = queryset.filter(compute_type=compute_type)
        # if min_price is not None:
        #     queryset = queryset.filter(price__gte=min_price)
        # if max_price is not None:
        #     queryset = queryset.filter(price__lte=max_price)

        compute_id_time = []
        startDate = self.request.query_params.get("startDate")
        endDate = self.request.query_params.get("endDate")
        if startDate is not None and endDate is not None:
            startDate_obj = datetime.strptime(startDate, "%Y-%m-%d").date()
            endDate_obj = datetime.strptime(endDate, "%Y-%m-%d").date()

            compute_time_working_objects = ComputeTimeWorking.objects.all()
            for compute_time_working_object in compute_time_working_objects:
                date_ranges = compute_time_working_object.day_range
                if date_ranges is not None:
                    for date_range in date_ranges:
                        start_day = datetime.strptime(
                            date_range["start_day"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).date()
                        end_day = datetime.strptime(
                            date_range["end_day"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).date()
                        if start_day <= startDate_obj <= end_day:
                            compute_id_time.append(
                                compute_time_working_object.compute_id
                            )

            queryset = queryset.filter(pk__in=compute_id_time)
        else:
            current_time = timezone.now().date()
            compute_time_working_objects = ComputeTimeWorking.objects.all()
            for compute_time_working_object in compute_time_working_objects:
                date_ranges = compute_time_working_object.day_range
                if date_ranges is not None:
                    for date_range in date_ranges:
                        start_day = datetime.strptime(
                            date_range["start_day"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).date()
                        end_day = datetime.strptime(
                            date_range["end_day"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).date()
                        if start_day <= current_time <= end_day:
                            compute_id_time.append(
                                compute_time_working_object.compute_id
                            )

        queryset = queryset.exclude(author_id=user_id)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.request.query_params.get('page', 1)
        type = self.request.query_params.get('type', None)
        paginator = self.pagination_class()
        paginator.page_size = 12
        # Get serializer data
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data

        # Get vast data
        vast_data = vast_service.vast_api_offer_old()
        if type == "ml":
            vast_data = [record for record in vast_data if vast_data.get("compute_type") == "ml"]

        # Combine serializer data and vast data
        combined_data = serializer_data + vast_data

        # request.query_params['page_size'] = '12'
        # Paginate combined data
        paginated_data = paginator.paginate_queryset(combined_data, request)

        return paginator.get_paginated_response(paginated_data)

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        return super(ComputeMarketplaceAPI, self).post(request, *args, **kwargs)

    # @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(ComputeMarketplaceAPI, self).put(request, *args, **kwargs)


request_body_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "page": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Page number", default=1
        ),
        "search": openapi.Schema(
            type=openapi.TYPE_STRING, description="Search term", default=""
        ),
        "field": openapi.Schema(
            type=openapi.TYPE_STRING, description="Field to search", default=""
        ),
        "sort": openapi.Schema(type=openapi.TYPE_STRING, description="Sort by field"),
        "provider": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Provider of compute",
            enum=["nvidia", "amd", "intel", "mbs"],
        ),
        "location": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Id of country", example="704"
                ),
                "alpha2": openapi.Schema(
                    type=openapi.TYPE_STRING, description="alpha2 code", example="vn"
                ),
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="country name",
                    example="Viet Nam",
                ),
            },
            description="location, read data from: https://github.com/stefangabos/world_countries/blob/master/data/countries/en/countries.json",
        ),
        "service_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Type of compute",
            enum=[
                "all",
                "model-training",
                "platform",
                "notebook",
                "storage",
                "label-tool",
            ],
        ),
        "gpus_machine": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="gpus machine",
            enum=[
                "any",
                "1x",
                "2x",
                "4x",
                "8x",
            ],
        ),
        "vcpu_model_training": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="vCPUs per Model Training",
            example="2",
        ),
        "disk_type": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="disk type",
            enum=["ssd", "nvme"],
        ),
        "free_time": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum time, format: DD/MM/YYYY",
                    example="22/05/2024",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum time, format: DD/MM/YYYY",
                    example="22/05/2025",
                ),
            },
            description="free time",
        ),
        "reliability": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum %", example="0"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum %, max 100",
                    example="100",
                ),
            },
            description="reliability",
        ),
        "machine_options": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="Machine options",
            items=openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["secure-cloud", "virtual-machines", "physical-machines"],
            ),
            example=["secure-cloud", "virtual-machines"],
        ),
        "cuda_version": openapi.Schema(
            type=openapi.TYPE_STRING, description="Min cuda version", example="11.4"
        ),
        "driver_version": openapi.Schema(
            type=openapi.TYPE_STRING, description="Driver version", example="592.72.22"
        ),
        "ubuntu_version": openapi.Schema(
            type=openapi.TYPE_STRING, description="Ubuntu version", example="22.04"
        ),
        "price": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum price", example="0"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum price",
                    example="99999",
                ),
            },
            description="Price range",
        ),
        "gpu_count": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum price", example="0"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum price", example="8"
                ),
            },
            description="Gpu Count",
        ),
        "tflops": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum", example="0"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum", example="500"
                ),
            },
            description="Gpu Count",
        ),
        "per_gpu_ram": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="per_gpu_ram convert to GB",
        ),
        "gpu_total_ram": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="gpu_total_ram convert to GB",
        ),
        "gpu_ram_bandwidth": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="gpu_ram_bandwidth convert to GB",
        ),
        "pcie_bandwidth": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="pcie_bandwidth convert to GB",
        ),
        "nvlink_bandwidth": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="nvlink_bandwidth convert to GB",
        ),
        "cpu_cores": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum", example="512"
                ),
            },
            description="cpu cores",
        ),
        "cpu_ram": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Minimum: GB", example="1"
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Maximum: GB", example="1000"
                ),
            },
            description="cpu_ram convert to GB",
        ),
        "cpu_ghz": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum:convert to Mhz",
                    example="1",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum:convert to Mhz",
                    example="1000",
                ),
            },
            description="cpu_ghz convert to Mhz",
        ),
        "disk_bandwidth": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum:convert to MB",
                    example="1",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum:convert to MB",
                    example="1000",
                ),
            },
            description="disk_bandwidth convert to MB",
        ),
        "inet_up": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum:convert to Mbps",
                    example="1",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum:convert to Mbps",
                    example="8",
                ),
            },
            description="inet_up convert to Mbps",
        ),
        "inet_down": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum:convert to Mbps",
                    example="1",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum:convert to Mbps",
                    example="8",
                ),
            },
            description="inet_down convert to Mbps",
        ),
        "open_port": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "from": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Minimum",
                    example="1",
                ),
                "to": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Maximum",
                    example="8",
                ),
            },
            description="Open TCP/UDP Ports",
        ),
        "page_size": openapi.Schema(type=openapi.TYPE_INTEGER, description="Page size"),
    },
)

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Compute Marketplaces Rent",
        operation_description="Get List Compute Marketplaces Rent",
        manual_parameters=[
            openapi.Parameter(
                "page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "search", openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "field", openapi.IN_QUERY, description="Field to search", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "sort", openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "type", openapi.IN_QUERY, description="Type of compute", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "min_price", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Minimum price"
            ),
            openapi.Parameter(
                "max_price", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Maximum price"
            ),
            openapi.Parameter(
                "startDate", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Start date"
            ),
            openapi.Parameter(
                "endDate", openapi.IN_QUERY, type=openapi.TYPE_STRING, description="End date"
            ),
            openapi.Parameter(
                "page_size", openapi.IN_QUERY, type=openapi.TYPE_NUMBER, description="Page size"
            ),
        ],
    ),
)

@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Compute Marketplaces Rent",
        operation_description="Get List Compute Marketplaces Rent",
        request_body=request_body_schema,
    ),
)
class ComputeRentListAPIView(generics.ListCreateAPIView):
    serializer_class = ComputeRentSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
        POST=all_permissions.annotations_view,
    )
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = ComputeGPU.objects.filter(
            status="in_marketplace", user_rented__lt=models.F("max_user_rental"),
            deleted_at__isnull= True
        )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        paginator = self.pagination_class()
        result = []


        paginated_data = paginator.paginate_queryset(result, request)
        paginated_response = self.get_paginated_response(paginated_data)
        paginated_response.data["count"] = 0

        return paginated_response

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)

        paginator = self.pagination_class()
        result = []


        paginated_data = paginator.paginate_queryset(result, request)
        paginated_response = self.get_paginated_response(paginated_data)
        paginated_response.data["count"] = 0

        return paginated_response

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get details ",
        operation_description="Perform an action with the selected items from a specific view.",
    ),
)
class ComputeMarketplaceDetailAPIView(generics.RetrieveAPIView):
    queryset = ComputeMarketplace.objects.all()
    serializer_class = ComputeMarketplaceDetailSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Replace compute_gpus in serialized data with filtered data
        filtered_gpus = instance.get_filtered_compute_gpus()
        data['compute_gpus'] = ComputeGpuRelateSerializer(filtered_gpus, many=True).data

        return Response(data, status=status.HTTP_200_OK)


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Delete Compute Marketplace",
        operation_description="Delete Compute Marketplace.",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="Compute Marketplace ID",
            ),
        ],
    ),
)
class ComputeMarketplaceDeleteAPI(generics.DestroyAPIView):
    serializer_class = ComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        DELETE=all_permissions.annotations_delete,
    )

    def get_queryset(self):
        return ComputeMarketplace.objects.all()

    def delete(self, request, *args, **kwargs):
        instance_id = kwargs.get("pk")
        user = request.user
        try:
            instance = ComputeMarketplace.objects.get(
                Q(id=instance_id), deleted_at__isnull=True
            )
            compute_gpus = ComputeGPU.objects.filter(
                Q(compute_marketplace_id=instance.pk), deleted_at__isnull=True
            )

            # if owner delete - update deleted at
            if instance.owner_id == user.pk:
                instance.deleted_at = timezone.now()
                instance.status = "pending"
                compute_gpus.update(deleted_at=timezone.now(), status="pending")
                if instance.type == 'MODEL-PROVIDER-VAST':
                    # vast_service.delete_instance_info(instance.infrastructure_id)
                    vast_provider.delete_compute(instance.infrastructure_id)
                instance.save()
                
            # if renter (author) delete - return compute for owner
            else:
                instance.status = "in_marketplace"
                instance.author_id = instance.owner_id
                instance.save()
                history_rent_subquery = History_Rent_Computes.objects.filter(
                    compute_gpu_id=OuterRef('pk'),
                    status='renting',
                    account_id=user.id,
                    deleted_by__isnull = True,
                    deleted_at__isnull = True
                )
                compute_gpus = ComputeGPU.objects.filter(
                    compute_marketplace_id=instance_id,
                    status='renting',
                    history_rent_computes__in=history_rent_subquery
                ).distinct()
                if instance.is_using_cpu:
                    history_rent = History_Rent_Computes.objects.filter(
                        status="renting",
                        compute_gpu_id__isnull=True,
                        compute_marketplace_id=instance_id,
                        account_id=user.pk,
                        deleted_by__isnull = True,
                        deleted_at__isnull = True

                    ).first()
                    history_rent.status = "completed"
                    history_rent.save()

                if compute_gpus is not None:
                    for gpu_renting in compute_gpus:

                        gpu_renting.status = "in_marketplace"
                        gpu_renting.user_rented -= 1
                        gpu_renting.save()
                        Trade.objects.filter(
                            resource="compute_gpu",
                            resource_id=gpu_renting.id,
                            status="renting",
                        ).update(status="completed")
                        history_rent = History_Rent_Computes.objects.filter(
                            status="renting",
                            compute_gpu_id=gpu_renting.id,
                            account_id=user.pk,
                            deleted_at__isnull = True,
                            deleted_by__isnull = True


                        ).first()

                        history_rent.status = "completed"
                        history_rent.save()
                        
                if instance.type == 'MODEL-PROVIDER-VAST':
                    # vast_service.delete_instance_info(instance.infrastructure_id)
                    vast_provider.delete_compute(instance.infrastructure_id)
                instance.save()

                # delete ML process
                mlgpu_queryset = MLGPU.objects.filter(compute_id=instance.id)
                mlgpu_ids = mlgpu_queryset.values_list("ml_id", flat=True)
                mlgpu_queryset.update(deleted_at=timezone.now())
                MLBackend.objects.filter(id__in=mlgpu_ids).update(
                    deleted_at=timezone.now()
                )

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except ComputeMarketplace.DoesNotExist:
            return Response(
                {"detail": "Compute Marketplace not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update Compute Marketplace",
        operation_description="Update Compute Marketplace By Id.",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="Compute Marketplace ID",
            ),
        ],
        request_body=ComputeMarketplaceSerializer,
    ),
)
class ComputeMarketplaceUpdateAPI(generics.UpdateAPIView):
    serializer_class = ComputeMarketplaceSerializer
    queryset = ComputeMarketplace.objects.all()
    permission_required = ViewClassPermission(
        PATCH=all_permissions.projects_change,
    )
    redirect_kwarg = "pk"

    def patch(self, request, *args, **kwargs):
        compute = ComputeMarketplace.objects.filter(pk=kwargs["pk"]).first()
        if not compute:
            return Exception({"error": "Compute not found"}, status=400)

        return super(ComputeMarketplaceUpdateAPI, self).patch(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(ComputeMarketplaceUpdateAPI, self).put(request, *args, **kwargs)


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Rent Compute Marketplace",
        operation_description="Rent Compute Marketplace By Id.",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="Compute Marketplace ID",
            ),
        ],
    ),
)
class ComputeMarketplaceRentAPI(generics.UpdateAPIView):
    serializer_class = ComputeMarketplaceRentSerializer
    queryset = ComputeMarketplace.objects.all()
    permission_required = ViewClassPermission(
        PATCH=all_permissions.projects_change,
    )
    redirect_kwarg = "pk"

    def patch(self, request, *args, **kwargs):
        user_id = self.request.user.id
        compute_gpus_id = self.request.data.get("compute_gpus_id")
        compute_gpus_id_list = compute_gpus_id.split(",")
        hours = int(self.request.data.get("hours"))
        price = self.request.data.get("price")
        compute_id = self.request.data.get("compute_id") # list compute rent
        token_symbol = self.request.data.get("token_symbol")
        token_name = self.request.data.get("token_name")
        # check portfolio money of user
        portfolio = Portfolio.objects.filter(
            account_id=user_id, token_symbol=token_symbol
        ).first()
        if not portfolio:
            return Response({"detail": "Portfolio not found"}, status=404)

        if self.request.data.get('type') == "MODEL-PROVIDER":
            create_payment = 200
            if create_payment == 200:
                compute = ComputeMarketplace.objects.create(
                    name=self.request.data.get('name'),
                    catalog_id=self.request.data.get('catalog_id'),
                    order=self.request.data.get('order'),
                    status=self.request.data.get('status'),
                    infrastructure_id=self.request.data.get('infrastructure_id'),
                    owner_id=user_id,
                    author_id=user_id,
                    organization_id=self.request.data.get('organization_id'),
                    config=self.request.data.get('config'),
                    ip_address=self.request.data.get('ip_address'),
                    port=self.request.data.get('port'),
                    docker_port=self.request.data.get('docker_port'),
                    kubernetes_port=self.request.data.get('kubernetes_port'),
                    file=self.request.data.get('file'),
                    type=self.request.data.get('type'),
                    infrastructure_desc=self.request.data.get('infrastructure_desc'),
                    callback_url=self.request.data.get('callback_url'),
                    client_id=self.request.data.get('client_id'),
                    client_secret=self.request.data.get('client_secret'),
                    ssh_key=self.request.data.get('ssh_key'),
                    card=self.request.data.get('card'),
                    price=self.request.data.get('price'),
                    compute_type=self.request.data.get('compute_type'),
                    is_using_cpu=self.request.data.get('is_using_cpu')
                )
            else:
                return Response({"message": "Payment not completed"})
        else:
            compute = ComputeMarketplace.objects.filter(
                Q(pk=kwargs["pk"]), deleted_at__isnull=True
            ).first()
        if not compute:
            return Response({"error": "Compute not found"}, status=400)

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

        def calculate_time_end(compute_id, hours):
            # Get the current time as the start time
            time_start = datetime.utcnow()
            hours = int(hours)
            end_time = None
            min_start_day = None
            max_end_day = time_start
            remaining_hours = int(hours)
            time_working = ComputeTimeWorking.objects.filter(
                Q(compute_id=compute_id), deleted_at__isnull=True
            ).first()
            if time_working is not None:
                # Iterate through each day range
                for day_range in time_working.day_range:
                    start_day = datetime.fromisoformat(
                        day_range["start_day"].rstrip("Z")
                    )
                    end_day = datetime.fromisoformat(day_range["end_day"].rstrip("Z"))

                    # If the current time is within the work range
                    if start_day <= time_start <= end_day:
                        # Get the maximum end day among all records within the current time
                        if max_end_day <= end_day:
                            max_end_day = end_day

                    # If the current time is in the future
                    if time_start <= start_day:
                        if min_start_day is None:
                            min_start_day = start_day
                        if start_day <= min_start_day:
                            min_start_day = start_day

                    else:
                        # If the current time is in the past
                        pass

            # Calculate hours used from the current time
            hours_in_past = (max_end_day - time_start).total_seconds() / 3600
            remaining_hours -= hours_in_past

            if min_start_day is not None:
                # Calculate the end time
                end_time = min_start_day + timedelta(hours=remaining_hours)

            return end_time.isoformat() + "Z" if end_time else None

        time_end = calculate_time_end(compute.id, hours)

        # create order, minus money from portfolio wallet, create History rent
        # compute_gpus_id = ['id1', 'id2']
        def process_payment(price, portfolio, token_symbol, compute_gpus_id, user_id):
            # create order
            order_instance = Order.objects.create(
                total_amount=1,
                price=price,
                unit=token_symbol,
                status="completed",
                user_id=user_id,
            )
            # amount = (
            #     price * 0.9
            #     if (timezone.now() - order_instance.created_at) < timedelta(days=30)
            #     else price
            # )
            amount = price + price * SERVICE_FEE/100
            # Giảm số lượng tiền trong ví
            portfolio.amount_holding -= amount
            portfolio.save()

            # Cập nhật trạng thái của order
            order_instance.status = "renting"
            OrderComputeGPU.objects.create(
                        order_id=order_instance.id, compute_gpu_id=compute_gpus_id
                    )
            order_instance.save()
            order_id = order_instance.pk

            trade_data = {
                "token_name": token_name,
                "token_symbol": token_symbol,
                "amount": amount,
                "price": price,
                "type": "Market Fund",
                "status": "completed",
                "resource": "compute_marketplace",  # with cpu
                "resource_id": compute.id,  # with cpu - using compute Id
                "account_id": user_id,
                "order": order_instance.id,
            }
            Trade.objects.create(**trade_data)
            return {"amount": amount, "order_id": order_id}

        payment = process_payment(
            price, portfolio, token_symbol, compute_gpus_id_list, user_id
        )

        access_token = get_env("MASTER_TOKEN", "")
        if access_token != "":
            endpoint = get_env("MASTER_NODE", "https://app.aixblock.io")
            headers = {f"Authorization": "Token {access_token}"}
            response = requests.patch(
                f"{endpoint}/api/model_marketplace/rent/{kwargs['pk']}", headers=headers
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

        user = request.user
        token = Token.objects.get(user=user)
        instance = self.get_object()

        # install docker
        compute_install = "completed"
        try:

            _port, _, _, _, _, _, _, _ = dockerContainerPull(
                compute.compute_type,
                compute.ip_address,
                compute.client_id,
                compute.client_secret,
                token,
                user_id=user.id
            )
            instance.port = f"{_port}"
            instance.save()
        except Exception as e:
            compute_install = "failed"

        # process if compute using cpu
        if compute and compute.is_using_cpu:
            history_rent_computes = History_Rent_Computes.objects.filter(
                Q(compute_marketplace_id=compute.id),
                Q(status="renting"),
                deleted_at__isnull=True,
                compute_gpu_id__isnull=True,
                deleted_by__isnull = True
            ).first()
            if history_rent_computes:
                return Response({"detail": "Compute rented"}, status=400)
            # rented with cpu - update author_id and status rented_bought
            compute.author_id = user_id
            compute.status = "rented_bought"
            compute.save()
            History_Rent_Computes.objects.create(
                account_id=user_id,
                compute_marketplace_id=compute.id,
                status="renting",
                order_id=payment["order_id"],
                rental_hours=hours,
                time_end=time_end,
                compute_install=compute_install,
            )

        # process if rent gpu
        else:
            for compute_gpu_id in compute_gpus_id_list:
                history_rent_computes = History_Rent_Computes.objects.filter(
                    Q(compute_gpu_id=compute_gpu_id),
                    Q(status="renting"),
                    Q(account_id=user_id),
                    deleted_at__isnull=True,
                    deleted_by__isnull = True
                ).first()
                if history_rent_computes:
                    return Response({"detail": "Compute GPUs were rented"}, status=400)

                compute_gpu = ComputeGPU.objects.filter(id=compute_gpu_id).first()
                if compute_gpu:
                    if ComputeMarketplace.objects.filter(
                        id=compute_gpu.compute_marketplace_id, owner_id=user_id
                    ).exists():
                        return Response(
                            {"detail": "You cannot rent your own compute"},
                            status=status.HTTP_403_FORBIDDEN,
                        )

                    compute_gpu.status = "renting"
                    compute_gpu.owner_id = compute.owner_id
                    compute_gpu.save()
                    History_Rent_Computes.objects.create(
                        account_id=user_id,
                        compute_marketplace_id=compute_gpu.compute_marketplace_id,
                        compute_gpu_id=compute_gpu_id,
                        status="renting",
                        order_id=payment["order_id"],
                        rental_hours=hours,
                        time_end=time_end,
                        compute_install=compute_install,
                    )
                else:
                    return Response({"detail": "Compute GPU not found"}, status=404)
            compute_gpu_in_marketplace = ComputeGPU.objects.filter(
                status="in_marketplace", compute_marketplace_id=compute.pk
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
            )
            return Response(
                {"id": create.id, "name": create.name, "author_id": create.author_id},
                status=201,
            )
        # process send mail when is rent done here
        # try:
        #     send_to = [user.username] if user.username else [user.email]

        #     # notify_reponse = ServiceSendEmail(DOCKER_API)
        #     data = {
        #             "subject": "Successfully hired compute",
        #             "from": "no-reply@staging.aixblock.org",
        #             "to": [f"{user.email}"],
        #             "html": f"<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Welcome to AIxBlock</title></head><body><p>Hi [{send_to}],</p><p>You have successfully hired Compute</p><p>Thank you for choosing AIxBlock. We look forward to supporting your journey with AI and blockchain technologies.</p><p>Best Regards,<br>The AIxBlock Team</p></body></html>",
        #             "text": "Welcome to AIxBlock!",
        #             "attachments": []
        #         }
        #     notify_reponse.send_email(data)
        #     print('send done')
        # except Exception as e:
        #     print(e)

        return super(ComputeMarketplaceRentAPI, self).patch(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(ComputeMarketplaceRentAPI, self).put(request, *args, **kwargs)

request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        # "compute_gpus_id": openapi.Schema(
        #     type=openapi.TYPE_STRING,
        #     description="Compute GPUs ID list, '11,12'",
        # ),
        # "vast_contract_id": openapi.Schema(
        #     type=openapi.TYPE_STRING,
        #     description="Vast contract ID list, can be empty",
        # ),
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
        tags=["Compute Marketplace"],
        operation_summary="Rent Compute Gpu Marketplace v2",
        operation_description="Rent Compute Gpu Marketplace",
        request_body=request_body
    ),
)
class ComputeMarketplaceRentV2API(generics.CreateAPIView):
    serializer_class = ComputeMarketplaceRentV2Serializer
    queryset = ComputeMarketplace.objects.all()
    permission_required = ViewClassPermission(
        POST=all_permissions.projects_change,
    )
    def post(self, request, *args, **kwargs):
        return Response(status=200)


class ComputeMarketplaceResolveAPI(generics.UpdateAPIView):
    permission_required = ViewClassPermission(
        PATCH=all_permissions.annotations_view,
    )

    def get_queryset(self):
        ComputeMarketplace_pk = self.request.data.get("id")
        project_pk = self.request.query_params.get("project")
        return ComputeMarketplace.objects.filter(id=ComputeMarketplace_pk)

    def patch(self, request, *args, **kwargs):
        ComputeMarketplace = self.get_object()

        if ComputeMarketplace is not None:
            # ComputeMarketplace.is_resolved = request.data.get('is_resolved')
            # ComputeMarketplace.save(update_fields=frozenset(['is_resolved']))
            return Response(ComputeMarketplaceSerializer(ComputeMarketplace).data)

        return Response(status=404)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Compute marketplace generate token worker",
        operation_description="Compute marketplace generate token worker.",
    ),
)
class ComputeMarketplaceGenTokenAPI(generics.ListAPIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get(self, request, *args, **kwargs):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        infrastructure_id = "".join(random.choice(chars) for _ in range(12))
        return Response({"token": infrastructure_id}, status=200)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Compute marketplace generate client secret",
        operation_description="Compute marketplace generate client secret.",
    ),
)
class ComputeMarketplaceGenSecretAPI(generics.ListAPIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        org_id = self.request.user.active_organization_id
        current_date = datetime.now().strftime("%d%m%Y")
        Application = get_application_model()
        app = Application()
        app.name = f"{user_id}_{org_id}_{current_date}"
        app.client_type = "confidential"
        app.authorization_grant_type = "authorization-code"
        app.user_id = user_id
        # ip_address = "108.181.196.144"  # <== need to set value ip of client platform for this var
        # app.redirect_uris = [f"http://{ip_address}:8080/oauth/login/callback"]

        app.save()
        return Response(
            {"client_id": app.client_id, "client_secret": app.client_secret}, status=200
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Compute marketplace user create self host",
        operation_description="Compute marketplace user create.",
    ),
)
class ComputeMarketplaceUserCreateAPI(generics.CreateAPIView):
    serializer_class = ComputeMarketplaceUserCreateSerializer
    permission_required = ViewClassPermission(
        POST=all_permissions.annotations_view,
    )
    parser_classes = MultiPartParser, JSONParser

    def perform_create(self, serializer):
        user_id = self.request.user.id
        org_id = self.request.user.active_organization_id

        if serializer.is_valid(raise_exception=True):
            serializer.save(owner_id=user_id, author_id=user_id, organization_id=org_id)

    def post(self, request, *args, **kwargs):
        from .self_host import delete_compute_duplicate_ip
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = get_env("MASTER_TOKEN", "")
        # if (access_token != ''):
        # endpoint = get_env('MASTER_NODE','https://app.aixblock.io')
        # headers = {
        #     f'Authorization': 'Token {access_token}'
        # }
        # response = requests.post(f"{endpoint}/api/model_marketplace/user/create", headers=headers, data=request.data)
        # print(response)
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     return Response({
        #         "error": "Failed to create user in the marketplace",
        #     }, status=response.status_code)

        ip_address = request.data.get("ip_address")
        compute_gpus = request.data.get("compute_gpus")
        infrastructure_id = request.data.get("infrastructure_id")
        compute_type = request.data.get("compute_type")
        config = request.data.get("config")
        client_secret = request.data.get("client_secret")
        location_id =  request.data.get("location_id")
        location_name =  request.data.get("location_name")
        location_alpha2 =  request.data.get("location_alpha2")
        client_id = request.data.get("client_id")
        cuda = request.data.get("cuda")
        user_id = request.user.id
        delete_compute_duplicate_ip(ip_address)
        compute = ComputeMarketplace.objects.filter(infrastructure_id=infrastructure_id, deleted_at__isnull = True).first()
        # compute = ComputeMarketplace.objects.filter(ip_address = ip_address, deleted_at__isnull = True).first()
        # handle if compute new
        # 1 gpu create 1 record in history_rent_compute and compute gpu
        org = Organization.objects.filter(created_by_id=user_id).first()
        if org is None:
            org = 0
        # nếu compute là máy mới
        # tạo compute, compute gpu và history rent cho từng compute gpu
        if compute is None:
            compute = ComputeMarketplace.objects.create(
                name=ip_address,
                infrastructure_id=infrastructure_id,
                owner_id=user_id,
                author_id=user_id,
                catalog_id=0,
                organization_id=org.id,
                config=config,
                ip_address=ip_address,
                docker_port=4243,
                kubernetes_port=6443,
                status="created",
                client_id=client_id,
                client_secret=client_secret,
                type=ComputeMarketplace.Type.COMPUTE_SELF_HOST,
                location_id = location_id,
                location_alpha2 = location_alpha2,
                location_name = location_name
            )
            compute_gpu = None
            # create compute gpu
            if len(compute_gpus) > 0:
                cuda_info = cuda[0]
                ram_info = cuda_info.get("ram_info")
                # ram_info = json.loads(cuda_info.get("ram_info"))
                for gpu in compute_gpus:
                    gpu_memory = gpu["gpu_memory"] 
                    if gpu_memory is None or gpu_memory == "":
                        gpu_memory = convert_mb_to_byte(ram_info['total_ram_mb'])
                    compute_gpu = ComputeGPU.objects.create(
                        compute_marketplace=compute,
                        infrastructure_id=compute,
                        gpu_id=gpu["gpu_id"],
                        gpu_name=gpu["gpu_name"],
                        memory_usage="",
                        gpu_memory = gpu_memory,
                        gpu_tflops=cuda_info["tflops"],
                        status="created",
                        gpu_index=gpu["gpu_index"],
                        mem_clock_mhz=cuda_info["mem_clock_mhz"],
                        gpu_clock_mhz=cuda_info["gpu_clock_mhz"],
                        memory_bus_width=cuda_info["memory_bus_width"],
                        number_of_pcie_per_gpu=f"{cuda_info['pcie_link_gen_max']},{cuda_info['pcie_link_width_max']}",
                        max_cuda_version=cuda_info["driver_version"],
                        cores=cuda_info["cores"],
                        cuda_cores=cuda_info["cuda_cores"],
                        ubuntu_version=cuda_info["ubuntu_version"],
                        owner_id=user_id,
                        branch_name=gpu["branch_name"].lower(),
                        eff_out_of_total_nu_of_cpu_virtual_cores=f"{cuda_info['used_cores']}/{cuda_info['cpu_cores']}",
                        eff_out_of_total_system_ram=f"{convert_mb_to_gb(ram_info['used_ram_mb'])}/{convert_mb_to_gb(ram_info['total_ram_mb'])}",
                        # total_memory_used=ram_info["used_ram_mb"],
                        gpu_memory_bandwidth=convert_gb_to_byte(
                            cuda_info["mem_bandwidth_gb_per_s"]
                        ),
                        location_id = location_id,
                        location_alpha2 = location_alpha2,
                        location_name = location_name

                    )

                    History_Rent_Computes.objects.create(
                        account_id=user_id,
                        compute_marketplace_id=compute_gpu.compute_marketplace_id,
                        compute_gpu_id=compute_gpu.id,
                        status="renting",
                        compute_install="installing",
                        service_type = compute_type
                    )

            # handle cpu
            if len(compute_gpus) == 0:
                History_Rent_Computes.objects.create(
                        account_id=user_id,
                        compute_marketplace_id=compute.id,
                        compute_gpu_id=None,
                        status="renting",
                        compute_install="installing",
                        service_type = compute_type

                )
                compute.is_using_cpu = True
                compute.save()

        # nếu đã có compute. reset toàn bộ dữ liệu cũ và update lại data mới (xoá ml liên quan)
        # gỡ compute_gpu về chợ và trạng thái là install_status là installing
        else:
            # xoá ml đang chạy bởi compute id
            # update data compute
            compute.name=ip_address
            compute.infrastructure_id=infrastructure_id
            compute.owner_id=user_id
            compute.author_id=user_id
            compute.catalog_id=0
            compute.organization_id=org.id
            compute.config=config
            compute.ip_address=ip_address
            compute.docker_port=4243
            compute.kubernetes_port=6443
            compute.status="created"
            compute.client_id=client_id
            compute.client_secret=client_secret
            compute.type=ComputeMarketplace.Type.COMPUTE_SELF_HOST
            compute.location_id = location_id
            compute.location_alpha2 = location_alpha2
            compute.location_name = location_name
            compute.save()
            mlgpus = MLGPU.objects.filter(compute_id= compute.id, deleted_at__isnull = True).all()
            if len(mlgpus) ==0:
                if len(compute_gpus) > 0:

                    cuda_info = cuda[0]
                    ram_info = cuda_info.get("ram_info")
                    # ram_info = json.loads(cuda_info.get("ram_info"))
                    for gpu in compute_gpus:
                        gpu_memory = gpu["gpu_memory"] 
                        if gpu_memory is None or gpu_memory == "":
                            gpu_memory = convert_mb_to_byte(ram_info['total_ram_mb'])
                        compute_gpu = ComputeGPU.objects.create(
                          compute_marketplace=compute,
                          infrastructure_id=compute,
                          gpu_id=gpu["gpu_id"],
                          gpu_name=gpu["gpu_name"],
                          memory_usage="",
                          gpu_memory = gpu_memory,
                          gpu_tflops=cuda_info["tflops"],
                          status="created",
                          gpu_index=gpu["gpu_index"],
                          mem_clock_mhz=cuda_info["mem_clock_mhz"],
                          gpu_clock_mhz=cuda_info["gpu_clock_mhz"],
                          memory_bus_width=cuda_info["memory_bus_width"],
                          number_of_pcie_per_gpu=f"{cuda_info['pcie_link_gen_max']},{cuda_info['pcie_link_width_max']}",
                          max_cuda_version=cuda_info["driver_version"],
                          cores=cuda_info["cores"],
                          cuda_cores=cuda_info["cuda_cores"],
                          ubuntu_version=cuda_info["ubuntu_version"],
                          owner_id=user_id,
                          branch_name=gpu["branch_name"].lower(),
                          eff_out_of_total_nu_of_cpu_virtual_cores=f"{cuda_info['used_cores']}/{cuda_info['cpu_cores']}",
                          eff_out_of_total_system_ram=f"{convert_mb_to_gb(ram_info['used_ram_mb'])}/{convert_mb_to_gb(ram_info['total_ram_mb'])}",
                          # total_memory_used=ram_info["used_ram_mb"],
                          gpu_memory_bandwidth=convert_gb_to_byte(
                              cuda_info["mem_bandwidth_gb_per_s"]
                          ),
                          location_id = location_id,
                          location_alpha2 = location_alpha2,
                          location_name = location_name

                      )
                        history = History_Rent_Computes.objects.filter(compute_marketplace_id = compute.id, deleted_at__isnull = True).first()
                        if history and history.compute_gpu_id is None:
                            history.compute_gpu_id=compute_gpu.id
                            history.compute_install="installing"
                            history.service_type = compute_type
                            history.status="renting"
                            history.save()
                        else:
                            History_Rent_Computes.objects.create(
                            account_id=user_id,
                            compute_marketplace_id=compute_gpu.compute_marketplace_id,
                            compute_gpu_id=compute_gpu.id,
                            status="renting",
                            compute_install="installing",
                            service_type = compute_type
                        )

                # handle cpu
                if len(compute_gpus) == 0:
                    history = History_Rent_Computes.objects.filter(compute_marketplace_id = compute.id, deleted_at__isnull = True).first()
                    if history is None:
                        History_Rent_Computes.objects.create(
                              account_id=user_id,
                              compute_marketplace_id=compute.id,
                              compute_gpu_id=None,
                              status="renting",
                              compute_install="installing",
                              service_type = compute_type

                      )
                    else:
                        history.compute_install = "installing"
                        history.service_type = compute_type
                        history.save()
                    compute.is_using_cpu = True
                    compute.save()
            for ml_gpu in mlgpus:
                mlbackend = MLBackend.objects.filter(id=ml_gpu.id).first()
                mlbackend.deleted_at = timezone.now()
                mlbackend.save()
                ml_gpu.deleted_at = timezone.now()
                ml_gpu.save()

            histories = History_Rent_Computes.objects.filter(compute_marketplace_id = compute.id, status = "renting", deleted_at__isnull = True, deleted_by__isnull = True).all()
            if histories.count() > 0 :
                for history in histories:
                    # update lại bản status renting và  compute_install="installing"
                    history.status = "renting"
                    history.compute_install = History_Rent_Computes.InstallStatus.INSTALLING
                    history.save()
            if len(compute_gpus) > 0:
                for gpu in compute_gpus:
                    # update lại compute gpu
                    compute_gpu = ComputeGPU.objects.filter(
                        gpu_id=gpu["gpu_id"], deleted_at__isnull=True
                    ).update(
                        compute_marketplace=compute,
                        infrastructure_id=compute,
                        gpu_id=gpu["gpu_id"],
                        gpu_name=gpu["gpu_name"],
                        memory_usage="",
                        gpu_memory=gpu_memory,
                        gpu_tflops=cuda_info["tflops"],
                        status="created",
                        gpu_index=gpu["gpu_index"],
                        mem_clock_mhz=cuda_info["mem_clock_mhz"],
                        gpu_clock_mhz=cuda_info["gpu_clock_mhz"],
                        memory_bus_width=cuda_info["memory_bus_width"],
                        number_of_pcie_per_gpu=f"{cuda_info['pcie_link_gen_max']},{cuda_info['pcie_link_width_max']}",
                        max_cuda_version=cuda_info["driver_version"],
                        cores=cuda_info["cores"],
                        cuda_cores=cuda_info["cuda_cores"],
                        ubuntu_version=cuda_info["ubuntu_version"],
                        owner_id=user_id,
                        branch_name=gpu["branch_name"].lower(),
                        eff_out_of_total_nu_of_cpu_virtual_cores=f"{cuda_info['used_cores']}/{cuda_info['cpu_cores']}",
                        eff_out_of_total_system_ram=f"{convert_mb_to_gb(ram_info['used_ram_mb'])}/{convert_mb_to_gb(ram_info['total_ram_mb'])}",
                        # total_memory_used=ram_info["used_ram_mb"],
                        gpu_memory_bandwidth=convert_gb_to_byte(
                            cuda_info["mem_bandwidth_gb_per_s"]
                        ),
                        location_id=location_id,
                        location_alpha2=location_alpha2,
                        location_name=location_name,
                    )

        compute_type = request.data.get("compute_type")
        if compute_type == None:
            compute_type = "full"
        client_id = request.data.get("client_id")
        client_secret = request.data.get("client_secret")
        user = request.user
        token = Token.objects.get(user=user)
        def pull_docker_container_and_update(compute_type, ip_address, client_id, client_secret, token, user_id, compute_marketplace_id, user, compute):
            max_retries = 5
            retry_delay = 5  # thời gian chờ giữa các lần thử lại (tính bằng giây)
            retries = 0
            #  create Thread
            compute_install = 'completed'
            minio_port = None
            user_email = None
            password = None
            network_name = None
            try:
                history_id = None
                #  create Thread
                history = History_Rent_Computes.objects.filter(compute_marketplace_id=compute_marketplace_id, deleted_at__isnull=True).order_by("-id").first()
                if history:
                    history_id = history.id
                _port, minio_port, user_email, password, minio_user_username, minio_password, network_name, minio_api_port = dockerContainerPull(
                    compute_type, ip_address, client_id, client_secret, token, user_id, history_id=history_id
                )
            except Exception as e:
                # Xử lý khi gặp lỗi trong dockerContainerPull
                _port = 0  # hoặc giá trị mặc định khác phù hợp
                compute_install = 'failed'
                print(f"Error in dockerContainerPull: {e}")

            while retries < max_retries:
                try:
                    compute = ComputeMarketplace.objects.filter(pk=compute_marketplace_id).first()
                    port = _port
                    schema = 'https'
                    if compute_type == "storage":
                        schema = "http"
                    if port == 0 or port is None and minio_api_port is not None:
                        port = minio_api_port
                    compute.port = _port
                    compute.api_port = minio_api_port
                    compute.save()
                    compute_gpus = ComputeGPU.objects.filter(compute_marketplace_id=compute_marketplace_id, deleted_at__isnull = True).all()
                    if len(compute_gpus) > 0:
                        for compute_gpu in compute_gpus:
                            gpu = ComputeGPU.objects.filter(id =compute_gpu.id ).first()
                            gpu.status = ComputeGPU.Status.IN_MARKETPLACE
                            gpu.save()
                            history = History_Rent_Computes.objects.filter(compute_marketplace_id = compute_marketplace_id,compute_gpu_id = compute_gpu.id, deleted_at__isnull = True ).first()
                            if history:
                                history.compute_install = compute_install
                                history.type = History_Rent_Computes.Type.OWN_NOT_LEASING
                                history.service_type = compute_type
                                history.schema = schema
                                history.container_network = network_name
                                history.port = port
                                history.save()
                    if compute and compute.is_using_cpu:
                        history = History_Rent_Computes.objects.filter(compute_marketplace_id = compute_marketplace_id,compute_gpu_id__isnull = True, deleted_at__isnull = True ).first()
                        if history:
                            history.compute_install = compute_install
                            history.type = History_Rent_Computes.Type.OWN_NOT_LEASING
                            history.service_type = compute_type
                            history.schema = schema
                            history.container_network = network_name
                            history.port = port
                            history.save()
                    
                    publish_message(
                        channel=compute.infrastructure_id, data={"refresh": True}, prefix=True
                    )

                    publish_message(
                        channel=compute.infrastructure_id,
                        data={"type": "Done", "data": "Successfully installed."},
                        prefix=True,
                    )

                    break

                except OperationalError as e:
                    retries += 1
                    print(f"Lỗi kết nối cơ sở dữ liệu: {e}. Thử lại lần {retries}/{max_retries}...")
                    time.sleep(retry_delay)
            else:
                print("Không thể kết nối đến cơ sở dữ liệu sau nhiều lần thử lại.")

            def send_mail_rent_compute(user, compute, tensorboard, ddp):
                send_to = user.username if user.username else user.email

                html_file_path =  './templates/mail/rent_compute_success.html'
                with open(html_file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                html_content = html_content.replace('[user]', f'{send_to}')
                html_content = html_content.replace("rented", "set up")
                html_content = html_content.replace('xxx', f'{compute.id}')
                html_content = html_content.replace('[endpoint]', f'https://{compute.ip_address}:{compute.port}')
                html_content = html_content.replace('[tensorboard]', f'http://{compute.ip_address}:{tensorboard}')
                html_content = html_content.replace('[ddp]', f'{compute.ip_address}{ddp}')

                data = {
                    "subject": "AIxBlock | Confirmation of Successful Compute Setup",
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

                email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
                email_thread.start()
            
            def send_mail_rent_compute_platform_with_s3(user, compute, email_user, pass_user, user_minio, pass_minio, minio_port, minio_api_port):
                send_to = user.username if user.username else user.email

                html_file_path =  './templates/mail/rent_compute_success_platform_with_s3.html'
                with open(html_file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                html_content = html_content.replace('[user]', f'{send_to}')
                html_content = html_content.replace('xxx', f'{compute.id}')
                html_content = html_content.replace('[domain]', f'https://{compute.ip_address}:{compute.port}')
                html_content = html_content.replace('[email]', email_user)
                html_content = html_content.replace('[pass]', pass_user)

                html_content = html_content.replace('[endpoint_minio]', f'{compute.ip_address}:{minio_port}')
                html_content = html_content.replace('[endpoint_minio_api]', f'http://{compute.ip_address}:{minio_api_port}')
                html_content = html_content.replace('[user_minio]', user_minio)
                html_content = html_content.replace('[pass_minio]', pass_minio)

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

                email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
                email_thread.start()

            def send_mail_s3(user, compute, email_user, pass_user):
                compute = ComputeMarketplace.objects.filter(id = compute.id).first()

                html_file_path =  './templates/mail/s3_vast.html'
                with open(html_file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                # notify_reponse = ServiceSendEmail(DOCKER_API)
                html_content = html_content.replace('[user]', f'{user.email}')
                html_content = html_content.replace('xxx', f'{compute.id}')

                html_content = html_content.replace('[endpoint_minio]', f'{compute.ip_address}:{compute.port}')
                html_content = html_content.replace('[endpoint_minio_api]', f'http://{compute.ip_address}:{compute.api_port}')

                html_content = html_content.replace('[user_minio]', email_user)
                html_content = html_content.replace('[pass_minio]', pass_user)

                data = {
                    "subject": f"AIxBlock | Confirmation of Compute Setup and Your Storage Access",
                    "from": "noreply@aixblock.io",
                    "to": [f"{user.email}"],
                    "html": html_content,
                    "text": "Remove compute!",
                }

                docket_api = "tcp://69.197.168.145:4243"
                host_name = MAIL_SERVER

                email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
                email_thread.start()
            try:
                if compute_type != "model-training":
                    if compute_type in ["full", "label-tool"]:
                        if minio_user_username:
                            send_mail_rent_compute_platform_with_s3(user, compute, user_email, password, minio_user_username, minio_password, minio_port, minio_api_port)
                        else:
                            send_mail_rent_compute_platform(user, compute, user_email, password)
                        # html_file_path =  './templates/mail/rent_compute_success_platform.html'
                        # with open(html_file_path, 'r', encoding='utf-8') as file:
                        #     html_content = file.read()

                        # html_content = html_content.replace('[user]', f'{send_to}')
                        # html_content = html_content.replace('xxx', f'{compute.infrastructure_id}')
                        # html_content = html_content.replace('[domain]', f'{compute.ip_address}:{compute.port}')
                        # html_content = html_content.replace('[email]', user_email)
                        # html_content = html_content.replace('[pass]', password)

                        # data = {
                        #     "subject": "AIxBlock | Confirmation of Compute Rental",
                        #     "from": "noreply@aixblock.io",
                        #     "to": [f'{user.email}'],
                        #     "html": html_content,
                        #     "text": "Welcome to AIxBlock!",
                        #     "attachments": []
                        # }

                    else:
                        send_mail_s3(user, compute, minio_user_username, minio_password)
                        # html_file_path =  './templates/mail/s3_full_service.html'
                        # with open(html_file_path, 'r', encoding='utf-8') as file:
                        #     html_content = file.read()

                        # # notify_reponse = ServiceSendEmail(DOCKER_API)
                        # html_content = html_content.replace('[user]', f'{send_to}')
                        # html_content = html_content.replace('xxx', f'{compute.infrastructure_id}')
                        # html_content = html_content.replace('[endpoint_minio]', f'{ip_address}:{_port}')

                        # html_content = html_content.replace('[user_minio]', minio_user_email)
                        # html_content = html_content.replace("[pass_minio]", minio_password)

                        # data = {
                        #     "subject": f"AIxBlock | Confirmation of Compute Rental and Your Storage Access",
                        #     "from": "noreply@aixblock.io",
                        #     "to": [f"{user.email}"],
                        #     "html": html_content,
                        #     "text": "Remove compute!",
                        # }

                else:   
                    send_mail_rent_compute(user, compute, minio_port, user_email)                 
                    # html_file_path =  './templates/mail/rent_compute_success.html'
                    # with open(html_file_path, 'r', encoding='utf-8') as file:
                    #     html_content = file.read()

                    # html_content = html_content.replace('[user]', f'{send_to}')
                    # html_content = html_content.replace('xxx', f'{compute.infrastructure_id}')

                    # data = {
                    #     "subject": "AIxBlock | Confirmation of Compute Rental",
                    #     "from": "noreply@aixblock.io",
                    #     "to": [f'{user.email}'],
                    #     "html": html_content,
                    #     "text": "Welcome to AIxBlock!"
                    # }

                # docket_api = "tcp://69.197.168.145:4243"
                # host_name = MAIL_SERVER

                # email_thread = threading.Thread(target=send_email_thread, args=(docket_api, host_name, data,))
                # email_thread.start()

            except Exception as e:
                print(e)

            try:
                from .self_host import check_status_port_docker, check_status_port_minio, check_status_port_platform, check_status_port_ml
                compute = ComputeMarketplace.objects.filter(pk=compute_marketplace_id).first()

                if compute_type in ["full", "label-tool"]:
                    check_status_port_docker(compute.ip_address, 4243, user.id, user.uuid, history.id)
                    check_status_port_minio(compute.ip_address, compute.api_port, user.id, user.uuid, history.id)
                    # check_status_port_minio(compute.ip_address, 9091, user.id, user.uuid, history.id)
                    check_status_port_platform(compute.ip_address, compute.port, user.id, user.uuid, history.id)
                elif compute_type == "storage":
                    check_status_port_minio(compute.ip_address, compute.api_port, user.id, user.uuid, history.id)
                    # check_status_port_minio(compute.ip_address, 9091, user.id, user.uuid, history.id)

                elif compute_type == "model-training":
                    check_status_port_ml(compute.ip_address, compute.port, user.id, user.uuid, history.id)

                notify_for_compute(user.uuid, "Success", "Compute installation completed.")
                update_notify_install("Compute installation successful.", compute.owner_id, f"Compute installation successful.", history.id, "Install Compute", "success")

            except Exception as e:
                print(e)

        threading.Thread(
            target=pull_docker_container_and_update,
            args=(compute_type, ip_address, client_id, client_secret, token, user_id, compute.id, user, compute),
        ).start()
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # data = serializer.data
        # compute_marketplace_id = compute.id
        # data["id"] = compute_marketplace_id
        return Response(serializer.data, status=status.HTTP_201_CREATED,)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Compute marketplace user create full flow",
        operation_description="Compute marketplace user create full flow.",
    ),
)
class ComputeMarketplaceUserCreateFullAPI(generics.CreateAPIView):
    serializer_class = ComputeMarketUserCreateFullSerializer
    permission_required = ViewClassPermission(
        POST=all_permissions.annotations_view,
    )
    parser_classes = MultiPartParser, FileUploadParser

    def perform_create(self, serializer):
        user_id = self.request.user.id
        org_id = self.request.user.active_organization_id
        current_date = datetime.now().strftime("%d%m%Y")
        Application = get_application_model()
        app = Application()
        app.name = f"{user_id}_{org_id}_{current_date}"
        app.client_type = "confidential"
        app.authorization_grant_type = "authorization-code"
        app.user_id = user_id
        app.save()

        serializer.save(
            owner_id=user_id,
            author_id=user_id,
            organization_id=org_id,
            client_id=app.client_id,
            client_secret=app.client_secret,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        ip_address = request.data.get("ip_address")
        config_data = request.data.get("config")
        existing_instance = ComputeMarketplace.objects.filter(
            ip_address=ip_address, deleted_at__isnull=True
        ).first()
        if existing_instance:
            # If it exists, update the config field and save the record
            existing_instance.config = json.loads(config_data)
            existing_instance.save()
            if serializer.is_valid():
                data = serializer.data
                data["id"] = existing_instance.id
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # compute_type = request.data.get('compute_type')
        # OAUTH_CLIENT_ID = request.data.get('client_id')
        # OAUTH_CLIENT_SECRET = request.data.get('client_secret')
        # client = docker.DockerClient(base_url=f"tcp://{ip_address}:4243")
        # client.login(username='quoiwowai', password='Abc!23456')

        # if compute_type == 'storage':
        #     client.api.pull('wowai/storage:latest', stream=True, decode=True)
        # if compute_type == 'GPU':
        # client.api.pull('wowai/segment_anything:latest', stream=True, decode=True)
        # client.api.pull('wowai/llama_meta_2:latest', stream=True, decode=True)
        # client.api.pull('wowai/falcon7b:latest', stream=True, decode=True)
        # client.api.pull('wowai/seamless_m4t:latest', stream=True, decode=True)
        # if compute_type == 'full':
        #     client.api.pull('aixblock/platform:latest', stream=True, decode=True)
        #     container = client.containers.run(
        #         "aixblock/platform:latest",
        #         detach=True,
        #         name=f"wowai-label-tool",
        #         device_requests=[

        #         ],
        #         ports={
        #             '8080/tcp': '8080',
        #         },
        #         environment={
        #             "POSTGRES_HOST":ip_address,
        #             "POSTGRES_PASSWORD":"@9^xwWA",
        #             "POSTGRES_NAME":"platform_v2",
        #             "POSTGRES_USER":"postgres",
        #             'OAUTH_CLIENT_ID':get_env('OAUTH_CLIENT_ID',f'{OAUTH_CLIENT_ID}'),
        #             'OAUTH_CLIENT_SECRET':get_env('OAUTH_CLIENT_SECRET',f'{OAUTH_CLIENT_SECRET}'),
        #             'OAUTH_TOKEN_URL':get_env('OAUTH_TOKEN_URL', 'https://app.aixblock.io'),
        #             'OAUTH_AUTHORIZE_URL':get_env('OAUTH_AUTHORIZE_URL','https://app.aixblock.io/o/authorize'),
        #             'OAUTH_API_BASE_URL':get_env('OAUTH_API_BASE_URL','https://app.aixblock.io'),
        #             'OAUTH_REDIRECT_URL':get_env('OAUTH_REDIRECT_URL',f'http://{ip_address}:8080/oauth/login/callback'),
        #             "MASTER_NODE":'https://app.aixblock.io',
        #             "MASTER_TOKEN":""
        #         },
        #         volumes={
        #         }
        #     )
        #     container.exec_run('python3 aixblock_core/manage.py create_superuser_with_password --username admin --password 123321 --noinput --email admin@wow-ai.com')
        #     container.exec_run('python3 aixblock_core/manage.py create_organization "default" --created_by_id 1 --token "unique_token" --team_id 1 --status "actived"')
        #     container.exec_run('python3 aixblock_core/manage.py seed_templates')
        # client.api.pull('wowai/infrastructure_verification:latest', stream=True, decode=True)
        # container = client.containers.run(
        #     "wowai/infrastructure_verification:latest",
        #     detach=True,
        #     name=f"wowai-infrastructure_verification",
        #     device_requests=[

        #     ],
        #     ports={
        #         '9090/tcp': '9090',
        #     },
        #     environment={
        #         # "SERVICE": "wowai/infrastructure_verification:latest",
        #     },
        #     volumes={
        #     }
        # )
        # client.api.pull('wowai/segment_anything:latest', stream=True, decode=True)
        # client.api.pull('wowai/llama_meta_2:latest', stream=True, decode=True)
        # client.api.pull('wowai/falcon7b:latest', stream=True, decode=True)
        # client.api.pull('wowai/seamless_m4t:latest', stream=True, decode=True)
        # client.api.pull('wowai/jupyterhub-notebook:latest', stream=True, decode=True)
        # container = client.containers.run(
        #     "wowai/jupyterhub-notebook:latest",
        #     detach=True,
        #     name=f"wowai-jupyterhub-notebook",
        #     device_requests=[

        #     ],
        #     ports={
        #         '8100/tcp': '8100',
        #     },
        #     environment={

        #     },
        #     volumes={
        #         "createusers.txt":"/root/createusers.txt"
        #     }
        # )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        compute_marketplace_id = serializer.instance.id
        data["id"] = compute_marketplace_id
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="find compute, gpu detail by ip address",
        operation_description="find compute, gpu detail by ip address",
    ),
)
class ComputeMarketplaceGetByIP(generics.RetrieveAPIView):
    serializer_class = ComputeMarketplaceSerializer
    queryset = ComputeMarketplace.objects.all()

    def get_object(self):
        ip_address = self.kwargs.get("ip_address")
        queryset = self.get_queryset()

        # Exclude computes with history status "Wait-verify"
        compute_marketplaces = queryset.filter(
            ip_address=ip_address,
            deleted_at__isnull=True
        ).exclude(
            history_rent_computes__compute_install=History_Rent_Computes.InstallStatus.WAIT_VERIFY
        ).order_by('-created_at')

        if compute_marketplaces.exists():
            compute_response = compute_marketplaces.first()
            return compute_response
        else:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Compute marketplace does not exist for this IP address."},
                status=status.HTTP_404_NOT_FOUND,
            )

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List GPUs",
        operation_description="Get List GPUs.",
        manual_parameters=[
            openapi.Parameter(
                name="project_id",
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description="Project ID",
            ),
            openapi.Parameter(
                name="is_using",
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description="1: True, 0 False",
            ),
            openapi.Parameter(
                name="compute_type",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="model-training,storage,full, label-tool",
            ),
        ],
    ),
)
class ListGpu(generics.ListAPIView):
    serializer_class = ComputeMarketplaceRentedSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get_queryset(self):
        user_id = self.request.user.id
        serializer_context = {"user_id": user_id}
        serializer = self.get_serializer(context=serializer_context)
        rented_records = History_Rent_Computes.objects.filter(
            compute_marketplace_id=OuterRef("pk"),
            status="renting",
            compute_install="completed",
            account_id=user_id,
            deleted_by__isnull = True,
            deleted_at__isnull = True
        )

        queryset = (
            ComputeMarketplace.objects.filter(deleted_at__isnull=True)
            .annotate(
                compute_install=Subquery(rented_records.values("compute_install")[:1])
            )
            .annotate(
                num_rented=Subquery(
                    rented_records.values("compute_marketplace")
                    .annotate(count=Count("compute_marketplace"))
                    .values("count")
                )
            )
            .exclude(num_rented=0)
            .order_by("-id")
            .distinct()
        )

        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user
        # get container for this project
        project_id = request.query_params.get("project_id")
        is_using = request.query_params.get("is_using")
        compute_type = request.query_params.get("compute_type")
        is_deploy = request.query_params.get("is_deploy", None)

        if is_deploy and is_deploy == "1":
            is_deploy = True
            
        gpus = []
        queryset = self.get_queryset()
        # Compute self added              => author_id=user.id, status=ComputeMarketplace.Status.CREATED
        # Compute rented from marketplace => author_id=user.id, status=ComputeMarketplace.Status.RENTED_BOUGHT
        # list_comp = ComputeMarketplace.objects.filter(deleted_at__isnull = True]).all()
        ml_gpu_subquery = (
            MLGPU.objects.filter(ml_id=OuterRef("pk"))
            .exclude(Q(deleted_at__isnull=False))
            .values("gpus_id")
        )
        if is_deploy:
            ml_backends = MLBackend.objects.filter(project_id=project_id, is_deploy=True, deleted_at__isnull=True).annotate(
                gpus_id=Subquery(ml_gpu_subquery)
            )
        else:
            ml_backends = MLBackend.objects.filter(project_id=project_id, deleted_at__isnull=True).annotate(
                gpus_id=Subquery(ml_gpu_subquery)
            )

        gpus_ids = []

        for ml_backend in ml_backends:
            gpus_id = ml_backend.gpus_id
            gpus_ids.append(int(gpus_id) if gpus_id is not None else 0)
        for comp in queryset:
            try:
                # ALl GPUs of compute that owned by current user
                # All GPUs of compute that rented from marketplace

                history_rent_subquery = History_Rent_Computes.objects.filter(
                    compute_gpu_id=OuterRef('pk'),
                    status='renting',
                    account_id=user.id,
                    deleted_at__isnull = True,
                    deleted_by__isnull = True,
                    service_type=History_Rent_Computes.SERVICE_TYPE.MODEL_TRAINING
                )
                if compute_type:
                    history_rent_subquery = history_rent_subquery.filter(
                        service_type=compute_type
                    )
                compute_gpus = ComputeGPU.objects.filter(
                    Q(status="renting")|Q(status="in_marketplace"),
                    compute_marketplace_id=comp.id,
                    history_rent_computes__in=history_rent_subquery,
                ).distinct()

                # if not compute_gpus and not comp.is_using_cpu:  # Check if both compute_gpus and is_using_cpu are empty
                #     continue
                # nvidia-smi --query-gpu=index,gpu_name,gpu_bus_id,timestamp,power.draw,clocks.mem --format=csv

                # GPU 0: NVIDIA RTX A6000 (UUID: GPU-b8b0bee9-1a2f-a1ca-3f22-9eed1d675873)
                list_gpu = []
                cpu = {}
                for gpu in compute_gpus:
                    mlgpu = MLGPU.objects.filter(
                        gpus_id=gpu.id, deleted_at__isnull=True
                    ).first()
                    # gpu avaiable
                    if gpu.id not in gpus_ids:
                        if (is_using != '1' and mlgpu is None) :
                            list_gpu.append(
                                {
                                    "id": gpu.id,
                                    "gpu_name": gpu.gpu_name,
                                    "power_consumption": gpu.power_consumption,
                                    "memory_usage": gpu.memory_usage,
                                    "gpu_index": gpu.gpu_index,
                                    "gpu_id": gpu.gpu_id,
                                    "branch_name": gpu.branch_name,
                                    "machine_options": gpu.machine_options,
                                    "type": comp.type,
                                }
                            )
                    # using
                    if gpu.id in gpus_ids and is_using == '1': 
                        list_gpu.append(
                            {
                                "id": gpu.id,
                                "gpu_name": gpu.gpu_name,
                                "power_consumption": gpu.power_consumption,
                                "memory_usage": gpu.memory_usage,
                                "gpu_index": gpu.gpu_index,
                                "gpu_id": gpu.gpu_id,
                                "branch_name": gpu.branch_name,
                                "machine_options": gpu.machine_options,
                                "type": comp.type,
                            }
                        )
                    
                    if gpu.id in gpus_ids and is_using == '0': 
                        if is_deploy:
                            list_gpu.append(
                                {
                                    "id": gpu.id,
                                    "gpu_name": gpu.gpu_name,
                                    "power_consumption": gpu.power_consumption,
                                    "memory_usage": gpu.memory_usage,
                                    "gpu_index": gpu.gpu_index,
                                    "gpu_id": gpu.gpu_id,
                                    "branch_name": gpu.branch_name,
                                    "machine_options": gpu.machine_options,
                                    "type": comp.type,
                                }
                            )
                if comp.is_using_cpu:
                    # turn off cpu
                    cpu = comp.config
                # comp.is_using_cpu or
                if  len(list_gpu) > 0: 
                    gpus.append(
                        {
                            "compute_gpus": list_gpu,
                            "compute_cpu": cpu,
                            "is_using_cpu": comp.is_using_cpu,
                            "compute_name": comp.ip_address,
                            "compute_id": comp.pk,
                            "type": comp.type,
                            "is_scale": comp.is_scale
                        }
                    )
            except Exception as e:
                logging.error(e)
                continue

        return Response(gpus, status=200)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Compute Marketplace Supply",
    ),
)
class ComputeMarketplaceSupplierAPI(generics.ListAPIView):
    serializer_class = ComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    pagination_class = SetPagination

    def get_queryset(self):
        user_id = self.request.user.id
        return (
            ComputeMarketplace.objects.filter(owner_id=user_id, deleted_at__isnull=True)
            .exclude(status__in=["pending"])
            .exclude(type="COMPUTE-SELF-HOST")
            .order_by("-id")
        )

    def get(self, request, *args, **kwargs):
        return super(ComputeMarketplaceSupplierAPI, self).get(request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Compute Marketplace Rented",
        operation_description="Get List Compute Marketplace Supply by renter.",
    ),
)
class ComputeMarketplaceRentedAPI(generics.ListAPIView):
    serializer_class = ComputeMarketplaceRentedSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    pagination_class = SetPagination

    def get_queryset(self):
        user_id = self.request.user.id
        serializer_context = {"user_id": user_id}
        serializer = self.get_serializer(context=serializer_context)
        current_time = timezone.now()

        # Tính thời gian kết thúc dự kiến của mỗi bản ghi
        # end_times = [record.time_start + timedelta(hours=record.rental_hours) for record in History_Rent_Computes.objects.all()]

        # # Lọc ra các bản ghi có thời gian kết thúc dự kiến lớn hơn hoặc bằng thời gian hiện tại
        # records = [record for record, end_time in zip(History_Rent_Computes.objects.all(), end_times) if end_time <= current_time]

        # for rented_records_out_of_date in records:
        #     if rented_records_out_of_date.compute_marketplace.type == "MODEL-PROVIDER-VAST":
        #         delete_instance_info(rented_records_out_of_date.compute_marketplace.infrastructure_id)
        #     rented_records_out_of_date.deleted_at = timezone.now()
        #     rented_records_out_of_date.status = "completed"
        #     rented_records_out_of_date.save()

        rented_records = History_Rent_Computes.objects.filter(
            compute_marketplace_id=OuterRef("pk"),
            status="renting",
            # compute_install="completed",
            account_id=user_id,
            deleted_by__isnull = True,
            deleted_at__isnull = True
        )

        queryset = (
            ComputeMarketplace.objects.filter(deleted_at__isnull=True)
            .annotate(
                # Sử dụng Subquery để lấy trường compute_install từ bản ghi phù hợp
                compute_install=Subquery(rented_records.values("compute_install")[:1])
            )
            .annotate(
                # Sử dụng Subquery để đếm số lượng bản ghi thỏa mãn điều kiện đã cho
                num_rented=Subquery(
                    rented_records.values("compute_marketplace")
                    .annotate(count=Count("compute_marketplace"))
                    .values("count")
                )
            )
            .exclude(
                # Loại bỏ các bản ghi của ComputeMarketplace
                # mà không có bất kỳ bản ghi thuộc History_Rent_Computes
                # thỏa mãn điều kiện đã cho
                num_rented=0
            )
            .order_by("-id")
            .distinct()
        )

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user_id": self.request.user.id})
        return context

    def get(self, request, *args, **kwargs):
        return super(ComputeMarketplaceRentedAPI, self).get(request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Compute Marketplace Rented By Card",
        operation_description="Get List Compute Marketplace Rented By Card.",
        manual_parameters=[
            page_parameter,
            search_parameter,
            field_search_parameter,
            sort_parameter,
            type_parameter,
            field_query_parameter,
            query_value_parameter,
        ],
    ),
)
class ComputeMarketplaceRentedByCardAPI(generics.ListAPIView):
    serializer_class = ComputeMarketplaceRentedCardSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user_id = self.request.user.id
        rented_records = (
            History_Rent_Computes.objects.filter(
                account_id=user_id,
                status="renting",
                deleted_at__isnull=True,
                deleted_by__isnull=True,
            )
            .exclude(compute_install="wait_verify")
            .all()
        )
        for rented_record in rented_records:
            if (
                rented_record.compute_marketplace.type == "MODEL-PROVIDER-VAST"
                and rented_record.compute_install != "installing"
                and rented_record.compute_marketplace.compute_type == 'all'
            ):
                # status_vast = vast_service.get_instance_info(rented_record.compute_marketplace.infrastructure_id)
                status_vast = vast_provider.info_compute(rented_record.compute_marketplace.infrastructure_id)
                if not status_vast['instances']:
                    # status_vast.deleted_at = timezone.now()
                    rented_record.compute_marketplace.deleted_at = timezone.now()
                    rented_record.compute_gpu.deleted_at = timezone.now()
                    rented_record.deleted_at = timezone.now()
                    rented_record.status = "completed"
                    rented_record.save()

        rented_records = rented_records.filter(deleted_at__isnull=True).select_related("compute_marketplace", "compute_gpu")
        return filterModel(self, rented_records, History_Rent_Computes)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="delete Marketplace Rented By Card",
        operation_description="delete Marketplace Supply by renter."
    ),
)
class HistoryRentComputeDeleteAPI(generics.DestroyAPIView):
    queryset = History_Rent_Computes.objects.all()
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    serializer_class = HistoryRentComputeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

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

        if request.query_params.get("project_id"):
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
                        hours_remaining = (instance.time_end - timezone.now()).total_second() / 3600
                        refund_amount = hours_remaining * compute_price.price
                        amount = math.floor(refund_amount * 100) / 100

                        req = requests.post(
                            settings.CRYPTO_API + "/api/v1/sign-message/cancel",
                            headers={
                                # "Authorization": "Basic " + basic_token,
                                "Content-Type": "application/json",
                            },

                            data=json.dumps({
                                "invoiceId": instance.order_id,
                                "walletAddress": request.data.get("walletAddress"),
                                "amountUSD": amount
                            })
                        )

                        data = req.json()

                        if not req.ok:
                            return Response(data, status=status.HTTP_400_BAD_REQUEST)
                        
                        return Response(data, status=status.HTTP_200_OK)
                
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

        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Catalog Compute Marketplace",
        manual_parameters=[
            openapi.Parameter(
                name="filter", type=openapi.TYPE_STRING, in_=openapi.IN_QUERY
            ),
            openapi.Parameter(
                name="value", type=openapi.TYPE_STRING, in_=openapi.IN_QUERY
            ),
        ],
    ),
)
class CataLogComputeMarketplaceAPI(generics.ListAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get_queryset(self):
        filter = self.request.GET.get("filter")
        value = self.request.GET.get("value")
        if filter == "all":
            return CatalogComputeMarketplace.objects.filter(
                Q(name__icontains=value)
                | Q(tag__icontains=value)
                | Q(status__icontains=value)
            ).order_by("-id")
        if filter == "name":
            return CatalogComputeMarketplace.objects.filter(
                name__icontains=value
            ).order_by("-id")
        if filter == "status":
            return CatalogComputeMarketplace.objects.filter(
                status__icontains=value
            ).order_by("-id")
        if filter == "tag":
            return CatalogComputeMarketplace.objects.filter(
                tag__icontains=value
            ).order_by("-id")

        return CatalogComputeMarketplace.objects.order_by("-id")

    def get(self, request, *args, **kwargs):
        return super(CataLogComputeMarketplaceAPI, self).get(request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List Catalog Compute with paginate",
    ),
)
class CataLogComputePaginateAPI(generics.ListAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    pagination_class = SetPagination

    def get_queryset(self):
        return CatalogComputeMarketplace.objects.order_by("-id")

    def get(self, request, *args, **kwargs):
        return super(CataLogComputePaginateAPI, self).get(request, *args, **kwargs)


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Delete Catalog Compute Marketplace",
    ),
)
class CataLogComputeMarketplaceDelAPI(generics.DestroyAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get_queryset(self):
        return CatalogComputeMarketplace.objects.order_by("-id")

    def delete(self, request, *args, **kwargs):
        super(CataLogComputeMarketplaceDelAPI, self).delete(request, *args, **kwargs)
        return Response({"status": "success"}, status=200)


@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Delete Catalog Compute Marketplace",
    ),
)
class CataLogComputeMarketplaceDelAPI(generics.DestroyAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )

    def get_queryset(self):
        return CatalogComputeMarketplace.objects.order_by("-id")

    def delete(self, request, *args, **kwargs):
        super(CataLogComputeMarketplaceDelAPI, self).delete(request, *args, **kwargs)
        return Response({"status": "success"}, status=200)


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update Catalog Compute Marketplace",
    ),
)
class CataLogComputeMarketplaceUpdateAPI(generics.UpdateAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_change,
    )
    redirect_kwarg = "pk"
    queryset = CatalogComputeMarketplace.objects.all()

    def patch(self, request, *args, **kwargs):
        return super(CataLogComputeMarketplaceUpdateAPI, self).patch(
            request, *args, **kwargs
        )

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(CataLogComputeMarketplaceUpdateAPI, self).put(
            request, *args, **kwargs
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Create Catalog Compute Marketplace",
    ),
)
class CataLogComputeMarketplaceCreateAPI(generics.CreateAPIView):
    serializer_class = CatalogComputeMarketplaceSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_create,
    )
    queryset = CatalogComputeMarketplace.objects.all()

    def post(self, request, *args, **kwargs):
        return super(CataLogComputeMarketplaceCreateAPI, self).post(
            request, *args, **kwargs
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Docker Kubernetes Status"],
        operation_summary="Check status docker, kubernetes status",
        operation_description="""
    Check status docker, kubernetes status
    Use the following cURL command:
    ```bash
    curl {host}/api/ml/docker?ml_id={{ml_id}}&action={{action}} -H 'Authorization: Token abc123'
    """.format(
            host=(settings.HOSTNAME or "https://localhost:8080")
        ),
        manual_parameters=[
            openapi.Parameter(
                name="ip_address",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="ip_address",
            ),
            openapi.Parameter(
                name="type",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description='type "docker" | "kubernetes"',
            ),
        ],
    ),
)
class ComputeDockerKubernetesAPI(generics.RetrieveAPIView):
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        POST=all_permissions.projects_change,
    )
    serializer_class = ComputeMarketplaceSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        ip_address = self.request.query_params.get("ip_address")
        service_type = self.request.query_params.get("type")
        port = 4243 if service_type == "docker" else 6443

        try:
            if not checkDockerKubernetesStatus(ip_address=ip_address, port=port):
                raise Exception("Service check failed")
            return Response(True, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                "An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class ComputeGPUCreateAPI(generics.CreateAPIView):
#     queryset = ComputeGPU.objects.all()

# class ComputeGPUListAPI(generics.ListAPIView):
#     queryset = ComputeGPU.objects.all()
#     serializer_class = ComputeGPUSerializer

# class ComputeGPURetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ComputeGPU.objects.all()
#     serializer_class = ComputeGPUSerializer

# class ComputeGPUBulkCreateAPI(generics.CreateAPIView):
#     serializer_class = ComputeGPUSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Create Compute Time Working",
    ),
)
class ComputeTimeWorkingCreateAPI(generics.CreateAPIView):
    queryset = ComputeTimeWorking.objects.all()
    serializer_class = ComputeTimeWorkingSerializer

    def post(self, request, *args, **kwargs):
        compute_id = request.data.get('compute_id')
        infrastructure_id = request.data.get('infrastructure_id')
        time_start = request.data.get('time_start')
        time_end = request.data.get('time_end')

        if datetime.strptime(time_start, "%H:%M:%S") > datetime.strptime(time_end, "%H:%M:%S"):
            return Response({"message":"Please re-set availability for your computes"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if ComputeTimeWorking instance already exists with given compute_id and infrastructure_id
        compute_time_working_instance = ComputeTimeWorking.objects.filter(
            compute_id=compute_id,
            deleted_at__isnull = True
        ).first()

        if compute_time_working_instance:
            # If instance exists, update it
            serializer = self.get_serializer(
                compute_time_working_instance, data=request.data
            )
        else:
            # If instance doesn't exist, create a new one
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Check if day_range exists and update ComputeMarketplace status accordingly
        if "day_range" in request.data and len(request.data["day_range"]) > 0:
            # Update status compute marketplace to in_marketplace
            if ComputeGpuPrice.objects.filter(
                compute_marketplace_id=request.data["compute_id"]
            ).exists():
                compute = ComputeMarketplace.objects.filter(
                    id=request.data["compute_id"]
                ).first()
                if compute:
                    compute.status = "in_marketplace"
                    compute.save()
        return Response(
            {
                "message": "ComputeTimeWorking created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get detail Compute Time Working",
    ),
)
class ComputeTimeWorkingDetailAPI(generics.RetrieveAPIView):
    serializer_class = ComputeTimeWorkingSerializer
    queryset = ComputeTimeWorking.objects.all()
    lookup_field = "compute_id"

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            return queryset.get(**filter_kwargs)
        except queryset.model.MultipleObjectsReturned:
            # Handle the case where multiple objects are returned
            return queryset.filter(**filter_kwargs).first()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update Compute Time Working",
    ),
)
class ComputeTimeWorkingUpdateAPI(generics.UpdateAPIView):
    serializer_class = ComputeTimeWorkingSerializer
    queryset = ComputeTimeWorking.objects.all()
    lookup_field = "compute_id"

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {
            self.lookup_field: self.kwargs[self.lookup_field],
            # "deleted_at__isnull": True,
        }
        objects = queryset.filter(**filter_kwargs)
        if objects.exists():
            return objects.first() 
        else:
            return ComputeTimeWorking.objects.create(**filter_kwargs)

    def update(self, request, *args, **kwargs):
        time_start = request.data.get('time_start')
        time_end = request.data.get('time_end')

        if datetime.strptime(time_start, "%H:%M:%S") > datetime.strptime(time_end, "%H:%M:%S"):
            return Response({"message":"Please re-set availability for your computes"}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if "day_range" in request.data and len(request.data["day_range"]) > 0:
            # Update status compute marketplace to in_marketplace
            if ComputeGpuPrice.objects.filter(
                compute_marketplace_id=request.data["compute_id"]
            ).exists():
                compute = ComputeMarketplace.objects.filter(
                    id=request.data["compute_id"]
                ).first()
                if compute and compute.status != "rented_bought":
                    compute_gpu = ComputeGPU.objects.filter(compute_marketplace_id=compute.id, deleted_at__isnull=True, status="created")
                    compute_gpu.update(status="in_marketplace")
                    compute.status = "in_marketplace"
                    compute.save()
        else:
            # Reset status compute marketplace to created
            compute = ComputeMarketplace.objects.filter(
                id=request.data["compute_id"]
            ).first()
            if compute and compute.status != "rented_bought":
                compute_gpu = ComputeGPU.objects.filter(
                    compute_marketplace_id=compute.id,
                    deleted_at__isnull=True,
                    status="created",
                )
                compute_gpu.update(status="in_marketplace")
                compute.status = "in_marketplace"
                compute.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get detail Compute History Renting",
    ),
)
class HistoryRentComputeAPI(generics.ListCreateAPIView):
    serializer_class = HistoryRentComputeSerializer
    pagination_class = SetPagination

    def get_queryset(self):
        user = self.request.user
        return History_Rent_Computes.objects.filter(account=user).order_by("-id")

    def get(self, request, *args, **kwargs):
        return super(HistoryRentComputeAPI, self).get(request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get detail Compute Preference",
    ),
)
# @method_decorator(name='post', decorator=swagger_auto_schema(
#     tags=['Compute Marketplace'],
#     operation_summary='Create detail Compute Preference',
# ))


class ComputesPreferenceAPI(generics.RetrieveAPIView):
    serializer_class = ComputesPreferenceSerializer
    queryset = Computes_Preference.objects.all()
    lookup_field = "id"  # Sử dụng 'user_id' thay vì 'id'

    def get_queryset(self):
        user_id = self.kwargs["id"]
        return self.queryset.filter(user_id=user_id, deleted_at__isnull=True).order_by(
            "-id"
        )

    def get(self, request, *args, **kwargs):
        instance = self.get_queryset().first()  # Lấy đối tượng đầu tiên từ queryset
        if instance:
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update detail Compute Preference",
        # manual_parameters=[
        #     openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='computes_preference_id')
        # ]
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Delete detail Compute Preference",
        # manual_parameters=[
        #     openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='computes_preference_id')
        # ]
    ),
)
class ComputesPreferenceUpdateAPI(generics.ListCreateAPIView):
    serializer_class = ComputesPreferenceSerializer

    def patch(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        try:
            instance = Computes_Preference.objects.get(id=id)
        except Computes_Preference.DoesNotExist:
            return Response(
                {"error": "Computes Preference not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        try:
            instances = Computes_Preference.objects.filter(user_id=id)
            for instance in instances:
                instance.deleted_at = timezone.now()
                instance.save()
        except Computes_Preference.DoesNotExist:
            return Response(
                {"error": "Computes Preference not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({"message": "Delete completed"}, status=status.HTTP_200_OK)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Auto find and merge card",
        manual_parameters=[
            #     openapi.Parameter('project_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='project id'),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="user id",
            ),
        ],
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Auto find and merge card",
        # manual_parameters=[
        #     openapi.Parameter('project_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='project id'),
        # openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='user id'),
        # ]
    ),
)
class AutoMergeCardAPI(generics.ListCreateAPIView):
    serializer_class = AutoMergeCardSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Create compute preferency complete"}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):

        return Response(
            {"message": "Auto provision is running"}, status=status.HTTP_200_OK
        )

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get status message install vast",
        operation_description="Get status message install vast",
    ),
)
class ComputeStatusInstalling(generics.ListAPIView):
    
    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs["id"]
            instance = ComputeMarketplace.objects.filter(id=id).first()
            if instance.type == "MODEL-PROVIDER-VAST":
                contract_id = instance.infrastructure_id
                # response = vast_service.get_instance_info(contract_id)
                response = vast_provider.info_compute(contract_id)
                if response['instances']:
                    return Response({"message": response['instances']['status_msg']}, status=200)
                else:
                    return Response({"message": "Not availeble"}, status=200)
            else:
                return Response({"message": "There are nothing"}, status=200)
        except Exception as e:
            return Response({"message": "There are nothing"}, status=500)


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update service type compute ",
        operation_description="Update service type compute ",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "service_type": openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="service type: full, storage, model-training, label-tool",
                ),
            },
        )
 
    )
)
class ChangeServiceTypeComputeRented(generics.UpdateAPIView):
    serializer_class = HistoryRentComputeSerializer

    def get_queryset(self):
        return History_Rent_Computes.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        type = request.data.get('service_type')  
        data['service_type'] = type
        data["compute_install"] = History_Rent_Computes.InstallStatus.INSTALLING
        compute_marketplace = instance.compute_marketplace
        user_id = self.request.user.id
        compute_vast_id = compute_marketplace.infrastructure_desc
        def install_vast(compute_vast_id, type, user_id):
            # delete compute vast
            # vast_service.delete_instance_info(compute_marketplace.infrastructure_id)
            vast_provider.delete_compute(compute_marketplace.infrastructure_id)

            # install
            if type == 'model-training':
                # status_install, response = vast_service.func_install_compute_vastai(compute_vast_id, "aixblock/template_ml-mnist:latest", 'ml', user_id)
                status_install, response = vast_provider.func_install_compute_vastai(compute_vast_id, "aixblock/template_ml-mnist:latest", 'ml', user_id)
                port_tem = 9090
            elif type =="storage":
                # status_install, response = vast_service.func_install_compute_vastai(compute_vast_id, "quay.io/minio/minio:latest", 'storage', user_id)
                status_install, response = vast_provider.func_install_compute_vastai(compute_vast_id, "quay.io/minio/minio:latest", 'storage', user_id)
                port_tem = 9001
            else:
                image_detail = InstallationService.objects.filter(
                    environment=ENVIRONMENT, image=AIXBLOCK_IMAGE_NAME, deleted_at__isnull=True
                    ).first()
                image_platform = AIXBLOCK_IMAGE_NAME + ":latest"
                if image_detail is not None: 
                    image_platform = str(image_detail.image) + ":" + str(image_detail.version)

                # status_install, response = vast_service.func_install_compute_vastai(compute_vast_id, image_platform, "full", user_id)
                status_install, response = vast_provider.func_install_compute_vastai(compute_vast_id, image_platform, "full", user_id)
                port_tem = 8081

            if not status_install:
                History_Rent_Computes.objects.filter(compute_marketplace__infrastructure_id=response,
                                                     compute_marketplace__deleted_at__isnull=True,
                                                     deleted_at__isnull = True, deleted_by__isnull = True).update(compute_install="failed")
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
                    organization_id=self.request.user.active_organization_id,
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

            compute = ComputeMarketplace.objects.filter(infrastructure_id=response['instances']['id'], deleted_at__isnull=True).update(
                name=response['instances']['public_ipaddr'],
                organization_id=self.request.user.active_organization_id,
                ip_address=response['instances']['public_ipaddr'],
                port=response['instances']['ports'][f'{port_tem}/tcp'][0]["HostPort"]
            )
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

            History_Rent_Computes.objects.filter(compute_marketplace=compute, deleted_by__isnull = True, deleted_at__isnull = True).update(
                                                    compute_install="completed",
                                                    ip_address=response['instances']['public_ipaddr'],
                                                    port=response['instances']['ports'][f'{port_tem}/tcp'][0]["HostPort"],
                                                    )
        if compute_marketplace.type == ComputeMarketplace.Type.PROVIDERVAST:
            thread = threading.Thread(
                target=install_vast, args=(compute_vast_id, type, user_id)
            )
            thread.start()

        def install_gpu(gpu_id, type, history_id):
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
            if not compute:
                return Exception({"error": "Compute not found"}, status=400)

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
                    {"detail": f"Docker does not run on {compute.ip_address}"},
                    status=400,
                )
            history = History_Rent_Computes.objects.filter(id= history_id).first()
            user = request.user
            token = Token.objects.get(user=user)

            # install docker
            compute_install = "completed"
            try:
                _port , _, _, _, _, _, _, _= dockerContainerPull(
                    type,
                    compute.ip_address,
                    compute.client_id,
                    compute.client_secret,
                    token,
                    user_id=user_id,
                    gpu_id=gpu_id,
                    gpu_index=compute_gpu.gpu_index,
                    history_id=history_id
                )
                compute.port = f"{_port}"
                compute.save()
                history.port = _port
                history.compute_install = compute_install
                history.save()
            except Exception as e:
                compute_install = "failed"
                history.compute_install = compute_install
                history.save()

            compute_gpu_id = gpu_id

            compute_gpu = ComputeGPU.objects.filter(id=compute_gpu_id).first()
            if compute_gpu:

                # update status install compute
                history.compute_install = compute_install
                history.save()

            else:
                return Response({"detail": "Compute GPU not found"}, status=404)
            # compute_gpu_in_marketplace = ComputeGPU.objects.filter(
            #     status="in_marketplace", compute_marketplace_id=compute.id
            # ).first()
            #  change status compute marketplace to 'rented_bought' if all compute has been rented
            # if compute_gpu_in_marketplace is None:
            #     compute.status = "rented_bought"
            #     compute.save()
            return

        if compute_marketplace.type in [ComputeMarketplace.Type.MODELCUSTOMER, ComputeMarketplace.Type.MODELSYSTEM]:
            thread = threading.Thread(
                target=install_gpu,
                args=(instance.compute_gpu_id, type, instance.id),
            )
            thread.start()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class DownloadFileView(generics.RetrieveAPIView):
    @swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="download file compute verify",
        manual_parameters=[
            openapi.Parameter(
                name="token_worker",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_PATH,
                description="A unique string value identifying the token.",
            ),
        ],
        responses={
            200: openapi.Response(description="File download succeeded."),
            404: openapi.Response(description="File not found."),
        },
    )
    def get(self, request, token_worker):
        base_dir = settings.BASE_DIR
        original_file_path = os.path.join(base_dir, "static/computes/aixblock_computes_verification-linux")
        new_file_name = f"aixblock_computes_verification-linux__{token_worker}"

        if os.path.exists(original_file_path):
            response = FileResponse(open(original_file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{new_file_name}"'
            return response
        else:
            raise Http404("File not found")


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="create compute selfhost wait verify",
        operation_description="create compute selfhost wait verify",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "infrastructure_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="infrastructure_id",
                ),
                "client_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="client_id",
                ),
                "client_secret": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="client_secret",
                ),
            },
        ),
    ),
)

class CreateComputeSelfhostWaitVerifyView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        # user_id = self.request.query_params.get('user_id')
        user_id = self.request.user.id
        try:
            user_uuid = self.request.user.uuid
        except:
            user_uuid = None

        infrastructure_id = self.request.data.get("infrastructure_id")
        client_id = self.request.data.get("client_id")
        client_secret = self.request.data.get("client_secret")

        token = Token.objects.filter(user=self.request.user).first().key
        if "Origin" in self.request.headers and self.request.headers["Origin"]:
            host_name = self.request.headers["Origin"]
        elif "Host" in self.request.headers:
            host_name = self.request.headers["Host"]
        else:
            host_name = "https://app.aixblock.io/"

        if "http" not in host_name:
            try:
                cheme = request.scheme
                host_name = f'{cheme}://{host_name}'
            except:
                host_name = "https://app.aixblock.io/"

        # create compute with infrastructure_id
        compute = ComputeMarketplace.objects.filter(
            infrastructure_id = infrastructure_id,
            deleted_at__isnull = True
        ).first()

        if not compute:
            compute = ComputeMarketplace.objects.create(
                infrastructure_id=infrastructure_id,
                owner_id=user_id,
                author_id=user_id,
                client_id=client_id,
                client_secret=client_secret,
                organization_id=self.request.user.active_organization_id,
                config = {},
                type=ComputeMarketplace.Type.COMPUTE_SELF_HOST,
            )

        compute_history_rent = History_Rent_Computes.objects.filter(
            compute_marketplace_id=compute.id,
            deleted_at__isnull=True,
            compute_install=History_Rent_Computes.InstallStatus.WAIT_VERIFY,
        ).first()
        if not compute_history_rent:
            compute_history_rent = History_Rent_Computes.objects.create(
                account_id=user_id,
                compute_marketplace_id=compute.id,
                status="renting",
                compute_install=History_Rent_Computes.InstallStatus.WAIT_VERIFY,
                type = History_Rent_Computes.Type.OWN_NOT_LEASING
            )

        # Start an event loop to handle the subscription and message receiving
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(
        #     handle_centrifuge_verify_compute(user_id, infrastructure_id)
        # )
        from .functions import ThreadManager
        thread_manager = ThreadManager()

        if not user_uuid:
            thread_name = f"{user_id}-{infrastructure_id}"
            thread_manager.start_thread(lambda: run_event_loop_in_thread(user_id, infrastructure_id, host_name, token), thread_name)
        else:
            thread_name = f"{user_uuid}-{infrastructure_id}"
            thread_manager.start_thread(lambda: run_event_loop_in_thread(user_uuid, infrastructure_id, host_name, token), thread_name)


        return Response(
            {"message": "create success"}, status=status.HTTP_200_OK
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="check compute selfhost wait verify",
        operation_description="check compute selfhost wait verify",
       
    ),
)

class CheckComputeSelfhostWaitVerifyView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        try:
            user_uuid = self.request.user.uuid
        except:
            user_uuid = None

        token = Token.objects.filter(user=self.request.user).first().key
        if "Origin" in self.request.headers and self.request.headers["Origin"]:
            host_name = self.request.headers["Origin"]
        elif "Host" in self.request.headers:
            host_name = self.request.headers["Host"]
        else:
            host_name = "https://app.aixblock.io/"

        if "http" not in host_name:
            try:
                cheme = request.scheme
                host_name = f'{cheme}://{host_name}'
            except:
                host_name = "https://app.aixblock.io/"

        compute = ComputeMarketplace.objects.filter(
            owner_id=user_id,
            author_id=user_id,
            type=ComputeMarketplace.Type.COMPUTE_SELF_HOST,
            deleted_at__isnull=True,
            history_rent_computes__compute_install=History_Rent_Computes.InstallStatus.WAIT_VERIFY,
            history_rent_computes__deleted_at__isnull=True,
        ).distinct().first()

        if compute:
            # Define a unique thread name based on user_id and compute.infrastructure_id
            thread_name = f"centrifuge_{user_id}_{compute.infrastructure_id}"

            # Check if a thread with the same name is already running
            if not any(thread.name == thread_name for thread in threading.enumerate()):
                # Start the new thread
                if not user_uuid:
                    thread_event_loop = threading.Thread(target=run_event_loop_in_thread, args=(user_id, compute.infrastructure_id, host_name, token), name=thread_name)
                else:
                    thread_event_loop = threading.Thread(target=run_event_loop_in_thread, args=(user_uuid, compute.infrastructure_id, host_name, token), name=thread_name)

                thread_event_loop.start()

            serializer = ComputeMarketplaceSerializer(compute)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "No computes with wait_verify status found"}, status=status.HTTP_404_NOT_FOUND
            )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Get List All Compute Marketplace Rented",
        operation_description="Get List All Compute Marketplace Supply",
        manual_parameters=[
            page_parameter,
            search_parameter,
            field_search_parameter,
            sort_parameter,
            type_parameter,
            
        ],
    ),
)
class ListAllComputeMarketplaceRentedAPI(generics.ListAPIView):
    serializer_class = ComputeMarketplaceRentedCardSerializer
    permission_required = ViewClassPermission(
        GET=all_permissions.annotations_view,
    )
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        rented_records = History_Rent_Computes.objects.filter(
            status="renting", deleted_at__isnull=True,  deleted_by__isnull = True
        ).all()

        rented_records = rented_records.filter(deleted_at__isnull=True, compute_install="wait_verify").select_related("compute_marketplace", "compute_gpu")
        return filterModel(self, rented_records, History_Rent_Computes)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"message": "You do not permission"}, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Create Catalog Compute Marketplace",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "result": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="result",
                ),
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="type",
                ),
                "verify": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="verify",
                ),
            },
        ),
    ),
)
class ProcessSelfHostAPI(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user_uuid = self.request.data.get("uuid")
        result = self.request.data.get("result")
        channel = self.request.data.get("channel")
        type = result.get("type")
        verify = result.get("verify")

        try:
            if type == "IP_ADDRESS":
                ip_address = result["data"]
                computeExisted, typeExisted = _check_compute_verify(ip_address=ip_address)

                try:
                    publish_message(
                        channel=channel,
                        data= {
                        "type": "COMPUTE_EXISTED",
                        "data": f"{computeExisted}",
                        "type_existed": f"{typeExisted}",
                    },
                        prefix=True,
                    )
                    print("Published verification result to the channel.")

                except Exception as e:
                    logging.error("Error during publish: %s", e)

            if type == "SERVER_INFO" and verify == "2":
                config = result.get("data")[0]
                _update_server_info(channel, config)

            if type == "GPU" and verify == 2:
                gpus = result.get('data')
                if gpus[0].get("uuid"):
                    _update_compute_gpus(channel, gpus)  

            if type == "DOCKER" and verify == "2":
                _handle_install_compute(channel)
                try:
                    publish_message(
                        channel=channel,
                        data={"type": "Done", "data": "Successfully installed."},
                        prefix=True,
                    )

                    notify_for_compute(user_uuid, "Success", "Compute installation completed.")

                except Exception as e:
                    logging.error("Error during publish: %s", e)

            if type == "COMPUTE_TYPE" and verify == 2:
                data = result.get("data")
                _handle_service_type(channel, data)
                
            if type == "CUDA" and verify == "2":
                data = result.get("data")
                _handle_cuda(channel, data)

            if type == "Fail":
                try:
                    data = result.get("data")
                    notify_for_compute(user_uuid, "Danger", f"{data}")

                    history = History_Rent_Computes.objects.filter(
                            compute_marketplace__infrastructure_id=channel,
                            deleted_at__isnull=True
                        ).first()

                    update_notify_install(f"Error installing compute: {data}", user_id, f"{data}", history.id, "Install Compute", "danger")

                except Exception as e:
                    logging.error("Error during publish: %s", e)

            return Response({"msg": "Completed installed self-host"})
        
        except Exception as e:
            notify_for_compute(user_uuid, "Danger", f"{e}")
            return Response({"msg": f"{e}"})
@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="check compute docker status",
        operation_description="check compute docker status",
        manual_parameters=[
            
            openapi.Parameter(
                'history_compute_id',
                openapi.IN_QUERY,
                description="ID of the history compute resource",
                type=openapi.TYPE_STRING
            )
        ]
    ),
)
class CheckComputeDockerStatus(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        from .functions import check_compute_run_status
        history_compute_id = request.query_params.get('history_compute_id')
        user_id = request.user.id

        # Your logic here, for example:
        if not history_compute_id:
            return Response(
                {"error": "compute_type and history_compute_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        check_compute_run_status(history_compute_id)
        # Example response using the parameters
        return Response(
            {
                "message": "Checking compute selfhost wait verify",
                "user_id": user_id,
                "history_compute_id": history_compute_id,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="Update compute type and location",
        operation_description="Update compute type and location",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "compute_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID of the compute"
                ),
                "compute_type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of the compute resource"
                ),
                "location_id": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID of the location"
                ),
                "location_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the location"
                ),
                "location_alpha2": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Alpha-2 code of the location"
                ),
            },
            required=["history_id"]
        ),
    ),
)
class UpdateComputeTypeAndLocation(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):

        # Extracting values from the request body
        compute_id = request.data.get('compute_id')
        compute_type = request.data.get('compute_type')
        location_id = request.data.get('location_id')
        location_name = request.data.get('location_name')
        location_alpha2 = request.data.get('location_alpha2')
        user_id = request.user.id



        # Check if compute exists
        compute = ComputeMarketplace.objects.filter(id=compute_id, deleted_at__isnull = True).first()
        if compute is None:
            return Response(
                {"error": "Compute marketplace not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update compute details
        compute.compute_type = compute_type
        compute.location_id = location_id
        compute.location_name = location_name
        compute.location_alpha2 = location_alpha2
        compute.save()

        # Return success response
        return Response(
            {
                "message": "Compute type and location updated successfully",
                "user_id": user_id,
                "compute_id": compute_id,
                "compute_type": compute_type,
                "location_id": location_id,
                "location_name": location_name,
                "location_alpha2": location_alpha2,
            },
            status=status.HTTP_200_OK,
        )

@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        tags=["Compute Marketplace"],
        operation_summary="calculate compute and model",
        operation_description="calculate compute and model: lease_computes_count - lease out compute, rented_compute_count - your compute list, rented_models_count - your rented model list",
    ),
)
class CalculateComputeModel(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        current_time = timezone.now()

        # Filter computes owned by the user and of the specified types
        computes = ComputeMarketplace.objects.filter(
            owner_id=user_id,
            type__in=[
                ComputeMarketplace.Type.MODELCUSTOMER,
                ComputeMarketplace.Type.MODELSYSTEM
            ],
            deleted_at__isnull = True
        )

        # Filter models rented by the user with time_end not yet reached
        rented_models = History_Rent_Model.objects.filter(
            user_id=user_id,
            time_end__gt=current_time,
            deleted_at__isnull = True,
            type = "rent",
            status="renting"
        )

        compute_history = History_Rent_Computes.objects.filter(account_id = user_id, status = 'renting',compute_install='completed',  deleted_at__isnull = True)

        # Calculate counts
        lease_computes_count = computes.count()
        rented_models_count = rented_models.count()
        rented_compute_count = compute_history.count()

        # Prepare the response data
        response_data = {
            "lease_computes_count": lease_computes_count,
            "rented_models_count": rented_models_count,
            "rented_compute_count": rented_compute_count
        }

        return Response(response_data, status=status.HTTP_200_OK)
