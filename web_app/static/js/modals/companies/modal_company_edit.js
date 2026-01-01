import { COMPANY_FIELDS } from "../../schemas/schema_companies.js";
import { loadCompanyData } from "./modal_company.loaders.js";
import { validateCompanyModal, extractCompanyPayload } from "./modal_company.utils.js";
import { apiFetch } from "../../utils.js";

export const EDIT_COMPANY_MODAL = {
  id: "editCompanyModal",
  title: "Edit Company",
  fields: COMPANY_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("editCompanyModal");
    const companyId = modal.dataset.companyId;

    if (companyId) {
      await loadCompanyData(modal, companyId);
    }
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editCompanyModal");
    const companyId = modal.dataset.companyId;

    if (!validateCompanyModal(modal)) return;

    try {
      const data = await apiFetch(`/companies/edit/${companyId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractCompanyPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company updated successfully!</b>
        </div>
      `);
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
    }
  }
};
