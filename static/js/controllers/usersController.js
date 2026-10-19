import { api } from "../api/api.js";
import {
    setCurrentUser,
    setAddresses,
    setLoading,
    setError,
} from "../state/state.js";
import { showToast } from "../ui/dialog.js";
import { SEED } from "../constants/constants.js";

export async function loadCurrentUser() {
    setLoading(true);
    setError(null);

    try {
        const users = await api.users.list();
        const user =
            users.find((u) => u.username === "juanperez") || users[0];

        if (!user) throw new Error("No hay usuarios");

        setCurrentUser(user);
    } catch (err) {
        setError(err.data || err.message);
        showToast("No se pudo cargar el usuario", "error");
        console.warn(err);
    } finally {
        setLoading(false);
    }
}
export async function loadAddresses() {
    setLoading(true);
    try {
        const addresses = await api.addresses.list();

        setAddresses(addresses);
    }catch (err) {
        setAddresses(SEED.addresses);
        console.warn("Direcciones desde SEED", err);
    }finally {
        setLoading(false);
    }
}

export default {
    loadCurrentUser,
    loadAddresses,
};