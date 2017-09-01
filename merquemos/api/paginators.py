from rest_framework import pagination

class PageLimitPagination(pagination.PageNumberPagination):
    def get_page_size(self, request):
        return request.GET['limit']
    
