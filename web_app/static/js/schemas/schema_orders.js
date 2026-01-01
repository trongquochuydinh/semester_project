export const ORDER_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "order_type", label: "Order Type" },
    { key: "created_at", label: "Created At" },
    { key: "completed_at", label: "Completed At" },
    { key: "total_price", label: "Total Price (Czk)" },
    { key: "user_id", label: "Issuer" },
    { key: "status", label: "Status" },
    { key: "__actions__", label: "Actions" }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-order-modal">
      Create Order entry
    </button>
  `
};

export const ORDER_SCHEMA_VIEW = {
  columns: [
    { key: "name", label: "Name" },
    { key: "price", label: "Price (Czk)" },
    { key: "quantity", label: "Quantity" }
  ],
  headerButton: ""
};

export const ORDER_SCHEMA_SELECT = {
  columns: [
    { key: "name", label: "Item" },
    { key: "price", label: "Price (CZK)" },
    { key: "__actions__", label: "Select" }
  ],
  headerButton: ""
};

export const ORDER_FIELDS = [
  {
    id: "order_type",
    label: "Order Type",
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
