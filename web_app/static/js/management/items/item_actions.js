import { t } from "../../utils.js";

export function renderItemActions(row) {
  const isInactive = row.is_active === "Discontinued";

  return `
    <button 
      class="btn btn-sm btn-outline-primary"
      data-action="edit-item"
      data-id="${row.id}">
      ${t("Edit")}
    </button>

    <button 
      class="btn btn-sm ${
        isInactive ? "btn-outline-success" : "btn-outline-danger"
      } ms-2"
      data-action="toggle-item"
      data-id="${row.id}">
      ${isInactive ? t("Activate") : t("Discontinue")}
    </button>
  `;
}
