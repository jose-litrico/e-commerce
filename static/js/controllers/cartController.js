import { api } from "../api/api.js";
import {
    getState,
    setCart,
    setCartItems,
    setLoading,
    setError,
} from "../state/state.js";
import { renderCart, renderCartCount } from "../ui/render.js";
import { showToast, showConfirm } from "../ui/dialog.js";
import {
    validateAddToCart,
    validateUpdateQuantity,
    firstError,
} from "../validators/validators.js";

function getUserId() {
    const { currentUser } = getState();
    return currentUser?.id ?? null;
}

export async function loadCart() {
    const userId = getUserId();
    if(!userId) return;

    setLoading(true);
    try {
        const cart = await api.cart.get(userId);
        setCart(cart);

        const items = cart?.items ?? [];
        setCartItems(items);

        renderCart(items);
        renderCartCount();
    }catch (err) {
        setError(err.data || err.message);
        showToast("Error al cargar el carrito", "error");
    }finally {
        setLoading(false);
    }
}

export async function addToCart(productId, quantity = 1) {
    const userId = getUserId();
    if(!userId) {
        showToast("Debes iniciar sesión para agregar al carrito", "error");
        
        return;
    }

    const result = validateAddToCart({ productId, quantity });
    if(!result.valid) {
        showToast(firstError(result.errors), "error");

        return;
    }

    setLoading(true);
    try {
        await api.cart.addItem(userId, {
            product: Number(productId),
            quantity: Number(quantity),
        });

        await loadCart();
        showToast("Producto agregado al carrito", "success");
    }catch (err) {
        const msg = err.data?.quantity?.[0] || err.data?.product?.[0] || err.data?.detail || "No se pudo agregar al carrito";
        showToast(msg, "error");
    }finally {
        setLoading(false);
    }
}

export async function updateCartItem(itemId, quantity) {
    const userId = getUserId();
    if(!userId) return;

    if(quantity < 1) {
        return removeFromCart(itemId);
    }

    const result = validateUpdateQuantity({ itemId, quantity });
    if(!result.valid) {
        showToast(firstError(result.errors), "error");
        
        return;
    }

    setLoading(true);
    try {
        await api.cart.updateItem(userId, itemId, quantity);
        await loadCart();
    }catch (err) {
        const msg = err.data?.quantity?.[0] || err.data?.item?.[0] || "No se pudo actualizar la cantidad";
        showToast(msg, "error");
    }finally {
        setLoading(false);
    }
}

export async function removeFromCart(itemId) {
    const userId = getUserId();
    if(!userId) return;

    setLoading(true);
    try {
        await api.cart.removeItem(userId, itemId);
        await loadCart();

        showToast("Ítem eliminado", "success");
    }catch (err) {
        showToast("No se pudo eliminar el ítem", "error");
    }finally {
        setLoading(false);
    }
}

export async function clearCart() {
    const userId = getUserId();
    if(!userId) return;

    const ok = await showConfirm("¿Vaciar todo el carrito?");
    if(!ok) return;

    setLoading(true);
    try {
        await api.cart.clear(userId);
        await loadCart();
        
        showToast("Carrito vaciado", "success");
    }catch (err) {
        showToast("No se pudo vaciar el carrito", "error");
    }finally {
        setLoading(false);
    }
}

export default {
    loadCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
};