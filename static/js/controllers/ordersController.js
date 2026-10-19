import { api } from "../api/api.js";
import {
    getState,
    setOrders,
    setLoading,
    setError,
} from "../state/state.js";
import { renderOrders } from "../ui/render.js";
import { showToast, showConfirm, showAlert } from "../ui/dialog.js";
import { loadCart } from "./cartController.js";
import {
    validateCreateOrder,
    validateOrderStatus,
    firstError,
} from "../validators/validators.js";

function getUserId() {
    const { currentUser } = getState();

    return currentUser?.id ?? null;
}

export async function loadOrders() {
    const userId = getUserId();
    if(!userId) return;

    setLoading(true);
    setError(null);

    try {
        const orders = await api.users.orders(userId);
        setOrders(orders);
        renderOrders(orders);
    }catch (err) {
        setError(err.data || err.message);
        showToast("Error al cargar pedidos", "error");
    }finally {
        setLoading(false);
    }
}

export async function createOrder(addressId) {
    const userId = getUserId();
    const { cartItems } = getState();

    const result = validateCreateOrder({
        userId,
        addressId,
        cartItems,
    });

    if(!result.valid) {
        showToast(firstError(result.errors), "error");

        return;
    }

    const ok = await showConfirm("¿Confirmar el pedido?");
    if(!ok) return;

    setLoading(true);
    try {
        const order = await api.orders.create({
            user: userId,
            shipping_address: Number(addressId),
        });

        await loadCart();
        await loadOrders();
        
        showToast(`Pedido #${order.id} creado`, "success");
    }catch (err) {
        const msg = err.data?.cart?.[0] || err.data?.stock?.[0] || err.data?.shipping_address?.[0] || err.data?.error || "No se pudo crear el pedido";
        showToast(typeof msg === "string" ? msg : JSON.stringify(msg), "error");
    }finally {
        setLoading(false);
    }
}

export async function updateOrderStatus(orderId, status) {
    const result = validateOrderStatus(status);
    if(!result.valid) {
        showToast(firstError(result.errors), "error");
        
        return;
    }

    setLoading(true);
    try {
        await api.orders.updateStatus(orderId, status);
        await loadOrders();
        
        showToast("Estado actualizado", "success");
    }catch (err) {
        showToast("No se pudo actualizar el estado", "error");
    }finally {
        setLoading(false);
    }
}

export default {
    loadOrders,
    createOrder,
    updateOrderStatus,
};