from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product
from pprint import pprint

def index(request):
    return render(request, 'main/index.html')

def contact(request):
    return render(request,'main/contact.html')


def single(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.gallery.all()
    reviews = product.reviews.prefetch_related('images')

    paginator = Paginator(reviews, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "product": product,
        "images": images,
        "reviews": page_obj.object_list,  # <-- use paginated reviews
        "page_obj": page_obj,
    }

    return render(request, "product/single.html", context)

