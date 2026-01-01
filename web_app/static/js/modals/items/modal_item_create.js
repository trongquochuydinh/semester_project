import { ITEM_FIELDS } from "./modal_item.fields.js";
import {
  validateInputs,
  extractPayload,
  renderSuccess,
  renderError
} from "./modal_item.utils.js";
import { apiFetch } from "../../utils.js";

export const CREATE_ITEM_MODAL = {
  id: "createItemModal",
  title: "Create Item Entry",
  fields: ITEM_FIELDS,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createItemModal");

    if (!validateInputs(modal)) return;

    const payload = extractPayload(modal, ["name", "price", "quantity"]);

    try {
      const data = await apiFetch("/items/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        renderError(writeResult, data.message || "Failed to create item");
        return;
      }

      renderSuccess(writeResult, "Item created successfully!");
    } catch (err) {
      console.error(err);
      renderError(writeResult, err.message || "Unexpected error occurred");
    }
  }
};
