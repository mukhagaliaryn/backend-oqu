from django.http import JsonResponse
from .models import Subcategory


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(own_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)
