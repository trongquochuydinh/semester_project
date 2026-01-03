import { initManagementPage } from "../management_page.js";
import { ORDER_SCHEMA_MANAGE } from "../../schemas/schema_orders.js";
import { CREATE_ORDER_MODAL } from "../../modals/orders/modal_order_create.js";
import { EDIT_ORDER_MODAL } from "../../modals/orders/modal_order_edit.js";
import { ORDER_DETAILS_MODAL } from "../../modals/orders/modal_order_details.js";
import { cancelOrder } from "./order_handlers.js";
import { renderOrderActions } from "./order_actions.js";

initManagementPage({
  modals: [
    CREATE_ORDER_MODAL,
    ORDER_DETAILS_MODAL
  ],

  openActions: [
    {
      action: "open-create-order-modal",
      modalId: "createOrderModal"
    },
    {
      action: "edit-order",
      modalId: "editOrderModal",
      datasetKey: "orderId"
    },
    {
      action: "open-order-details",
      modalId: "orderDetailsModal",
      datasetKey: "orderId"
    }
  ],

  customActions: [
    {
      name: "cancel-order",
      handler: cancelOrder
    }
  ],

  table: {
    containerId: "orders-table",
    title: "Orders",
    schema: ORDER_SCHEMA_MANAGE,
    tableName: "orders",
    pageSize: 5,
    filters: {},
    actions: renderOrderActions
  }
});
