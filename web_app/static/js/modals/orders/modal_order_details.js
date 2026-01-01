import { loadOrderData } from "./modal_order.loaders.js";

export const ORDER_DETAILS_MODAL = {
  id: "orderDetailsModal",
  title: "Order Details",
  fields: [],

  onLoad: async () => {
    const modal = document.getElementById("orderDetailsModal");
    const orderId = modal.dataset.orderId;

    const order = await loadOrderData(modal, orderId);

    modal.querySelector(".modal-body").innerHTML = `
      <p><b>ID:</b> ${order.id}</p>
      <p><b>Status:</b> ${order.status}</p>
      <p><b>Total price:</b> ${order.total_price} CZK</p>
      <p><b>Created at:</b> ${order.created_at}</p>
    `;
  }
};
