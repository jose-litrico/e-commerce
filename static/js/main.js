import { initApp } from "./controllers/appController.js";

document.addEventListener("DOMContentLoaded", () => {
    initApp().catch((err) => {
        console.error("Error al iniciar la aplicación: ", err);
    });
});