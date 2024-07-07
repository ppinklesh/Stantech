from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'quantity_sold', 'rating', 'review_count']
    list_filter = ['category', 'price']
    search_fields = ['product_name', 'category']

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_staff', 'is_active']

admin.site.register(User, CustomUserAdmin)
