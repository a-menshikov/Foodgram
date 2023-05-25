from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомный пагинатор."""
    page_size_query_param = 'limit'
