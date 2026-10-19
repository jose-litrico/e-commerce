import { api } from "../api/api.js";
import {
    setProducts,
    setFilters,
    setLoading,
    setError,
    getState,
} from "../state/state.js";
import { renderProducts, setActiveCategory } from "../ui/render.js";
import { showToast } from "../ui/dialog.js";
import {
    validateProductFilters,
    firstError,
} from "../validators/validators.js";

export async function loadProducts() {
    setLoading(true);
    setError(null);

    try {
        const { filters } = getState();
        const products = await api.products.list({
            search: filters.search || undefined,
            category: filters.category || undefined,
            ordering: filters.ordering || undefined,
        });
        
        setProducts(products);
        renderProducts(products);
    }catch (err) {
        setError(err.data || err.message);
        showToast("Error al cargar productos", "error");
    }finally {
        setLoading(false);
    }
}

export function handleSearch(search) {
    const result = validateProductFilters({ search });
    if(!result.valid) {
        showToast(firstError(result.errors), "error");
        
        return;
    }

    setFilters({ search: (search || "").trim() });
    loadProducts();
}

export function handleOrdering(ordering) {
    const result = validateProductFilters({ ordering });
    if(!result.valid) {
        showToast(firstError(result.errors), "error");
       
        return;
    }

    setFilters({ ordering });
    loadProducts();
}

export function handleCategoryFilter(categoryId) {
    const category =categoryId === "all" || categoryId == null ? null : Number(categoryId);
    const result = validateProductFilters({ category });
    
    if(!result.valid) {
        showToast(firstError(result.errors), "error");
        
        return;
    }

    setFilters({ category });
    setActiveCategory(categoryId === "all" ? null : categoryId);
    loadProducts();
}

export default {
    loadProducts,
    handleSearch,
    handleOrdering,
    handleCategoryFilter,
};