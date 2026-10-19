from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    OrderItem,
    Order,
    CartItem,
    Cart,
    Address,
    Product,
    Category,
    User,
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'is_staff', 'is_active', 'date_joined', )

    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', )

    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined', )

    ordering = ('-date_joined', )

    readonly_fields = ('date_joined', 'last_login', )

    fieldsets = (
        (
            None, {
                'fields': (
                    'username',
                    'password',
                ),
            },
        ), (
            'Informacion personal', {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'birth_date',
                ),
            },
        ), (
            'Permisos', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                ),
            },
        ), (
            'Fechas importantes', {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        )
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide', ),
                'fields': ('username', 'email', 'password1', 'password2', 'phone', 'birth_date', ),
            }
        ),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active', 'created_at', )

    list_filter = ('is_active', 'created_at', )

    search_fields = ('name', 'slug', 'description', )

    prepopulated_fields = {'slug': ('name', )}

    ordering = ('name', )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at', 'updated_at', )

    list_filter = ('is_active', 'category', 'created_at', )

    search_fields = ('name', 'slug', 'description', )

    prepopulated_fields = {'slug': ('name', )}

    list_editable = ('price', 'stock', 'is_active', )

    ordering = ('-created_at', )

    raw_id_fields = ('category', )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'street', 'city', 'state', 'zip_code', 'country', 'is_default', 'created_at', )

    list_filter = ('country', 'state', 'is_default', 'created_at', )

    search_fields = ('street', 'city', 'zip_code', 'user__username', 'user__email', )

    ordering = ('-created_at', )

    raw_id_fields = ('user', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', )

    list_filter = ('created_at', 'updated_at', )

    search_fields = ('user__username', 'user__email', )

    ordering = ('-updated_at', )

    raw_id_fields = ('user', )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at', 'updated_at', )

    list_filter = ('created_at', )

    search_fields = ('product__name', 'cart__user__username', )

    ordering = ('-created_at', )

    raw_id_fields = ('cart', 'product', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'shipping_address', 'created_at', 'updated_at', )

    list_filter = ('status', 'created_at', )

    search_fields = ('user__username', 'user__email', 'id', )

    ordering = ('-created_at', )

    raw_id_fields = ('user', 'shipping_address', )

    list_editable = ('status', )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', )

    list_filter = ('order__status', )

    search_fields = ('product__name', 'order__id', 'order__user__username', )

    ordering = ('-id', )

    raw_id_fields = ('order', 'product', )