export const COMPANIES_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: "Company" },
    { key: "field", label: "Field" },
    { key: "__actions__", label: "Actions" }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-company-modal">
      Create Company
    </button>
  `
};

export const COMPANIES_SCHEMA_VIEW = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: "Company" },
    { key: "field", label: "Field" }
  ],
  headerButton: ""
};

export const COMPANY_FIELDS = [
  {
    id: "company_name",
    label: "Company name",
    html: `<input id="company_name" class="form-control" required>`
  },
  {
    id: "field",
    label: "Field",
    html: `<input id="field" class="form-control" required>`
  }
];
