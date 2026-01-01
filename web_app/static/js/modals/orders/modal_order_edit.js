import { loadOrderData } from "./modal_order.loaders.js";
import { apiFetch } from "../../utils.js";

export const EDIT_ORDER_MODAL = {
  id: "editOrderModal",
  title: "Edit Order",

  fields: [
    {
      label: "Order Type",
      html: `
        <select id="order_type" class="form-select" required>
          <option value="purchase">Purchase</option>
          <option value="sale">Sale</option>
        </select>
      `
    }
  ],

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
        body: JSON.stringify({
          order_type: modal.querySelector("#order_type").value
        })
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
