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
      name: "toggle-item",
      handler: async (itemId) => {
        const data = await apiFetch(
          `/items/toggle_item_is_active/${itemId}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(itemId)
          }
        );

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

      const isDisabled = row.is_active === "Discontinued";

      return `
        <button 
          class="btn btn-sm btn-outline-primary"
          data-action="edit-item"
          data-id="${row.id}">
          Edit
        </button>

        <button 
          class="btn btn-sm ${
            isDisabled ? "btn-outline-success" : "btn-outline-danger"
          } ms-2"
          data-action="toggle-item"
          data-id="${row.id}">
          ${isDisabled ? "Activate" : "Discontinue"}
        </button>
      `;
    }
  }
});
