import { apiFetch } from "../../utils.js";

export async function toggleOrder(orderId) {
  await apiFetch(`/orders/toggle_order_status/${orderId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orderId)
  });

  location.reload();
}
