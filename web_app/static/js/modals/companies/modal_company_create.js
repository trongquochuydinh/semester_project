import { COMPANY_FIELDS } from "../../schemas/schema_companies.js";
import { validateCompanyModal, extractCompanyPayload } from "./modal_company.utils.js";
import { t, apiFetch } from "../../utils.js";

export const CREATE_COMPANY_MODAL = {
  id: "createCompanyModal",
  title: t("CreateCompany"),
  fields: COMPANY_FIELDS,

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createCompanyModal");
    if (!validateCompanyModal(modal)) return false;

    try {
      const data = await apiFetch("/companies/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractCompanyPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return false;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Company created successfully!</b>
        </div>
      `);
      return true;
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
      return false;
    }
  }
};
