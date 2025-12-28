import { createPaginatedTable } from "./elements/table.js";
import { USERS_SCHEMA_MANAGE } from "./schemas/schema_users.js";
import { registerAction } from "./elements/action.js";
import { createFormModal } from "./elements/modal.js";
import { CREATE_USER_MODAL } from "./modals/modal_user_create.js";
import { EDIT_USER_MODAL } from "./modals/modal_user_edit.js";
import { apiFetch } from "./utils.js";

document.addEventListener("DOMContentLoaded", () => {
  createFormModal(CREATE_USER_MODAL);
  createFormModal(EDIT_USER_MODAL);

  registerAction("open-create-user-modal", () => {
    const modalEl = document.getElementById("createUserModal");
    new bootstrap.Modal(modalEl).show();
  });

  registerAction("edit-user", (userId) => {
    const modalEl = document.getElementById("editUserModal");
    modalEl.dataset.userId = userId;
    new bootstrap.Modal(modalEl).show();
  });

  registerAction("disable-user", async (userId) => {
    const data = await apiFetch(`/users/disable/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userId)
    });

    if (!data.success) {
      alert(data.message);
    }
  });

  registerAction("enable-user", async (userId) => {
    const data = await apiFetch(`/users/enable/${userId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userId)
    });

    if (!data.success) {
      alert(data.message);
    }
  });

  const container = document.getElementById("users-table");

  if (container) {
    createPaginatedTable({
      container,
      title: "Users",
      schema: USERS_SCHEMA_MANAGE,
      tableName: "users",
      pageSize: 5,
      filters: {
        include_self: false   // management view
      },
      actions: (row) => {
        const isDisabled = row.is_active === false;

        return `
          <button 
            class="btn btn-sm btn-outline-primary"
            data-action="edit-user" 
            data-id="${row.id}">
            Edit
          </button>

          <button 
            class="btn btn-sm ${isDisabled ? "btn-outline-success" : "btn-outline-danger"} ms-2"
            data-action="${isDisabled ? "enable-user" : "disable-user"}"
            data-id="${row.id}">
            ${isDisabled ? "Enable" : "Disable"}
          </button>
        `;
      }
    });
  }
});
