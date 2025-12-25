import { BASE_USER_MODAL, loadRoles, loadCompanies } from "./modal_user.js";
import { apiFetch } from "../utils.js";

export const CREATE_USER_MODAL = {
  id: "createUserModal",
  title: "Create User",
  ...BASE_USER_MODAL,

  onLoad: async () => {
    const modal = document.getElementById("createUserModal");
    await loadRoles(modal);
    await loadCompanies(modal);
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createUserModal");

    const payload = {
      username: modal.querySelector("#username").value,
      email: modal.querySelector("#email").value,
      role: modal.querySelector("#role").value,
      company_id: modal.querySelector("#company").value
    };

    try {
      const data = await apiFetch("/users/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!data.success) {
        writeResult(
          `<div class="text-danger">${data.message || "Failed to create user"}</div>`
        );
        return;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>User created successfully!</b><br>
          <b>Password:</b> <code>${data.initial_password}</code>
        </div>
      `);

    } catch (err) {
      console.error(err);
      writeResult(`<div class="text-danger">${err.message || "Unexpected error occurred."}</div>`);
    }
  }
};
