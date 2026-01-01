import { initManagementPage } from "../management_page.js";
import { ITEMS_SCHEMA_MANAGE } from "../../schemas/schema_items.js";
import { CREATE_ITEM_MODAL } from "../../modals/items/modal_item_create.js";
import { EDIT_ITEM_MODAL } from "../../modals/items/modal_item_edit.js";
import { toggleItem } from "./item_handlers.js";
import { renderItemActions } from "./item_actions.js";

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
      handler: toggleItem
    }
  ],

  table: {
    containerId: "items-table",
    title: "Items",
    schema: ITEMS_SCHEMA_MANAGE,
    tableName: "items",
    pageSize: 5,
    filters: {},
    actions: renderItemActions
  }
});
