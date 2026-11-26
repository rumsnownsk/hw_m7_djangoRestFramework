from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size', # кол-во сущностей на странице
    max_page_size = 10