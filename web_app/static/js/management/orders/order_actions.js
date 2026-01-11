import { t } from "../../utils.js";

export function renderOrderActions(row) {
  let buttons = `
    <button 
      class="btn btn-sm btn-outline-secondary"
      data-action="open-order-details"
      data-id="${row.id}">
      ${t("Details")}
    </button>
  `;

  if (row.status === "pending") {
    buttons += `
      <button 
        class="btn btn-sm btn-outline-danger ms-2"
        data-action="cancel-order"
        data-id="${row.id}">
        ${t("Cancel")}
      </button>
    `;
  }

  return buttons;
}
