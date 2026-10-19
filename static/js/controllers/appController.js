import { subscribe } from "../state/state.js";
import { renderAll } from "../ui/render.js";
import { bindAllEvents } from "../events/events.js";

import { loadCategories } from "./categoriesController.js";
import { loadProducts } from "./productsController.js";
import { loadCart } from "./cartController.js";
import { loadOrders } from "./ordersController.js";
import { loadCurrentUser, loadAddresses } from "./usersController.js";

export async function initApp() {
    subscribe((state) => renderAll(state));

    bindAllEvents();

    await loadCurrentUser();
    await loadAddresses();
    await loadCategories();
    await loadProducts();
    await loadCart();
    await loadOrders();
}