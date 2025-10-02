from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator

def index(request):
    return render(request,'main/index.html')

def single(request):
    images = [
        {"title": "Wooden Door", "url": "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(73).webp"},
        {"title": "Modern Glass Door", "url": "https://mdbcdn.b-cdn.net/img/Photos/Vertical/mountain1.webp"},
        {"title": "Classic Dining Table", "url": "https://mdbcdn.b-cdn.net/img/Photos/Vertical/mountain2.webp"},
        {"title": "Rustic Wooden Table", "url": "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(73).webp"},
        {"title": "Minimalist Dining Setup", "url": "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(18).webp"},
        {"title": "Antique Door", "url": "https://mdbcdn.b-cdn.net/img/Photos/Vertical/mountain3.webp"},
        {"title": "Luxury Dining Room", "url": "https://mdbcdn.b-cdn.net/img/Photos/Horizontal/Nature/4-col/img%20(73).webp"},
    ]

    # Paginate results (3 per page here)
    paginator = Paginator(images, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "product/single.html", {"page_obj": page_obj})

