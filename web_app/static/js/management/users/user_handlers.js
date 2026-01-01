import { apiFetch } from "../../utils.js";

export async function toggleUser(userId) {
  await apiFetch(`/users/toggle_user_is_active/${userId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userId)
  });

  location.reload();
}
