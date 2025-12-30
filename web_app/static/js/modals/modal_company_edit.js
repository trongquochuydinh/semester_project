// static/js/modals/modal_company_edit.js
import { BASE_COMPANY_MODAL } from "./modal_company.js";
import { apiFetch } from "../utils.js";

async function populateCompanyData(companyId) {
  try {
    const company = await apiFetch(`/companies/get/${companyId}`);
    const modal = document.getElementById("editCompanyModal");

    modal.querySelector("#company_name").value = company.company_name ?? "";
    modal.querySelector("#field").value = company.field ?? "";

  } catch (err) {
    console.error("Error loading company data:", err);
  }
}

export const EDIT_COMPANY_MODAL = {
  id: "editCompanyModal",
  title: "Edit Company",
  ...BASE_COMPANY_MODAL,

  onLoad: async () => {
    const modal = document.getElementById("editCompanyModal");
    const companyId = modal.dataset.companyId;

    if (companyId) {
      await populateCompanyData(companyId);
    }
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editCompanyModal");
    const companyId = modal.dataset.companyId;

    const inputs = modal.querySelectorAll("input");
    for (const input of inputs) {
        if (!input.checkValidity()) {
        input.reportValidity();
        return;
        }
    }

    const payload = {
      company_name: modal.querySelector("#company_name").value,
      field: modal.querySelector("#field").value
    };

    try {
      const data = await apiFetch(`/companies/edit/${companyId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to update company"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company updated successfully!</b>
        </div>
      `);

    } catch (err) {
      console.error(err);
      writeResult(
        `<div class="text-danger">${err.message || "Unexpected error occurred."}</div>`
      );
    }
  }
};
