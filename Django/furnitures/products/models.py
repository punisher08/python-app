from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    # Basic product details
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # Blog heading
    blog_heading = models.CharField(max_length=255, blank=True, null=True)

    # Media
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    # Pricing & stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"{self.product.name} - Image"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(default=1)  # 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars"

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="reviews/")

    def __str__(self):
        return f"Image for Review {self.review.id}"