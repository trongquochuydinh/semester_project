import { ORDER_FIELDS } from "../../schemas/schema_orders.js";
import { extractOrderPayload, renderOrderItemActions } from "./modal_order.utils.js";
import { ORDER_SCHEMA_SELECT } from "../../schemas/schema_orders.js";
import { createPaginatedTable } from "../../elements/table.js";
import { apiFetch } from "../../utils.js";

export const CREATE_ORDER_MODAL = {
  id: "createOrderModal",
  title: "Create Order",
  fields: ORDER_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("createOrderModal");
    const container = modal.querySelector(".order-items-container");

    await createPaginatedTable({
      container,
      title: "Select Items",
      schema: ORDER_SCHEMA_SELECT,
      tableName: "items",
      pageSize: 5,
      actions: renderOrderItemActions
    });

    // ✅ Event delegation for checkbox ↔ quantity wiring
    container.addEventListener("change", (e) => {
      if (!e.target.classList.contains("order-item-check")) return;

      const id = e.target.dataset.itemId;
      const qty = container.querySelector(
        `.order-item-qty[data-item-id="${id}"]`
      );

      if (!qty) return;

      qty.disabled = !e.target.checked;
      if (!e.target.checked) qty.value = 1;
    });
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createOrderModal");

    // collect selected items
    const items = Array.from(
      modal.querySelectorAll(".order-item-check:checked")
    ).map(check => {
      const id = check.dataset.itemId;
      const qty = modal.querySelector(
        `.order-item-qty[data-item-id="${id}"]`
      ).value;

      return {
        item_id: Number(id),
        quantity: Number(qty)
      };
    });

    if (items.length === 0) {
      writeResult(`<div class="text-danger">Select at least one item.</div>`);
      return false;
    }

    try {
      const data = await apiFetch("/orders/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...extractOrderPayload(modal),
          items
        })
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return false;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>Order created successfully!</b>
        </div>
      `);
      return true;

    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
      return false;
    }
  }
};
