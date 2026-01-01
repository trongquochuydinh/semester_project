import { ORDER_FIELDS } from "../../schemas/schema_orders.js";
import { extractOrderPayload } from "./modal_order.utils.js";
import { loadOrderData } from "./modal_order.loaders.js";
import { apiFetch } from "../../utils.js";

export const EDIT_ORDER_MODAL = {
  id: "editOrderModal",
  title: "Edit Order",
  fields: ORDER_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("editOrderModal");
    const orderId = modal.dataset.orderId;

    const order = await loadOrderData(modal, orderId);
    modal.querySelector("#order_type").value = order.order_type;
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editOrderModal");
    const orderId = modal.dataset.orderId;

    try {
      const data = await apiFetch(`/orders/edit/${orderId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractOrderPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Order updated successfully!</b>
        </div>
      `);
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
    }
  }
};
