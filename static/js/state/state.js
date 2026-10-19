import { SEED } from "../constants/constants.js";

const state = {
    products: [],
    categories: [],
    cart: null,
    cartItems: [],
    orders: [],
    addresses: [],
    currentUser: null,

    filters: {
        search: "",
        category: null,
        ordering: "-created_at",
    },

    loading: false,
    error: null,

    listeners: [],
};

function notify() {
    state.listeners.forEach((listener) => listener(getState()));
}

export function subscribe(listener) {
    state.listeners.push(listener);
    return () => {
        state.listeners = state.listeners.filter((l) => l !== listener);
    };
}

export function getState() {
    return {
        products: state.products,
        categories: state.categories,
        cart: state.cart,
        cartItems: state.cartItems,
        orders: state.orders,
        addresses: state.addresses,
        currentUser: state.currentUser,
        filters: { ...state.filters },
        loading: state.loading,
        error: state.error,
        cartCount: getCartCount(),
        cartTotal: getCartTotal(),
    };
}

export function getCartCount() {
    return state.cartItems.reduce((sum, item) => sum + item.quantity, 0);
}

export function getCartTotal() {
    return state.cartItems.reduce((sum, item) => {
        const price = item.product?.price ?? item.price ?? 0;
        return sum + price * item.quantity;
    }, 0);
}

export function getFilteredProducts() {
    let products = [...state.products];

    if (state.filters.search) {
        const q = state.filters.search.toLowerCase();
        products = products.filter(
            (p) =>
                p.name.toLowerCase().includes(q) ||
                (p.description && p.description.toLowerCase().includes(q))
        );
    }

    if (state.filters.category) {
        products = products.filter(
            (p) => p.category === state.filters.category || p.category?.id === state.filters.category
        );
    }

    const ordering = state.filters.ordering;

    products.sort((a, b) => {
        switch (ordering) {
            case "price":
                return a.price - b.price;
            case "-price":
                return b.price - a.price;
            case "name":
                return a.name.localeCompare(b.name);
            case "-name":
                return b.name.localeCompare(a.name);
            case "created_at":
                return new Date(a.created_at) - new Date(b.created_at);
            case "-created_at":
            default:
                return new Date(b.created_at) - new Date(a.created_at);
        }
    });

    return products;
}

export function setLoading(value) {
    state.loading = value;
    notify();
}

export function setError(error) {
    state.error = error;

    notify();
}

export function setProducts(products) {
    state.products = products;

    notify();
}

export function setCategories(categories) {
    state.categories = categories;

    notify();
}

export function setCart(cart) {
    state.cart = cart;
    state.cartItems = cart?.items ?? cart?.cartitem_set ?? [];

    notify();
}

export function setCartItems(items) {
    state.cartItems = items;

    notify();
}

export function setOrders(orders) {
    state.orders = orders;

    notify();
}

export function setAddresses(addresses) {
    state.addresses = addresses;

    notify();
}

export function setCurrentUser(user) {
    state.currentUser = user;

    notify();
}

export function setFilters(partial) {
    state.filters = { ...state.filters, ...partial };

    notify();
}

export function resetFilters() {
    state.filters = {
        search: "",
        category: null,
        ordering: "-created_at",
    };

    notify();
}

export function initWithSeed() {
    state.categories = SEED.categories;
    state.products = SEED.products;
    state.currentUser = SEED.users[1] ?? null; // juanperez por defecto
    state.addresses = SEED.addresses.filter(
        (a) => a.user === state.currentUser?.id
    );
    state.cartItems = [];
    state.orders = [];

    notify();
}

export default {
    subscribe,
    getState,
    getCartCount,
    getCartTotal,
    getFilteredProducts,
    setLoading,
    setError,
    setProducts,
    setCategories,
    setCart,
    setCartItems,
    setOrders,
    setAddresses,
    setCurrentUser,
    setFilters,
    resetFilters,
    initWithSeed,
};