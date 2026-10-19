export function isEmpty(value) {
    return value === null || value === undefined || String(value).trim() === "";
}

export function isPositiveInteger(value) {
    const n = Number(value);

    return Number.isInteger(n) && n > 0;
}

export function isNonNegativeInteger(value) {
    const n = Number(value);

    return Number.isInteger(n) && n >= 0;
}

export function isPositiveNumber(value) {
    const n = Number(value);

    return !Number.isNaN(n) && n > 0;
}

export function isValidEmail(email) {
    if(isEmpty(email)) return false;

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).trim());
}

export function validateAddToCart({ productId, quantity = 1 }) {
    const errors = {};

    if (!isPositiveInteger(productId)) errors.product = "Producto inválido.";
    if (!isPositiveInteger(quantity)) errors.quantity = "La cantidad debe ser un entero mayor a 0."; 

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function validateUpdateQuantity({ itemId, quantity }) {
    const errors = {};

    if(!isPositiveInteger(itemId)) errors.item = "Ítem inválido.";
    if(!isPositiveInteger(quantity)) errors.quantity = "La cantidad debe ser un entero mayor a 0.";

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function validateCreateOrder({ userId, addressId, cartItems = [] }) {
    const errors = {};

    if(!isPositiveInteger(userId)) errors.user = "Usuario inválido.";
    if(!isPositiveInteger(addressId)) errors.shipping_address = "Debes seleccionar una dirección de envío.";
    if(!Array.isArray(cartItems) || cartItems.length === 0) errors.cart = "El carrito está vacío.";

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function validateOrderStatus(status) {
    const allowed = [
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled",
    ];
    const errors = {};

    if(isEmpty(status) || !allowed.includes(String(status))) errors.status = `Estado inválido. Opciones: ${allowed.join(", ")}`;

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function validateProductFilters({ search, category, ordering } = {}) {
    const errors = {};
    const allowedOrderings = [
        "price",
        "-price",
        "name",
        "-name",
        "created_at",
        "-created_at",
    ];

    if(category != null && category !== "" && !isPositiveInteger(category)) errors.category = "Categoría inválida.";
    if(ordering && !allowedOrderings.includes(ordering)) errors.ordering = "Ordenamiento inválido.";
    if(search && String(search).length > 200) errors.search = "La búsqueda es demasiado larga.";

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function validateAddress(payload = {}) {
    const errors = {};

    if (isEmpty(payload.street)) errors.street = "La calle es obligatoria.";
    if (isEmpty(payload.city)) errors.city = "La ciudad es obligatoria.";
    if (isEmpty(payload.state)) errors.state = "El estado es obligatorio.";
    if (isEmpty(payload.zip_code)) errors.zip_code = "El código postal es obligatorio.";
    if (isEmpty(payload.country)) errors.country = "El país es obligatorio.";
    

    return {
        valid: Object.keys(errors).length === 0,
        errors,
    };
}

export function firstError(errors = {}) {
    const keys = Object.keys(errors);

    if(!keys.length) return null;
    const value = errors[keys[0]];

    return Array.isArray(value) ? value[0] : value;
}

export default {
    isEmpty,
    isPositiveInteger,
    isNonNegativeInteger,
    isPositiveNumber,
    isValidEmail,
    validateAddToCart,
    validateUpdateQuantity,
    validateCreateOrder,
    validateOrderStatus,
    validateProductFilters,
    validateAddress,
    firstError,
};