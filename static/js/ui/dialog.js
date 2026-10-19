function ensureDialogRoot() {
    let root = document.getElementById("dialog-root");
    if (!root) {
        root = document.createElement("div");
        root.id = "dialog-root";
        root.className = "dialog-root";
        document.body.appendChild(root);
    }
    return root;
}

function closeDialog() {
    const root = document.getElementById("dialog-root");
    if (root) {
        root.innerHTML = "";
        root.classList.remove("dialog-root--open");
    }
}

/**
 * @param {string} message
 * @param {string} [title="Aviso"]
 * @returns {Promise<void>}
 */
export function showAlert(message, title = "Aviso") {
    return new Promise((resolve) => {
        const root = ensureDialogRoot();
        root.classList.add("dialog-root--open");

        root.innerHTML = `
            <div class="dialog-backdrop" data-dialog-close></div>
            <div class="dialog" role="alertdialog" aria-modal="true" aria-labelledby="dialog-title">
                <h2 id="dialog-title" class="dialog__title">${title}</h2>
                <p class="dialog__message">${message}</p>
                <div class="dialog__actions">
                    <button type="button" class="dialog__btn dialog__btn--primary" data-dialog-ok>
                        Aceptar
                    </button>
                </div>
            </div>
        `;

        const finish = () => {
            closeDialog();
            resolve();
        };

        root.querySelector("[data-dialog-ok]").addEventListener("click", finish);
        root.querySelector("[data-dialog-close]").addEventListener("click", finish);
    });
}

/** 
 * @param {string} message
 * @param {string} [title="Confirmar"]
 * @returns {Promise<boolean>}
 */
export function showConfirm(message, title = "Confirmar") {
    return new Promise((resolve) => {
        const root = ensureDialogRoot();
        root.classList.add("dialog-root--open");

        root.innerHTML = `
            <div class="dialog-backdrop" data-dialog-close></div>
            <div class="dialog" role="alertdialog" aria-modal="true" aria-labelledby="dialog-title">
                <h2 id="dialog-title" class="dialog__title">${title}</h2>
                <p class="dialog__message">${message}</p>
                <div class="dialog__actions">
                    <button type="button" class="dialog__btn dialog__btn--secondary" data-dialog-cancel>
                        Cancelar
                    </button>
                    <button type="button" class="dialog__btn dialog__btn--primary" data-dialog-ok>
                        Confirmar
                    </button>
                </div>
            </div>
        `;

        const finish = (value) => {
            closeDialog();
            resolve(value);
        };

        root.querySelector("[data-dialog-ok]").addEventListener("click", () => finish(true));
        root.querySelector("[data-dialog-cancel]").addEventListener("click", () => finish(false));
        root.querySelector("[data-dialog-close]").addEventListener("click", () => finish(false));
    });
}

/**
 * @param {string} message
 * @param {"success"|"error"|"info"} [type="info"]
 * @param {number} [duration=3000]
 */

export function showToast(message, type = "info", duration = 3000) {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.className = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add("toast--visible"));

    setTimeout(() => {
        toast.classList.remove("toast--visible");
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

export default {
    showAlert,
    showConfirm,
    showToast,
    closeDialog,
};