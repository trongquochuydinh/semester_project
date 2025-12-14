import { BASE_USER_MODAL, loadRoles, loadCompanies } from "./modal_user.js";

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

    const payload = {
      username: modal.querySelector("#username").value,
      email: modal.querySelector("#email").value,
      role_id: modal.querySelector("#role").value,
      company_id: modal.querySelector("#company").value
    };

    try {
      const res = await fetch(`/users/edit/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        writeResult(`<div class="text-danger">${data.message || "Failed to update user"}</div>`);
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>User updated successfully!</b>
        </div>
      `);

      setTimeout(() => location.reload(), 1500);

    } catch (err) {
      console.error(err);
      writeResult(`<div class="text-danger">Unexpected error occurred.</div>`);
    }
  }
};

async function populateUserData(userId) {
  try {
    const res = await fetch(`/users/get/${userId}`);
    if (!res.ok) throw new Error("Failed to fetch user data");

    const user = await res.json();
    const modal = document.getElementById("editUserModal");

    modal.querySelector("#username").value = user.username ?? "";
    modal.querySelector("#email").value = user.email ?? "";
    modal.querySelector("#role").value = user.role ?? "";
    modal.querySelector("#company").value = user.company_id ?? "";

  } catch (err) {
    console.error("Error loading user data:", err);
  }
}
