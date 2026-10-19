import {
    handleSearch,
    handleOrdering,
    handleCategoryFilter,
} from "../controllers/productsController.js";

import {
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
} from "../controllers/cartController.js";

import { createOrder } from "../controllers/ordersController.js";
import { getState } from "../state/state.js";
import { showAlert, showToast } from "../ui/dialog.js";

function on(el, event, handler) {
    if(!el) return;
    el.addEventListener(event, handler);
}

export function bindCatalogEvents() {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");
    const orderingSelect = document.getElementById("ordering-select");
    const categoryList = document.getElementById("category-list");

    on(searchForm, "submit", (e) => {
        e.preventDefault();
        handleSearch(searchInput?.value || "");
    });

    on(orderingSelect, "change", (e) => {
        handleOrdering(e.target.value);
    });

    on(categoryList, "click", (e) => {
        const link = e.target.closest("[data-category]");
        
        if(!link) return;
        
        e.preventDefault();
        handleCategoryFilter(link.dataset.category);
    });
}

export function bindProductGridEvents() {
    const productGrid = document.getElementById("product-grid");

    on(productGrid, "click", (e) => {
        const btn = e.target.closest(".product-card__add-btn[data-product-id]");
        
        if(!btn || btn.disabled) return;

        e.preventDefault();
        addToCart(btn.dataset.productId, 1);
    });
}

export function bindCartPanelEvents() {
    const cartItems = document.getElementById("cart-items");
    const clearBtn = document.getElementById("btn-clear-cart");

    on(cartItems, "click", (e) => {
        const btn = e.target.closest("[data-action]");
        if(!btn) return;

        const itemId = Number(btn.dataset.itemId);
        const action = btn.dataset.action;
        const { cartItems: items } = getState();
        const item = items.find((i) => i.id === itemId);

        if(action === "remove") {
            removeFromCart(itemId);
            
            return;
        }

        if(!item) return;

        let quantity = item.quantity || 1;
        if(action === "increase") quantity += 1;
        if(action === "decrease") quantity -= 1;

        if(quantity < 1) {
            removeFromCart(itemId);
            
            return;
        }

        updateCartItem(itemId, quantity);
    });

    on(clearBtn, "click", () => clearCart());
}

export function bindCheckoutEvents() {
    const checkoutBtn = document.getElementById("btn-checkout");

    on(checkoutBtn, "click", async () => {
        const { addresses, currentUser, cartItems } = getState();

        if(!currentUser) {
            showToast("Debes iniciar sesión", "error");
            
            return;
        }

        if(!cartItems.length) {
            showToast("El carrito está vacío", "error");
            
            return;
        }

        const userAddresses = addresses.filter(
            (a) => a.user === currentUser.id || a.user?.id === currentUser.id
        );

        const address = userAddresses.find((a) => a.is_default) || userAddresses[0];

        if(!address) {
            await showAlert(
                "No tienes una dirección registrada. Agrégala desde el admin o la API.",
                "Sin dirección"
            );
            
            return;
        }

        await createOrder(address.id);
    });
}

export function bindAuthEvents() {
    const loginBtn = document.getElementById("btn-login");
    const registerBtn = document.getElementById("btn-register");

    on(loginBtn, "click", (e) => {
        e.preventDefault();
        showToast("Login: próximamente", "info");
    });

    on(registerBtn, "click", (e) => {
        e.preventDefault();
        showToast("Registro: próximamente", "info");
    });
}

export function bindAllEvents() {
    bindCatalogEvents();
    bindProductGridEvents();
    bindCartPanelEvents();
    bindCheckoutEvents();
    bindAuthEvents();
}

export default {
    bindAllEvents,
    bindCatalogEvents,
    bindProductGridEvents,
    bindCartPanelEvents,
    bindCheckoutEvents,
    bindAuthEvents,
};