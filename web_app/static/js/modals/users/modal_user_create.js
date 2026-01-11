import { USER_FIELDS } from "../../schemas/schema_users.js";
import { loadRoles, loadCompanies } from "./modal_user.loaders.js";
import { validateModal, extractUserPayload } from "./modal_user.utils.js";
import { t, apiFetch } from "../../utils.js";

export const CREATE_USER_MODAL = {
  id: "createUserModal",
  title: t("CreateUser"),
  fields: USER_FIELDS,

  onLoad: async () => {
    const modal = document.getElementById("createUserModal");
    await loadRoles(modal);
    await loadCompanies(modal);
  },

  onSubmit: async (writeResult) => {
    const modal = document.getElementById("createUserModal");
    if (!validateModal(modal)) return false;

    try {
      const data = await apiFetch("/users/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractUserPayload(modal))
      });

      if (!data.success) {
        writeResult(`<div class="text-danger">${data.message}</div>`);
        return false;
      }

      writeResult(`
        <div class="alert alert-success">
          <b>User created successfully!</b><br>
          <b>Password:</b> <code>${data.initial_password}</code>
        </div>
      `);
      return true;
    } catch (err) {
      writeResult(`<div class="text-danger">${err.message}</div>`);
      return false;
    }
  }
};
