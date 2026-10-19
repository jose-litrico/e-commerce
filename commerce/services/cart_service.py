from django.db import transaction
from rest_framework.exceptions import ValidationError

from ..models import Cart, CartItem, Product, User
from ..validators.common import validate_positive_integer, get_object_or_validation_error


class CartService:

    @staticmethod
    def get_or_create_cart(user: User) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    @transaction.atomic
    def add_item(user: User, product_id: int, quantity: int = 1) -> CartItem:
        quantity = validate_positive_integer(quantity, "quantity")
        product = get_object_or_validation_error(Product, product_id, "product")

        if not product.is_active:
            raise ValidationError({"product": "Este producto no está disponible."})

        if product.stock < quantity:
            raise ValidationError({
                "quantity": f"Stock insuficiente. Solo hay {product.stock} unidades."
            })

        cart = CartService.get_or_create_cart(user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                raise ValidationError({
                    "quantity": f"Stock insuficiente. Solo hay {product.stock} unidades."
                })
            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity", "updated_at"])

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_item_quantity(user: User, item_id: int, quantity: int) -> CartItem:
        quantity = validate_positive_integer(quantity, "quantity")
        cart = CartService.get_or_create_cart(user)

        try:
            cart_item = CartItem.objects.select_related("product").get(
                pk=item_id, cart=cart
            )
        except CartItem.DoesNotExist:
            raise ValidationError({"item": "Ítem del carrito no encontrado."})

        if cart_item.product.stock < quantity:
            raise ValidationError({
                "quantity": f"Stock insuficiente. Solo hay {cart_item.product.stock} unidades."
            })

        cart_item.quantity = quantity
        cart_item.save(update_fields=["quantity", "updated_at"])
        
        return cart_item

    @staticmethod
    def remove_item(user: User, item_id: int):
        cart = CartService.get_or_create_cart(user)
        deleted, _ = CartItem.objects.filter(pk=item_id, cart=cart).delete()

        if not deleted:
            raise ValidationError({"item": "Ítem del carrito no encontrado."})

    @staticmethod
    def clear_cart(user: User):
        cart = CartService.get_or_create_cart(user)
        cart.items.all().delete()

    @staticmethod
    def get_cart_total(cart: Cart):
        total = 0

        for item in cart.items.select_related("product").all():
            total += item.product.price * item.quantity

        return total