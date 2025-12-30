import { BASE_USER_MODAL, loadRoles, loadCompanies } from "./modal_user.js";
import { apiFetch } from "../utils.js";

export const EDIT_USER_MODAL = {
  id: "editUserModal",
  title: "Edit User",
  ...BASE_USER_MODAL,

  onLoad: async () => {
    const modal = document.getElementById("editUserModal");
    const userId = modal.dataset.userId;

    await loadRoles(modal);
    await loadCompanies(modal);

    if (userId) {
      await populateUserData(userId);
    }
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("editUserModal");
    const userId = modal.dataset.userId;

    const inputs = modal.querySelectorAll("input");
    for (const input of inputs) {
        if (!input.checkValidity()) {
        input.reportValidity();
        return;
        }
    }

    const payload = {
      username: modal.querySelector("#username").value,
      email: modal.querySelector("#email").value,
      role: modal.querySelector("#role").value,
      company_id: modal.querySelector("#company").value
    };

    try {
      const data = await apiFetch(`/users/edit/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to update user"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>User updated successfully!</b>
        </div>
      `);

    } catch (err) {
      console.error(err);
      writeResult(
        `<div class="text-danger">${err.message || "Unexpected error occurred."}</div>`
      );
    }
  }
};

async function populateUserData(userId) {
  try {
    const user = await apiFetch(`/users/get/${userId}`);
    const modal = document.getElementById("editUserModal");

    modal.querySelector("#username").value = user.username ?? "";
    modal.querySelector("#email").value = user.email ?? "";
    modal.querySelector("#role").value = user.role ?? "";
    modal.querySelector("#company").value = user.company_id ?? "";

  } catch (err) {
    console.error("Error loading user data:", err);
  }
}
