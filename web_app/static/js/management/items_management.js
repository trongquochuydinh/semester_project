import { initManagementPage } from "./management_page.js";
import { ITEMS_SCHEMA_MANAGE } from "../schemas/schema_items.js";
import { CREATE_ITEM_MODAL } from "../modals/modal_items_create.js";
import { EDIT_ITEM_MODAL } from "../modals/modal_items_edit.js";
import { apiFetch } from "../utils.js";

initManagementPage({
  modals: [
    CREATE_ITEM_MODAL,
    EDIT_ITEM_MODAL
  ],

  openActions: [
    {
      action: "open-create-item-modal",
      modalId: "createItemModal"
    },
    {
      action: "edit-item",
      modalId: "editItemModal",
      datasetKey: "itemId"
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
          data-action="edit-item"
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
