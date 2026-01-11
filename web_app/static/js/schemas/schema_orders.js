import { t } from "../utils.js";

export const ORDER_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "order_type", label: t("Order Type") },
    { key: "created_at_fmt", label: t("Created At") },
    { key: "completed_at_fmt", label: t("Completed At") },
    // { key: "total_price", label: t("Total Price (Czk)") },
    { key: "user_id", label: t("Issuer") },
    { key: "status", label: t("status") },
    { key: "__actions__", label: t("actions") }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-order-modal">
      ${t("CreateOrder")}
    </button>
  `
};

export const ORDER_SCHEMA_VIEW = {
  columns: [
    { key: "name", label: t("Name") },
    { key: "price", label: t("Price (Czk)") },
    { key: "quantity", label: t("Quantity") }
  ],
  headerButton: ""
};

export const ORDER_SCHEMA_SELECT = {
  columns: [
    { key: "name", label: t("Item") },
    { key: "price", label: t("Price (CZK)") },
    { key: "__actions__", label: "Select" }
  ],
  headerButton: ""
};

export const ORDER_FIELDS = [
  {
    id: "order_type",
    label: t("Order Type"),
    html: `
      <select id="order_type" class="form-select" required>
        <option value="restock">Restock</option>
        <option value="sale">Sale</option>
      </select>
    `
  },
  {
    id: "__items__",
    label: "",
    html: `
      <div class="order-items-container mt-3"></div>
    `
  }
];
