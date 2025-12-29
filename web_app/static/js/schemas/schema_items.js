export const ITEMS_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: "Company" },
    { key: "sku", label: "SKU" },
    { key: "price", label: "Price" },
    { key: "quantity", label: "Quantity" },
    { key: "is_active", label: "Status" },
    { key: "company_name", label: "Company" },
    { key: "create_at", label: "Created at" },
    { key: "updated_at", label: "Updated at" },
    { key: "__actions__", label: "Actions" }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-company-modal">
      Create Item entry
    </button>
  `
};

export const ITEMS_SCHEMA_VIEW = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: "Name" },
    { key: "price", label: "Price" },
    { key: "quantity", label: "Quantity" }
  ],
  headerButton: ""
};
