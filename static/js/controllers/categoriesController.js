import { api } from "../api/api.js";
import { setCategories, setLoading, setError } from "../state/state.js";
import { renderCategories } from "../ui/render.js";
import { showToast } from "../ui/dialog.js";

export async function loadCategories() {
    setLoading(true);
    setError(null);

    try {
        const categories = await api.categories.list();

        setCategories(categories);
        renderCategories(categories);
    }catch (err) {
        setError(err.data || err.message);
        showToast("Error al cargar categorías", "error");
    }finally {
        setLoading(false);
    }
}

export default {
    loadCategories,
};