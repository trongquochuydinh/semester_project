import { createTable } from "./elements/table.js";
import { USERS_SCHEMA_MANAGE } from "./schemas/schema_users.js";
import { registerAction } from "./elements/action.js";
import { createFormModal } from "./elements/modal.js";
import { CREATE_USER_MODAL } from "./modals/modal_user_create.js";
import { EDIT_USER_MODAL } from "./modals/modal_user_edit.js";
import { apiFetch } from "./utils.js";

const PAGE_SIZE = 5;
let currentPage = 0;

async function loadUsers(page = 0) {
  const user_container = document.getElementById("users-table");
  if (!user_container) return;

  const users = await apiFetch("/paginate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      table_name: "users",
      limit: PAGE_SIZE,
      offset: page * PAGE_SIZE,
      filters: {}
    })
  });

  user_container.innerHTML = "";

  createTable({
    title: "Users",
    element: user_container,
    schema: USERS_SCHEMA_MANAGE,
    rows: users.data,
    actions: (row) => `
      <button 
        class="btn btn-sm btn-outline-primary"
        data-action="edit-user" 
        data-id="${row.id}">
        Edit
      </button>

      <button 
        class="btn btn-sm btn-outline-danger ms-2"
        data-action="delete-user" 
        data-id="${row.id}">
        Delete
      </button>
    `
  });

  renderPagination(users.total);
}

function renderPagination(total) {
  const totalPages = Math.ceil(total / PAGE_SIZE);
  let pagination = document.getElementById("users-pagination");

  if (!pagination) {
    pagination = document.createElement("div");
    pagination.id = "users-pagination";
    pagination.className = "mt-3 d-flex gap-1";
    document.getElementById("users-table").after(pagination);
  }

  pagination.innerHTML = "";

  for (let i = 0; i < totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = `btn btn-sm ${
      i === currentPage ? "btn-primary" : "btn-outline-primary"
    }`;
    btn.textContent = i + 1;

    btn.onclick = () => {
      currentPage = i;
      loadUsers(currentPage);
    };

    pagination.appendChild(btn);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  createFormModal(CREATE_USER_MODAL);
  createFormModal(EDIT_USER_MODAL);

  registerAction("open-create-user-modal", () => {
    const modalEl = document.getElementById("createUserModal");
    new bootstrap.Modal(modalEl).show();
  });

  registerAction("edit-user", (userId) => {
    const modalEl = document.getElementById("editUserModal");
    modalEl.dataset.userId = userId;
    new bootstrap.Modal(modalEl).show();
  });

  await loadUsers(0);
});
