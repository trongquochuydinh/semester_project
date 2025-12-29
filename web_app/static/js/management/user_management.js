import { initManagementPage } from "./management_page.js";
import { USERS_SCHEMA_MANAGE } from "../schemas/schema_users.js";
import { CREATE_USER_MODAL } from "../modals/modal_user_create.js";
import { EDIT_USER_MODAL } from "../modals/modal_user_edit.js";
import { apiFetch } from "../utils.js";

initManagementPage({
  modals: [
    CREATE_USER_MODAL,
    EDIT_USER_MODAL
  ],

  openActions: [
    {
      action: "open-create-user-modal",
      modalId: "createUserModal"
    },
    {
      action: "edit-user",
      modalId: "editUserModal",
      datasetKey: "userId"
    }
  ],

  customActions: [
    {
      name: "toggle-user",
      handler: async (userId) => {
        const data = await apiFetch(
          `/users/toggle_user_is_active/${userId}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userId)
          }
        );

        alert(data.message);
        location.reload();
      }
    }
  ],

  table: {
    containerId: "users-table",
    title: "Users",
    schema: USERS_SCHEMA_MANAGE,
    tableName: "users",
    pageSize: 5,
    filters: { include_self: false },
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
          class="btn btn-sm ${
            isDisabled ? "btn-outline-success" : "btn-outline-danger"
          } ms-2"
          data-action="toggle-user"
          data-id="${row.id}">
          ${isDisabled ? "Enable" : "Disable"}
        </button>
      `;
    }
  }
});
