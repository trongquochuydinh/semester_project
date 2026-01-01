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
