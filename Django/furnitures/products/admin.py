from django.contrib import admin
from .models import Product, ProductGallery, Review, ReviewImage


# --- Inline for Product Gallery ---
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


# --- Inline for Review Images ---
class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


# --- Inline for Reviews ---
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    show_change_link = True  # allows clicking into review detail page


# --- Review Admin (with inline review images) ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageInline]
    list_display = ('product', 'user', 'rating', 'created_at')


# --- Product Admin (with gallery + reviews inline) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'created_at')
    inlines = [ProductGalleryInline, ReviewInline]


# --- Register remaining models ---
admin.site.register(ProductGallery)
admin.site.register(ReviewImage)
