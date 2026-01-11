import { t } from "../utils.js";

export const ITEMS_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: t("Name") },
    { key: "sku", label: "SKU" },
    { key: "price", label: t("Price (Czk)") },
    { key: "quantity", label: t("Quantity") },
    { key: "is_active", label: t("status") },
    { key: "company_name", label: t("company") },
    { key: "__actions__", label: t("actions") }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-item-modal">
      ${"CreateItemEntry"}
    </button>
  `
};

export const ITEMS_SCHEMA_VIEW = {
  columns: [
    { key: "name", label: t("Name") },
    { key: "price", label: t("Price (Czk)") },
    { key: "quantity", label: t("Quantity") }
  ],
  headerButton: ""
};

export const ITEM_FIELDS = [
  {
    id: "name",
    label: t("Name"),
    html: `<input id="name" class="form-control" required>`
  },
  {
    id: "price",
    label: t("Price (Czk)"),
    html: `
      <input
        id="price"
        type="number"
        class="form-control"
        min="0"
        step="0.01"
        required
      >
    `
  },
  {
    id: "quantity",
    label: t("Quantity"),
    html: `
      <input
        id="quantity"
        type="number"
        class="form-control"
        min="0"
        step="1"
        required
      >
    `
  }
];

