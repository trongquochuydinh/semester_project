// static/js/modals/modal_company_create.js
import { BASE_COMPANY_MODAL } from "./modal_company.js";
import { apiFetch } from "../utils.js";

export const CREATE_COMPANY_MODAL = {
  id: "createCompanyModal",
  title: "Create Company",
  ...BASE_COMPANY_MODAL,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createCompanyModal");

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
      const data = await apiFetch("/companies/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to create company"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company created successfully!</b>
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
