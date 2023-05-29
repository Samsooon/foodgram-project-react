from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    Pagination for users
    """
    page_size_query_param = 'limit'
