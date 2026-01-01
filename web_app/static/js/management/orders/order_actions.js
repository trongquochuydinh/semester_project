export function renderOrderActions(row) {
  let buttons = `
    <button 
      class="btn btn-sm btn-outline-secondary"
      data-action="open-order-details"
      data-id="${row.id}">
      Details
    </button>
  `;

  if (row.status === "pending") {
    buttons += `
      <button 
        class="btn btn-sm btn-outline-primary ms-2"
        data-action="edit-order"
        data-id="${row.id}">
        Edit
      </button>

      <button 
        class="btn btn-sm btn-outline-danger ms-2"
        data-action="toggle-order"
        data-id="${row.id}">
        Cancel
      </button>
    `;
  }

  return buttons;
}
