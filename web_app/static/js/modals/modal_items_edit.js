import { BASE_ITEM_MODAL } from "./modal_items.js";
import { apiFetch } from "../utils.js";

async function populateItemData(itemId) {
  try {
    const item = await apiFetch(`/items/get/${itemId}`);
    const modal = document.getElementById("editItemModal");

    modal.querySelector("#name").value = item.name ?? "";
    modal.querySelector("#price").value = item.price ?? "";
    modal.querySelector("#quantity").value = item.quantity ?? "";

  } catch (err) {
    console.error("Error loading item data:", err);
  }
}

export const EDIT_ITEM_MODAL = {
  id: "editItemModal",
  title: "Edit Item Entry",
  ...BASE_ITEM_MODAL,

  onLoad: async () => {
    const modal = document.getElementById("editItemModal");
    const itemId = modal.dataset.itemId;

    if (itemId) {
      await populateItemData(itemId);
    }
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editItemModal");
    const itemId = modal.dataset.itemId;

    const payload = {
      name: modal.querySelector("#name").value,
      price: modal.querySelector("#price").value,
      quantity: modal.querySelector("#quantity").value
    };

    try {
      const data = await apiFetch(`/items/edit/${itemId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to update item"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Item updated successfully!</b>
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
