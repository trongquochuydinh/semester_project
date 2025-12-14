import { createTable } from "./elements/table.js";
import { USERS_SCHEMA_MANAGE } from "./schemas/schema_users.js";
import { registerAction } from "./elements/action.js";
import { createFormModal } from "./elements/modal.js";
import { CREATE_USER_MODAL } from "./modals/modal_user_create.js";
import { EDIT_USER_MODAL } from "./modals/modal_user_edit.js";


document.addEventListener("DOMContentLoaded", async () => {
    createFormModal(CREATE_USER_MODAL);
    createFormModal(EDIT_USER_MODAL);

    // register action so clicking the schema button opens modal
    registerAction("open-create-user-modal", () => {
      const modalEl = document.getElementById("createUserModal");
      new bootstrap.Modal(modalEl).show();
    });

    registerAction("edit-user", (userId) => {
      const modalEl = document.getElementById("editUserModal");
      modalEl.dataset.userId = userId;
      new bootstrap.Modal(modalEl).show();
    });

    const user_container = document.getElementById("users-table");

    if (user_container) {
      const resUsers = await fetch("/paginate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table_name: "users", limit: 5, offset: 0, filters: {} })
      });

      const users = await resUsers.json();
      createTable({
        title: "Users",
        element: user_container,
        schema: USERS_SCHEMA_MANAGE,
        rows: users.data,
          actions: (row) => `
            <button 
              class="btn btn-sm btn-outline-primary"
              data-action="edit-user" 
              data-id="${row.id}">
              Edit
            </button>

            <button 
              class="btn btn-sm btn-outline-danger ms-2"
              data-action="delete-user" 
              data-id="${row.id}">
              Delete
            </button>
          `
      });
    }
});
