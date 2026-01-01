export const ITEMS_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: "Name" },
    { key: "sku", label: "SKU" },
    { key: "price", label: "Price (Czk)" },
    { key: "quantity", label: "Quantity" },
    { key: "is_active", label: "Status" },
    { key: "company_name", label: "Company" },
    { key: "__actions__", label: "Actions" }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-item-modal">
      Create Item entry
    </button>
  `
};

export const ITEMS_SCHEMA_VIEW = {
  columns: [
    { key: "name", label: "Name" },
    { key: "price", label: "Price (Czk)" },
    { key: "quantity", label: "Quantity" }
  ],
  headerButton: ""
};
