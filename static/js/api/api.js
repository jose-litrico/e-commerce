const BASE_URL = "/api";

function getCookie(name) {
    const cookies = document.cookie.split(";");

    for(const cookie of cookies) {
        const [key, value] = cookie.trim().split("=");

        if(key === name) return decodeURIComponent(value);
    }

    return null;
}

async function request(endpoint, options={}) {
    const url = `${BASE_URL}${endpoint}`;

    const config = {
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
            ...options.headers,
        },
        ...options,
    };

    if(config.body && typeof config.body === "object") config.body = JSON.stringify(config.body);

    const response = await fetch(url, config);

    let data = null;
    const contentType = response.headers.get("content-type");

    if(contentType && contentType.includes("application/json")) data = await response.json();

    if(!response.ok) {
        const error = new Error("Api Error");

        error.status = response.status;
        error.data = data;

        throw error;
    }

    return data;
}

export const UserApi = {
    list() {
        return request("/users/");
    },

    get(id) {
        return request(`/users/${id}/`);
    },

    create(payload) {
        return request("/users/", {
            method: "POST",
            body: payload,
        });
    },

    update(id, payload) {
        return request(`/users/${id}/`, {
            method: "PUT",
            body: payload,
        });
    },

    orders(userId) {
        return request(`/users/${userId}/orders/`);
    },
};

export const CategoriesApi = {
    list() {
        return request("/categories/");
    },

    get(id) {
        return request(`/categories/${id}/`);
    },

    create(payload) {
        return request("/categories/", {
            method: "POST",
            body: payload,
        });
    },

    update(id, payload) {
        return request(`/categories/${id}/`, {
            method: "PUT",
            body: payload,
        });
    },

    delete(id) {
        return request(`/categories/${id}/`, {
            method: "DELETE",
        });
    },
}

export const ProductsApi = {
    list({ search, category, ordering } = {}) {
        const params = new URLSearchParams();

        if(search) params.append("search", search);
        if(category) params.append("category", category);
        if(ordering) params.append("ordering", ordering);

        const query = params.toString();
        const endpoint = query? `/products/?${query}` : "/products/";

        return request(endpoint);
    },

    get(id) {
        return request(`/products/${id}/`);
    },

    create(payload) {
        return request("/products/", {
            method: "POST",
            body: payload,
        });
    },

    update(id, payload) {
        return request(`/products/${id}/`, {
            method: "PUT",
            body: payload,
        });
    },

    delete(id) {
        return request(`/products/${id}/`, {
            method: "DELETE",
        });
    },
}

export const AddressApi = {
    list() {
        return request("/address/");
    },

    get(id) {
        return request(`/address/${id}/`);
    },

    create(payload) {
        return request("/address/", {
            method: "POST",
            body: payload,
        });
    },

    update(id, payload) {
        return request(`/address/${id}/`, {
            method: "PUT",
            body: payload,
        });
    },

    delete(id) {
        return request(`/address/${id}/`, {
            method: "DELETE",
        });
    },
}

export const CartApi = {
    get(userId) {
        return request(`/cart/${userId}/`);
    },

    addItem(userId, { product, quantity = 1}) {
        return request(`/cart/${userId}/add/`, {
            method: "POST",
            body: { product, quantity },
        });
    },

    updateItem(userId, itemId, quantity) {
        return request(`/cart/${userId}/items/${itemId}/`, {
            method: "PUT",
            body: { quantity },
        });
    },
    
    removeItem(userId, itemId) {
        return request(`/cart/${userId}/items/${itemId}/remove/`, {
            method: "DELETE",
        });
    },

    clear(userId) {
        return request(`/cart/${userId}/clear/`, {
            method: "POST",
        });
    }
}

export const orderApi = {
    list() {
        return request("/orders/");
    },

    get(id) {
        return request(`/orders/${id}/`);
    },

    create(payload) {
        return request("/orders/", {
            method: "POST",
            body: payload,
        });
    },

    updateStatus(id, status) {
        return request(`/orders/${id}/status/`, {
            method: "POST",
            body: { status },
        });
    },
}

export const api = {
    users: UserApi,
    categories: CategoriesApi,
    products: ProductsApi,
    addresses: AddressApi,
    cart: CartApi,
    orders: orderApi,
};

export default api;