import { t } from "../utils.js";

export const COMPANIES_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: t("company") },
    { key: "field", label: t("Field") },
    { key: "__actions__", label: t("actions") }
  ],
  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-company-modal">
      ${t("CreateCompany")}
    </button>
  `
};

export const COMPANIES_SCHEMA_VIEW = {
  columns: [
    { key: "id", label: "ID" },
    { key: "name", label: t("company") },
    { key: "field", label: t("Field") }
  ],
  headerButton: ""
};

export const COMPANY_FIELDS = [
  {
    id: "company_name",
    label: t("company"),
    html: `<input id="company_name" class="form-control" required>`
  },
  {
    id: "field",
    label: t("Field"),
    html: `<input id="field" class="form-control" required>`
  }
];
