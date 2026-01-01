import { apiFetch } from "../../utils.js";

export async function loadOrderData(modal, orderId) {
  return await apiFetch(`/orders/get/${orderId}`);
}
