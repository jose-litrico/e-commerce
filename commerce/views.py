from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from .models import (
    User, 
    Category, 
    Product, 
    Address,
    Cart, 
    CartItem, 
    Order, 
    OrderItem
)

from .serializers import (
    UserSerializer, 
    CategorySerializer, 
    ProductSerializer,
    AddressSerializer, 
    CartSerializer, 
    CartItemSerializer,
    OrderSerializer, 
    OrderItemSerializer
)

from .services.cart_service import CartService
from .services.order_service import OrderService


class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many=True)
        
        return Response(serializers.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailView(APIView):
    def get(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)


        return Response(serializer.data)

    def put(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        user.delete()

        return Response(
            {"message": "Usuario eliminado"},
            status=status.HTTP_200_OK
        )


class CategoryListCreateView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many=True)

        return Response(serializers.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryDetailView(APIView):
    def get(self, request, category_id: int):
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def put(self, request, category_id: int):
        category = get_object_or_404(Category, pk=category_id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, category_id: int):
        category = get_object_or_404(Category, pk=category_id)
        category.delete()

        return Response(
            {"message": "Categoria eliminada"},
            status=status.HTTP_200_OK
        )


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").filter(is_active=True)

        search = request.query_params.get("search")

        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        category_id = request.query_params.get("category")

        if category_id:
            products = products.filter(category_id=category_id)

        ordering = request.query_params.get("ordering", "-created_at")
        allowed_orderings = ["price", "-price", "name", "-name", "created_at", "-created_at"]

        if ordering in allowed_orderings:
            products = products.order_by(ordering)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductDetailView(APIView):
    def get(self, request, product_id: int):
        product = get_object_or_404(
            Product.objects.select_related("category"),
            pk=product_id
        )

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def put(self, request, product_id: int):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, product_id: int):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()

        return Response(
            {"message": "Producto eliminado"},
            status=status.HTTP_200_OK
        )


class AddressListCreateView(APIView):
    def get(self, request):
        address = Address.objects.select_related("user").all()
        serializers = AddressSerializer(address, many=True)

        return Response(serializers.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AddressDetailView(APIView):
    def get(self, request, address_id: int):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address)

        return Response(serializer.data)

    def put(self, request, address_id: int):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, address_id: int):
        address = get_object_or_404(Address, pk=address_id)
        address.delete()

        return Response(
            {"message": "Direccion eliminada"},
            status=status.HTTP_200_OK
        )


class CartDetailView(APIView):
    def get(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        cart = CartService.get_or_create_cart(user)
        serializer = CartSerializer(cart)

        return Response(serializer.data)


class CartAddItemView(APIView):
    def post(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        try:
            item = CartService.add_item(user, product_id, quantity)
            serializer = CartItemSerializer(item)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )


class CartUpdateItemView(APIView):
    def put(self, request, user_id: int, item_id: int):
        user = get_object_or_404(User, pk=user_id)
        quantity = request.data.get("quantity")

        try:
            item = CartService.update_item_quantity(user, item_id, quantity)
            serializer = CartItemSerializer(item)

            return Response(serializer.data)
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )


class CartRemoveItemView(APIView):
    def delete(self, request, user_id: int, item_id: int):
        user = get_object_or_404(User, pk=user_id)
        try:
            CartService.remove_item(user, item_id)

            return Response(
                {"message": "Item eliminado del carrito"},
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )


class CartClearView(APIView):
    def post(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        CartService.clear_cart(user)

        return Response(
            {"message": "Carrito vaciado"},
            status=status.HTTP_200_OK
        )


class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.select_related(
            "user", "shipping_address"
        ).prefetch_related("items").all()
        serializers = OrderSerializer(orders, many=True)
        return Response(serializers.data)

    def post(self, request):
        user_id = request.data.get("user")
        address_id = request.data.get("shipping_address")

        if not user_id or not address_id:
            return Response(
                {"error": "User y shipping_address son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=user_id)

        try:
            order = OrderService.create_order_from_cart(user, int(address_id))
            serializer = OrderSerializer(order)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderDetailView(APIView):
    def get(self, request, order_id: int):
        order = get_object_or_404(
            Order.objects.select_related(
                "user", "shipping_address"
            ).prefetch_related("items"),
            pk=order_id
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class OrderUpdateStatusView(APIView):
    def post(self, request, order_id: int):
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "El campo status es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = OrderService.update_status(order_id, new_status)
            serializer = OrderSerializer(order)

            return Response(serializer.data)
        except ValidationError as e:
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserOrderHistoryView(APIView):
    def get(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        orders = Order.objects.filter(user=user).select_related(
            "shipping_address"
        ).prefetch_related("items").order_by("-created_at")

        serializers = OrderSerializer(orders, many=True)
        
        return Response(serializers.data)