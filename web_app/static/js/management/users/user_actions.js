export function renderUserActions(row) {
  const isDisabled = row.is_active === false;

  return `
    <button 
      class="btn btn-sm btn-outline-primary"
      data-action="edit-user"
      data-id="${row.id}">
      Edit
    </button>

    <button 
      class="btn btn-sm ${
        isDisabled ? "btn-outline-success" : "btn-outline-danger"
      } ms-2"
      data-action="toggle-user"
      data-id="${row.id}">
      ${isDisabled ? "Enable" : "Disable"}
    </button>
  `;
}
