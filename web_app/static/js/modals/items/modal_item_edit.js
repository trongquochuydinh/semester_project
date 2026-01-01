import { ITEM_FIELDS } from "./modal_item.fields.js";
import { loadItemData } from "./modal_item.loaders.js";
import {
  validateInputs,
  extractPayload,
  renderSuccess,
  renderError
} from "./modal_item.utils.js";
import { apiFetch } from "../../utils.js";

export const EDIT_ITEM_MODAL = {
  id: "editItemModal",
  title: "Edit Item Entry",
  fields: ITEM_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("editItemModal");
    const itemId = modal.dataset.itemId;

    if (itemId) {
      await loadItemData(modal, itemId);
    }
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editItemModal");
    const itemId = modal.dataset.itemId;

    if (!validateInputs(modal)) return;

    try {
      const data = await apiFetch(`/items/edit/${itemId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractPayload(modal, ["name", "price", "quantity"]))
      });

      if (!data.success) {
        renderError(writeResult, data.message || "Failed to update item");
        return;
      }

      renderSuccess(writeResult, "Item updated successfully!");
    } catch (err) {
      console.error(err);
      renderError(writeResult, err.message || "Unexpected error occurred");
    }
  }
};
