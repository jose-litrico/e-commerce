from django.db import transaction
from rest_framework.exceptions import ValidationError
from decimal import Decimal

from ..models import Order, OrderItem, Address, User
from ..services.cart_service import CartService
from ..validators.common import get_object_or_validation_error


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user: User, address_id: int) -> Order:
        cart = CartService.get_or_create_cart(user)
        items = list(cart.items.select_related("product").all())

        if not items:
            raise ValidationError({"cart": "El carrito está vacío."})

        address = get_object_or_validation_error(Address, address_id, "shipping_address")

        if address.user_id != user.id:
            raise ValidationError({"shipping_address": "La dirección no pertenece al usuario."})

        for item in items:
            if not item.product.is_active:
                raise ValidationError({
                    "product": f"El producto '{item.product.name}' ya no está disponible."
                })
            if item.product.stock < item.quantity:
                raise ValidationError({
                    "stock": f"Stock insuficiente para '{item.product.name}'. "
                             f"Disponible: {item.product.stock}"
                })

        total = Decimal("0.00")
        for item in items:
            total += item.product.price * item.quantity

        order = Order.objects.create(
            user=user,
            shipping_address=address,
            total=total,
            status="pending"
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])

        cart.items.all().delete()
        
        return order

    @staticmethod
    @transaction.atomic
    def update_status(order_id: int, new_status: str) -> Order:
        valid_statuses = dict(Order.STATUS_CHOICES).keys()

        if new_status not in valid_statuses:
            raise ValidationError({
                "status": f"Estado inválido. Opciones: {', '.join(valid_statuses)}"
            })

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise ValidationError({"order": "Pedido no encontrado."})

        order.status = new_status
        order.save(update_fields=["status", "updated_at"])

        return order