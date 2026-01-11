import { t } from "../../utils.js";

export function renderCompanyActions(row) {
  return `
    <button 
      class="btn btn-sm btn-outline-primary"
      data-action="edit-company"
      data-id="${row.id}">
      ${t("Edit")}
    </button>

    <button 
      class="btn btn-sm btn-outline-danger ms-2"
      data-action="delete-company"
      data-id="${row.id}">
      ${t("Delete")}
    </button>
  `;
}
