import { apiFetch } from "../../utils.js";

export const CREATE_ORDER_MODAL = {
  id: "createOrderModal",
  title: "Create Order",

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

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createOrderModal");

    try {
      const data = await apiFetch("/orders/create", {
        method: "POST",
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
          <b>Order created successfully!</b>
        </div>
      `);
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
    }
  }
};
