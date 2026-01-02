import { loadOrderData } from "./modal_order.loaders.js";
import { createPaginatedTable } from "../../elements/table.js";
import { ITEMS_SCHEMA_VIEW } from "../../schemas/schema_items.js"

export const ORDER_DETAILS_MODAL = {
  id: "orderDetailsModal",
  title: "Order Details",
  fields: [],

  onLoad: async () => {
    const modal = document.getElementById("orderDetailsModal");
    const orderId = modal.dataset.orderId;

    let container = modal.querySelector(".order-details-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "order-details-container";
      modal.querySelector(".modal-body").appendChild(container);
    }

    await createPaginatedTable({
      container,
      title: "Ordered Items",
      schema: ITEMS_SCHEMA_VIEW,
      tableName: `orders/${orderId}/items`,
      pageSize: 5,
      actions: () => ""
    });
  }
};
