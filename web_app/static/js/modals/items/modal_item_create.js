import { ITEM_FIELDS } from "../../schemas/schema_items.js";
import {
  validateInputs,
  extractPayload,
  renderSuccess,
  renderError
} from "./modal_item.utils.js";
import { t, apiFetch } from "../../utils.js";

export const CREATE_ITEM_MODAL = {
  id: "createItemModal",
  title: t("CreateItemEntry"),
  fields: ITEM_FIELDS,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createItemModal");

    if (!validateInputs(modal)) return false;

    const payload = extractPayload(modal, ["name", "price", "quantity"]);

    try {
      const data = await apiFetch("/items/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        renderError(writeResult, data.message || "Failed to create item");
        return false;
      }

      renderSuccess(writeResult, "Item created successfully!")
      return true;
    } catch (err) {
      console.error(err);
      renderError(writeResult, err.message || "Unexpected error occurred")
      return false;
    }
  }
};
