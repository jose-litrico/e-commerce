import { ORDER_STATUS_LABELS } from "../constants/constants.js";
import { getFilteredProducts, getCartCount, getCartTotal } from "../state/state.js";

function formatPrice(value) {
    const num = Number(value) || 0;
    return new Intl.NumberFormat("es-MX", {
        style: "currency",
        currency: "USD",
    }).format(num);
}

export function renderCartCount(count) {
    const el = document.getElementById("cart-count");
    if (el) {
        el.textContent = String(count ?? getCartCount());
    }
}

/**
 * @param {Array} categories
 */
export function renderCategories(categories = []) {
    const list = document.getElementById("category-list");
    if (!list) return;

    const allItem = `
        <li class="category-nav__item">
            <a href="#"
               class="category-nav__link category-nav__link--active"
               data-category="all"
               id="category-all">
                Todos
            </a>
        </li>
    `;

    const items = categories
        .filter((c) => c.is_active !== false)
        .map(
            (c) => `
        <li class="category-nav__item">
            <a href="#"
               class="category-nav__link"
               data-category="${c.id}"
               id="category-${c.id}">
                ${c.name}
            </a>
        </li>
    `
        )
        .join("");

    list.innerHTML = allItem + items;
}

/**
 * @param {string|number|null} categoryId
 */
export function setActiveCategory(categoryId) {
    const links = document.querySelectorAll(".category-nav__link");
    links.forEach((link) => {
        const value = link.dataset.category;
        const isActive =
            categoryId == null || categoryId === "all"
                ? value === "all"
                : String(value) === String(categoryId);
        link.classList.toggle("category-nav__link--active", isActive);
    });
}

/**
 * @param {Array} [products] 
 */
export function renderProducts(products) {
    const grid = document.getElementById("product-grid");
    if (!grid) return;

    const list = products ?? getFilteredProducts();

    if (!list.length) {
        grid.innerHTML = `
            <p id="no-products" class="products__empty">
                No hay productos disponibles.
            </p>
        `;
        return;
    }

    grid.innerHTML = list
        .map((product) => {
            const categoryName =
                product.category?.name ??
                product.category_name ??
                "";
            const imageUrl = product.image || "/static/images/placeholder.png";
            const outOfStock = product.stock <= 0;

            return `
            <article class="product-card ${outOfStock ? "product-card--out-of-stock" : ""}"
                     data-product-id="${product.id}">
                <a href="#" class="product-card__link" data-product-detail="${product.id}">
                    <div class="product-card__image-wrapper">
                        <img
                            src="${imageUrl}"
                            alt="${product.name}"
                            class="product-card__image"
                            id="product-image-${product.id}"
                        >
                    </div>
                    <div class="product-card__body">
                        <h3 class="product-card__name" id="product-name-${product.id}">
                            ${product.name}
                        </h3>
                        <p class="product-card__category">${categoryName}</p>
                        <p class="product-card__price" id="product-price-${product.id}">
                            ${formatPrice(product.price)}
                        </p>
                        <p class="product-card__stock">
                            ${outOfStock ? "Agotado" : `Stock: ${product.stock}`}
                        </p>
                    </div>
                </a>
                <button
                    type="button"
                    class="product-card__add-btn"
                    id="add-to-cart-${product.id}"
                    data-product-id="${product.id}"
                    ${outOfStock ? "disabled" : ""}
                >
                    ${outOfStock ? "Sin stock" : "Agregar al carrito"}
                </button>
            </article>
        `;
        })
        .join("");
}

/**
 * @param {Array} items
 */
export function renderCart(items = []) {
    const container = document.getElementById("cart-items");
    if (!container) return;

    if (!items.length) {
        container.innerHTML = `
            <p id="cart-empty" class="cart__empty">Tu carrito está vacío.</p>
        `;
        renderCartCount(0);
        const totalEl = document.getElementById("cart-total");
        if (totalEl) totalEl.textContent = formatPrice(0);
        return;
    }

    container.innerHTML = items
        .map((item) => {
            const product = item.product ?? item;
            const name = product.name ?? "Producto";
            const price = product.price ?? item.price ?? 0;
            const quantity = item.quantity ?? 1;
            const subtotal = price * quantity;

            return `
            <div class="cart-item" data-item-id="${item.id}" data-product-id="${product.id ?? item.product_id}">
                <div class="cart-item__info">
                    <h3 class="cart-item__name">${name}</h3>
                    <p class="cart-item__price">${formatPrice(price)} c/u</p>
                </div>
                <div class="cart-item__controls">
                    <button type="button"
                            class="cart-item__qty-btn"
                            data-action="decrease"
                            data-item-id="${item.id}">−</button>
                    <span class="cart-item__qty" id="cart-qty-${item.id}">${quantity}</span>
                    <button type="button"
                            class="cart-item__qty-btn"
                            data-action="increase"
                            data-item-id="${item.id}">+</button>
                </div>
                <p class="cart-item__subtotal">${formatPrice(subtotal)}</p>
                <button type="button"
                        class="cart-item__remove"
                        data-action="remove"
                        data-item-id="${item.id}"
                        aria-label="Eliminar">
                    ✕
                </button>
            </div>
        `;
        })
        .join("");

    renderCartCount(items.reduce((s, i) => s + (i.quantity || 0), 0));

    const totalEl = document.getElementById("cart-total");
    if (totalEl) {
        const total = items.reduce((s, i) => {
            const p = i.product?.price ?? i.price ?? 0;
            return s + p * (i.quantity || 0);
        }, 0);
        totalEl.textContent = formatPrice(total);
    }
}

/**
 * @param {Array} orders
 */
export function renderOrders(orders = []) {
    const container = document.getElementById("orders-list");
    if (!container) return;

    if (!orders.length) {
        container.innerHTML = `
            <p id="orders-empty" class="orders__empty">No tienes pedidos aún.</p>
        `;
        return;
    }

    container.innerHTML = orders
        .map((order) => {
            const statusLabel =
                ORDER_STATUS_LABELS[order.status] ?? order.status;
            const date = order.created_at
                ? new Date(order.created_at).toLocaleDateString("es-MX")
                : "";

            return `
            <article class="order-card" data-order-id="${order.id}">
                <header class="order-card__header">
                    <h3 class="order-card__id">Pedido #${order.id}</h3>
                    <span class="order-card__status order-card__status--${order.status}">
                        ${statusLabel}
                    </span>
                </header>
                <p class="order-card__date">${date}</p>
                <p class="order-card__total">${formatPrice(order.total)}</p>
            </article>
        `;
        })
        .join("");
}

/**
 * @param {boolean} isLoading
 */
export function renderLoading(isLoading) {
    let el = document.getElementById("loading-overlay");
    if (isLoading) {
        if (!el) {
            el = document.createElement("div");
            el.id = "loading-overlay";
            el.className = "loading-overlay";
            el.innerHTML = `<div class="loading-overlay__spinner"></div>`;
            document.body.appendChild(el);
        }
        el.classList.add("loading-overlay--visible");
    } else if (el) {
        el.classList.remove("loading-overlay--visible");
    }
}

/**
 * @param {object} state
 */
export function renderAll(state) {
    if (!state) return;

    renderCartCount(state.cartCount);
    renderCategories(state.categories);
    setActiveCategory(state.filters?.category);
    renderProducts(getFilteredProducts());
    renderCart(state.cartItems);
    renderOrders(state.orders);
    renderLoading(state.loading);

    const orderingSelect = document.getElementById("ordering-select");
    if (orderingSelect && state.filters?.ordering)  orderingSelect.value = state.filters.ordering;

    const searchInput = document.getElementById("search-input");
    if (searchInput && state.filters?.search != null) searchInput.value = state.filters.search;
    
}

export default {
    formatPrice,
    renderCartCount,
    renderCategories,
    setActiveCategory,
    renderProducts,
    renderCart,
    renderOrders,
    renderLoading,
    renderAll,
};