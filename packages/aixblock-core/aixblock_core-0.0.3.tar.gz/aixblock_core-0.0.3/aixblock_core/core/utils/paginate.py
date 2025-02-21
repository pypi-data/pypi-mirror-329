from rest_framework.pagination import PageNumberPagination
class SetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 10000