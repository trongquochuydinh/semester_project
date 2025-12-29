import { initManagementPage } from "./management_page.js";
import { ITEMS_SCHEMA_MANAGE } from "../schemas/schema_items.js";
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
    containerId: "items-table",
    title: "Items",
    schema: ITEMS_SCHEMA_MANAGE,
    tableName: "items",
    pageSize: 5,
    filters: { },
    actions: (row) => {

      return `
        <button 
          class="btn btn-sm btn-outline-primary"
          data-action="edit-user"
          data-id="${row.id}">
          Edit
        </button>

        <button 
          class="btn btn-sm btn-outline-danger ms-2"
          data-action="disable-item"
          data-id="${row.id}">
          Disable
        </button>
      `;
    }
  }
});
