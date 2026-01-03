export function renderCompanyActions(row) {
  return `
    <button 
      class="btn btn-sm btn-outline-primary"
      data-action="edit-company"
      data-id="${row.id}">
      Edit
    </button>

    <button 
      class="btn btn-sm btn-outline-danger ms-2"
      data-action="delete-company"
      data-id="${row.id}">
      Delete
    </button>
  `;
}
