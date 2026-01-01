import { apiFetch } from "../../utils.js";

export async function loadItemData(modal, itemId) {
  const item = await apiFetch(`/items/get/${itemId}`);

  modal.querySelector("#name").value = item.name ?? "";
  modal.querySelector("#price").value = item.price ?? "";
  modal.querySelector("#quantity").value = item.quantity ?? "";
}
