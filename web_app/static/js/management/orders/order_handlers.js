import { apiFetch } from "../../utils.js";

export async function cancelOrder(orderId) {
  await apiFetch(`/orders/cancel/${orderId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orderId)
  });

  location.reload();
}
