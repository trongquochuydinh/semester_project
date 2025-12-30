import { BASE_ITEM_MODAL } from "./modal_items.js";
import { apiFetch } from "../utils.js";

export const CREATE_ITEM_MODAL = {
  id: "createItemModal",
  title: "Create Item Entry",
  ...BASE_ITEM_MODAL,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createItemModal");

    const inputs = modal.querySelectorAll("input");
    for (const input of inputs) {
        if (!input.checkValidity()) {
        input.reportValidity();
        return;
        }
    }

    const payload = {
      name: modal.querySelector("#name").value,
      price: modal.querySelector("#price").value,
      quantity: modal.querySelector("#quantity").value
    };

    try {
      const data = await apiFetch("/items/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to create company"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company created successfully!</b>
        </div>
      `);

    } catch (err) {
      console.error(err);
      writeResult(
        `<div class="text-danger">${err.message || "Unexpected error occurred."}</div>`
      );
    }
  }
};
