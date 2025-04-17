/** @odoo-module **/

import { onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";

function setupCatalogButton() {
    onMounted(() => {
        const button = document.querySelector('#clickable_div');
        if (button) {
            button.addEventListener('click', (e) => {
                console.log("Div clicked:", e);
            });
        }
    });
}

// Registrar el comportamiento en el punto de entrada adecuado (por ejemplo, en el frontend)
registry.category("services").add("library_portal.catalog_button", {
    start() {
        setupCatalogButton();
    }
});
