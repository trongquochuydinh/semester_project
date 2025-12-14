import { createTable } from "./elements/table.js";
import { registerAction } from "./elements/action.js";
import { createFormModal } from "./elements/modal.js";
import { apiFetch } from "./utils.js";
import { CREATE_COMPANY_MODAL } from "./modals/modal_company_create.js";
import { EDIT_COMPANY_MODAL } from "./modals/modal_company_edit.js";
import { COMPANIES_SCHEMA_MANAGE } from "./schemas/schema_companies.js";

document.addEventListener("DOMContentLoaded", async () => {
  createFormModal(CREATE_COMPANY_MODAL);
  createFormModal(EDIT_COMPANY_MODAL);

    registerAction("open-create-company-modal", () => {
        const modalEl = document.getElementById("createCompanyModal");
        new bootstrap.Modal(modalEl).show();
    });

    registerAction("edit-company", (companyId) => {
        const modalEl = document.getElementById("editCompanyModal");

        // store company id for the modal
        modalEl.dataset.companyId = companyId;

        new bootstrap.Modal(modalEl).show();
    });

  const container = document.getElementById("companies-table");

  if (container) {
    const companies = await apiFetch("/paginate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        table_name: "companies",
        limit: 10,
        offset: 0,
        filters: {}
      })
    });

    createTable({
      title: "Companies",
      element: container,
      schema: COMPANIES_SCHEMA_MANAGE,
      rows: companies.data,
      actions: (row) => `
        <button 
          class="btn btn-sm btn-outline-primary"
          data-action="edit-company"
          data-id="${row.id}">
          Edit
        </button>

        <button 
          class="btn btn-sm btn-outline-danger ms-2"
          data-action="delete-company"
          data-id="${row.id}">
          Delete
        </button>
      `
    });
  }
});
