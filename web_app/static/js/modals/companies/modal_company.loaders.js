import { apiFetch } from "../../utils.js";

export async function loadCompanyData(modal, companyId) {
  const company = await apiFetch(`/companies/get/${companyId}`);

  modal.querySelector("#company_name").value = company.company_name ?? "";
  modal.querySelector("#field").value = company.field ?? "";
}
