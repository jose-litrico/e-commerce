from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from commerce.models import (
    User, Category, Product, Address,
    Cart, CartItem, Order, OrderItem
)
from commerce.services.cart_service import CartService
from commerce.services.order_service import OrderService
from rest_framework.exceptions import ValidationError


# =========================================================
# TESTS DE MODELOS
# =========================================================
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='123456789'
        )

        self.category = Category.objects.create(
            name='Electrónica',
            slug='electronica'
        )

        self.product = Product.objects.create(
            name='Laptop',
            slug='laptop',
            description='Laptop de prueba',
            price=Decimal('999.99'),
            stock=10,
            category=self.category
        )

        self.address = Address.objects.create(
            user=self.user,
            street='Calle 123',
            city='Ciudad',
            state='Estado',
            zip_code='12345',
            country='USA'
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electrónica')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_product_belongs_to_category(self):
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.products.all())

    def test_address_belongs_to_user(self):
        self.assertEqual(self.address.user, self.user)

class CartServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='cartuser',
            email='cart@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(name='Test', slug='test')

        self.product = Product.objects.create(
            name='Mouse',
            slug='mouse',
            description='Mouse gamer',
            price=Decimal('25.00'),
            stock=5,
            category=self.category,
            is_active=True
        )

    def test_get_or_create_cart(self):
        cart = CartService.get_or_create_cart(self.user)
        self.assertIsInstance(cart, Cart)
        self.assertEqual(cart.user, self.user)

        cart2 = CartService.get_or_create_cart(self.user)
        self.assertEqual(cart.id, cart2.id)

    def test_add_item(self):
        item = CartService.add_item(self.user, self.product.id, quantity=2)

        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.cart.user, self.user)

    def test_add_item_increases_quantity(self):
        CartService.add_item(self.user, self.product.id, quantity=1)
        item = CartService.add_item(self.user, self.product.id, quantity=2)

        self.assertEqual(item.quantity, 3)

    def test_add_item_insufficient_stock(self):
        with self.assertRaises(ValidationError):
            CartService.add_item(self.user, self.product.id, quantity=20)

    def test_add_inactive_product(self):
        self.product.is_active = False
        self.product.save()

        with self.assertRaises(ValidationError):
            CartService.add_item(self.user, self.product.id, quantity=1)

    def test_update_item_quantity(self):
        item = CartService.add_item(self.user, self.product.id, quantity=1)
        updated = CartService.update_item_quantity(self.user, item.id, quantity=4)

        self.assertEqual(updated.quantity, 4)

    def test_remove_item(self):
        item = CartService.add_item(self.user, self.product.id, quantity=1)
        CartService.remove_item(self.user, item.id)

        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_clear_cart(self):
        CartService.add_item(self.user, self.product.id, quantity=1)
        CartService.clear_cart(self.user)
        cart = CartService.get_or_create_cart(self.user)

        self.assertEqual(cart.items.count(), 0)

class OrderServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='orderuser',
            email='order@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(name='Test', slug='test-order')

        self.product = Product.objects.create(
            name='Teclado',
            slug='teclado',
            description='Teclado mecánico',
            price=Decimal('50.00'),
            stock=10,
            category=self.category,
            is_active=True
        )

        self.address = Address.objects.create(
            user=self.user,
            street='Av. Principal 100',
            city='Lima',
            state='Lima',
            zip_code='15001',
            country='Perú'
        )

        CartService.add_item(self.user, self.product.id, quantity=2)

    def test_create_order_from_cart(self):
        order = OrderService.create_order_from_cart(self.user, self.address.id)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total, Decimal('100.00'))  # 50 * 2
        self.assertEqual(order.items.count(), 1)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

        cart = CartService.get_or_create_cart(self.user)
        self.assertEqual(cart.items.count(), 0)

    def test_create_order_empty_cart(self):
        CartService.clear_cart(self.user)

        with self.assertRaises(ValidationError):
            OrderService.create_order_from_cart(self.user, self.address.id)

    def test_update_status(self):
        order = OrderService.create_order_from_cart(self.user, self.address.id)
        updated = OrderService.update_status(order.id, 'confirmed')

        self.assertEqual(updated.status, 'confirmed')

    def test_update_status_invalid(self):
        order = OrderService.create_order_from_cart(self.user, self.address.id)

        with self.assertRaises(ValidationError):
            OrderService.update_status(order.id, 'estado_invalido')

class ProductAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Ropa', slug='ropa')

        self.product = Product.objects.create(
            name='Camiseta',
            slug='camiseta',
            description='Camiseta de algodón',
            price=Decimal('15.00'),
            stock=20,
            category=self.category,
            is_active=True
        )

    def test_list_products(self):
        url = reverse('product-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_products(self):
        url = reverse('product-list-create')
        response = self.client.get(url, {'search': 'Camiseta'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_category(self):
        url = reverse('product-list-create')
        response = self.client.get(url, {'category': self.category.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        url = reverse('product-detail', kwargs={'product_id': self.product.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Camiseta')

class CartAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(name='Test', slug='test-api')

        self.product = Product.objects.create(
            name='Auriculares',
            slug='auriculares',
            description='Auriculares bluetooth',
            price=Decimal('30.00'),
            stock=15,
            category=self.category,
            is_active=True
        )

    def test_get_cart(self):
        url = reverse('cart-detail', kwargs={'user_id': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_item_to_cart(self):
        url = reverse('cart-add-item', kwargs={'user_id': self.user.id})
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)

    def test_clear_cart(self):
        # Primero agregar un ítem
        CartService.add_item(self.user, self.product.id, quantity=1)

        url = reverse('cart-clear', kwargs={'user_id': self.user.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cart = CartService.get_or_create_cart(self.user)
        self.assertEqual(cart.items.count(), 0)

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='orderapi',
            email='orderapi@example.com',
            password='testpass123'
        )

        self.category = Category.objects.create(name='Test', slug='test-order-api')

        self.product = Product.objects.create(
            name='Monitor',
            slug='monitor',
            description='Monitor 24 pulgadas',
            price=Decimal('150.00'),
            stock=5,
            category=self.category,
            is_active=True
        )

        self.address = Address.objects.create(
            user=self.user,
            street='Calle Falsa 123',
            city='Ciudad',
            state='Estado',
            zip_code='00000',
            country='USA'
        )

        CartService.add_item(self.user, self.product.id, quantity=1)

    def test_create_order(self):
        url = reverse('order-list-create')
        data = {
            'user': self.user.id,
            'shipping_address': self.address.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(Decimal(response.data['total']), Decimal('150.00'))

    def test_user_order_history(self):
        OrderService.create_order_from_cart(self.user, self.address.id)

        url = reverse('user-order-history', kwargs={'user_id': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_order_status(self):
        order = OrderService.create_order_from_cart(self.user, self.address.id)

        url = reverse('order-update-status', kwargs={'order_id': order.id})
        data = {'status': 'shipped'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'shipped')