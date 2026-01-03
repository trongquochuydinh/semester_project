import { apiFetch } from "../../utils.js";

export async function deleteCompany(companyId) {
  if (!confirm("Are you sure you want to delete this company?")) return;

  await apiFetch(`/companies/delete/${companyId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(companyId)
  });

  location.reload();
}