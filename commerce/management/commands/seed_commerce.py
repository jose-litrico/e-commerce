from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from commerce.models import Category, Product, Address, Cart

User = get_user_model()


class Command(BaseCommand):
    help = "Carga usuarios, categorías, productos y direcciones de ejemplo"

    def handle(self, *args, **options):
        self.stdout.write("Sembrando datos de MiTienda...\n")

        users = self._seed_users()
        categories = self._seed_categories()
        self._seed_products(categories)
        self._seed_addresses(users)
        self._seed_carts(users)

        self.stdout.write(self.style.SUCCESS("\n✓ Seed completado"))
        self.stdout.write(
            f"  Usuario de prueba: juanperez (id={users['juan'].id}) / password: juan123"
        )
        self.stdout.write(
            f"  En appController usa: loadCurrentUser({users['juan'].id})"
        )

    def _seed_users(self):
        data = [
            {
                "key": "admin",
                "username": "admin",
                "email": "admin@mitienda.com",
                "first_name": "Admin",
                "last_name": "Sistema",
                "phone": "555-0001",
                "password": "admin123",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "key": "juan",
                "username": "juanperez",
                "email": "juan@email.com",
                "first_name": "Juan",
                "last_name": "Pérez",
                "phone": "555-0102",
                "password": "juan123",
            },
            {
                "key": "ana",
                "username": "anagarcia",
                "email": "ana@email.com",
                "first_name": "Ana",
                "last_name": "García",
                "phone": "555-0103",
                "password": "ana123",
            },
            {
                "key": "luis",
                "username": "luismartinez",
                "email": "luis@email.com",
                "first_name": "Luis",
                "last_name": "Martínez",
                "phone": "555-0104",
                "password": "luis123",
            },
        ]

        users = {}
        for item in data:
            key = item.pop("key")
            password = item.pop("password")
            defaults = {k: v for k, v in item.items() if k != "username"}

            user, created = User.objects.get_or_create(
                username=item["username"],
                defaults=defaults,
            )
            if created or not user.has_usable_password():
                user.set_password(password)
                user.save()

            users[key] = user
            status = "creado" if created else "ya existía"
            self.stdout.write(f"  Usuario {user.username} (id={user.id}) — {status}")

        return users

    def _seed_categories(self):
        data = [
            ("Electrónica", "electronica", "Celulares, audio, computación y gadgets"),
            ("Ropa", "ropa", "Moda, calzado y accesorios"),
            ("Hogar", "hogar", "Decoración, cocina y organización"),
            ("Deportes", "deportes", "Fitness, outdoor y equipo deportivo"),
            ("Libros", "libros", "Ficción, no ficción y educativos"),
            ("Juguetes", "juguetes", "Juegos, construcción y entretenimiento"),
            ("Belleza", "belleza", "Cuidado personal y cosméticos"),
            ("Alimentos", "alimentos", "Snacks, bebidas y despensa"),
        ]

        categories = {}
        for name, slug, description in data:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": description,
                    "is_active": True,
                },
            )
            categories[slug] = cat
            status = "creada" if created else "ya existía"
            self.stdout.write(f"  Categoría {name} — {status}")

        return categories

    def _seed_products(self, categories):
        # (name, slug, description, price, stock, category_slug)
        data = [
            # Electrónica
            ("Auriculares Bluetooth Pro", "auriculares-bluetooth-pro",
             "Cancelación de ruido, 30 h de batería y micrófono integrado.", "59.99", 30, "electronica"),
            ("Teclado Mecánico RGB", "teclado-mecanico-rgb",
             "Switches red, retroiluminación RGB y reposamuñecas.", "79.99", 18, "electronica"),
            ("Mouse Gamer 16000 DPI", "mouse-gamer-16000",
             "Sensor óptico de alta precisión y 8 botones programables.", "34.50", 40, "electronica"),
            ("Monitor 24\" Full HD 75Hz", "monitor-24-full-hd",
             "Panel IPS, HDMI y VGA. Ideal para oficina y gaming casual.", "129.99", 12, "electronica"),
            ("Power Bank 20000 mAh", "power-bank-20000",
             "Carga rápida USB-C y dos puertos USB-A.", "29.99", 45, "electronica"),
            ("Webcam Full HD", "webcam-full-hd",
             "1080p, micrófono dual y clip universal.", "39.99", 22, "electronica"),

            # Ropa
            ("Camiseta Básica Algodón", "camiseta-basica-algodon",
             "100% algodón, corte regular. Varios colores.", "14.99", 60, "ropa"),
            ("Jeans Slim Fit", "jeans-slim-fit",
             "Denim elástico, corte slim y lavado medio.", "39.99", 28, "ropa"),
            ("Sudadera con Capucha", "sudadera-capucha",
             "Felpa suave, bolsillo canguro y cordón ajustable.", "32.99", 35, "ropa"),
            ("Mochila Urbana Laptop", "mochila-urbana-laptop",
             "Compartimento para laptop 15\", resistente al agua.", "44.99", 20, "ropa"),
            ("Gorra Clásica", "gorra-clasica",
             "Ajustable, bordado frontal y visera curva.", "12.99", 50, "ropa"),

            # Hogar
            ("Lámpara de Escritorio LED", "lampara-escritorio-led",
             "3 temperaturas de color, brazo flexible y puerto USB.", "24.99", 32, "hogar"),
            ("Set Sábanas Queen", "set-sabanas-queen",
             "Microfibra suave, incluye fundas de almohada.", "34.99", 15, "hogar"),
            ("Botella Térmica 750 ml", "botella-termica-750",
             "Acero inoxidable. Frío 24 h / caliente 12 h.", "18.99", 55, "hogar"),
            ("Organizador de Escritorio", "organizador-escritorio",
             "Bambú, 5 compartimentos para útiles y cables.", "16.50", 25, "hogar"),
            ("Difusor de Aromas", "difusor-aromas",
             "Ultrasónico, luz LED y apagado automático.", "27.99", 18, "hogar"),

            # Deportes
            ("Zapatillas Running", "zapatillas-running",
             "Amortiguación ligera, malla transpirable.", "89.99", 16, "deportes"),
            ("Colchoneta Yoga 6 mm", "colchoneta-yoga-6mm",
             "Antideslizante, incluye correa de transporte.", "22.50", 30, "deportes"),
            ("Pelota de Fútbol N°5", "pelota-futbol-n5",
             "Cosida a máquina, cámara de butilo.", "19.99", 24, "deportes"),
            ("Botella Deportiva 1 L", "botella-deportiva-1l",
             "Libre de BPA, tapa antiderrame.", "11.99", 40, "deportes"),
            ("Bandas Elásticas Set x5", "bandas-elasticas-set",
             "5 resistencias, ideal para entrenamiento en casa.", "15.99", 35, "deportes"),

            # Libros
            ("Cien años de soledad", "cien-anos-de-soledad",
             "Gabriel García Márquez. Edición de bolsillo.", "16.50", 20, "libros"),
            ("El Principito", "el-principito",
             "Antoine de Saint-Exupéry. Edición ilustrada.", "12.99", 35, "libros"),
            ("Sapiens", "sapiens-harari",
             "Yuval Noah Harari. Historia de la humanidad.", "21.99", 14, "libros"),
            ("El Quijote", "el-quijote",
             "Miguel de Cervantes. Edición completa.", "18.50", 10, "libros"),

            # Juguetes
            ("Lego Classic 500 piezas", "lego-classic-500",
             "Set creativo con bases y bloques de colores.", "44.99", 12, "juguetes"),
            ("Puzzle 1000 piezas", "puzzle-1000-piezas",
             "Paisaje montaña. Incluye poster de referencia.", "17.99", 18, "juguetes"),
            ("Set de Arte Infantil", "set-arte-infantil",
             "Crayones, acuarelas y block de dibujo.", "13.99", 22, "juguetes"),

            # Belleza
            ("Crema Hidratante Facial", "crema-hidratante-facial",
             "Para todo tipo de piel, 50 ml.", "19.99", 28, "belleza"),
            ("Kit Brochas Maquillaje", "kit-brochas-maquillaje",
             "12 piezas con estuche de viaje.", "24.50", 16, "belleza"),

            # Alimentos
            ("Café Molido 500 g", "cafe-molido-500g",
             "Tueste medio, origen Colombia.", "9.99", 40, "alimentos"),
            ("Chocolate Amargo 70%", "chocolate-amargo-70",
             "Tableta 100 g, sin azúcar añadida.", "4.50", 60, "alimentos"),
            ("Mix de Frutos Secos 250 g", "mix-frutos-secos-250",
             "Almendras, nueces y pasas.", "6.99", 35, "alimentos"),
        ]

        created = 0
        for name, slug, description, price, stock, cat_slug in data:
            _, was_created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "description": description,
                    "price": Decimal(price),
                    "stock": stock,
                    "category": categories[cat_slug],
                    "is_active": True,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(f"  Productos: {created} nuevos, {len(data)} en total definidos")

    def _seed_addresses(self, users):
        addresses = [
            (users["juan"], "Av. Reforma 123", "Ciudad de México", "CDMX", "06600", "México", "555-0102"),
            (users["juan"], "Calle Secundaria 45", "Ciudad de México", "CDMX", "03100", "México", "555-0102"),
            (users["ana"], "Av. Vallarta 500", "Guadalajara", "Jalisco", "44100", "México", "555-0103"),
            (users["luis"], "Calle 50 #120", "Mérida", "Yucatán", "97000", "México", "555-0104"),
        ]

        for i, (user, street, city, state, zip_code, country, phone) in enumerate(addresses):
            Address.objects.get_or_create(
                user=user,
                street=street,
                defaults={
                    "city": city,
                    "state": state,
                    "zip_code": zip_code,
                    "country": country,
                    "phone": phone,
                    "is_default": i == 0 or street.startswith("Av. Vallarta") or street.startswith("Calle 50"),
                },
            )

        self.stdout.write(f"  Direcciones: {len(addresses)}")

    def _seed_carts(self, users):
        for user in users.values():
            Cart.objects.get_or_create(user=user)
        self.stdout.write(f"  Carritos: {len(users)}")