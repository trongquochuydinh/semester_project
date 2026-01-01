import { COMPANY_FIELDS } from "./modal_company.fields.js";
import { validateCompanyModal, extractCompanyPayload } from "./modal_company.utils.js";
import { apiFetch } from "../../utils.js";

export const CREATE_COMPANY_MODAL = {
  id: "createCompanyModal",
  title: "Create Company",
  fields: COMPANY_FIELDS,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createCompanyModal");
    if (!validateCompanyModal(modal)) return;

    try {
      const data = await apiFetch("/companies/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractCompanyPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company created successfully!</b>
        </div>
      `);
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
    }
  }
};
