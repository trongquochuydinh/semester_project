import { ITEM_FIELDS } from "../../schemas/schema_items.js";
import { loadItemData } from "./modal_item.loaders.js";
import {
  validateInputs,
  extractPayload,
  renderSuccess,
  renderError
} from "./modal_item.utils.js";
import { t, apiFetch } from "../../utils.js";

export const EDIT_ITEM_MODAL = {
  id: "editItemModal",
  title: t("EditItemEntry"),
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

    if (!validateInputs(modal)) return false;

    try {
      const data = await apiFetch(`/items/edit/${itemId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractPayload(modal, ["name", "price", "quantity"]))
      });

      if (!data.success) {
        renderError(writeResult, data.message || "Failed to update item");
        return false;
      }

      renderSuccess(writeResult, "Item updated successfully!");
      return true;
    } catch (err) {
      console.error(err);
      renderError(writeResult, err.message || "Unexpected error occurred");
      return false;
    }
  }
};
