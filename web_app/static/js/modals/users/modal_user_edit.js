import { USER_FIELDS } from "../../schemas/schema_users.js";
import { loadRoles, loadCompanies } from "./modal_user.loaders.js";
import { validateModal, extractUserPayload } from "./modal_user.utils.js";
import { apiFetch } from "../../utils.js";

async function populateUserData(userId) {
  const modal = document.getElementById("editUserModal");
  const user = await apiFetch(`/users/get/${userId}`);

  modal.querySelector("#username").value = user.username ?? "";
  modal.querySelector("#email").value = user.email ?? "";
  modal.querySelector("#role").value = user.role ?? "";
  modal.querySelector("#company").value = user.company_id ?? "";
}

export const EDIT_USER_MODAL = {
  id: "editUserModal",
  title: "Edit User",
  fields: USER_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("editUserModal");
    const userId = modal.dataset.userId;

    await loadRoles(modal);
    await loadCompanies(modal);

    if (userId) await populateUserData(userId);
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editUserModal");
    const userId = modal.dataset.userId;
    if (!validateModal(modal)) return;

    try {
      const data = await apiFetch(`/users/edit/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractUserPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return;
      }

      writeResult(`<div class="alert alert-success"><b>User updated successfully!</b></div>`);
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
    }
  }
};
