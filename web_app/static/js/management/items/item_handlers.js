import { apiFetch } from "../../utils.js";

export async function toggleItem(itemId) {
  await apiFetch(`/items/toggle_item_is_active/${itemId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(itemId)
  });

  location.reload();
}
