/**
 * Generic table card builder
 * @param {Object} options
 * @param {string} options.title - Table title
 * @param {Array} options.columns - Array of { key, label }
 * @param {Array} options.rows - Array of objects
 * @returns {HTMLElement}
 */
function createTableCard({ title, columns, rows }) {
  const col = document.createElement("div");
  col.className = "col-md-12 col-xl-8";

  const headerHtml = columns.map(col => `<th>${col.label}</th>`).join("");
  const rowsHtml = rows.map(row => {
    const cells = columns.map(col => {

      if (col.key === "actions") {
        return `
          <td class="text-end">

            <button class="btn btn-sm btn-outline-primary me-2"
                    data-action="edit-user"
                    data-user-id="${row.id}">
              Edit
            </button>

            <button class="btn btn-sm btn-outline-danger"
                    data-action="delete-user"
                    data-user-id="${row.id}">
              Delete
            </button>

          </td>
        `;
      }

      return `<td>${row[col.key] ?? "—"}</td>`;
    }).join("");

    return `<tr>${cells}</tr>`;
  }).join("");

  col.innerHTML = `
    <h5 class="mb-3">${title}</h5>
    <div class="card tbl-card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover table-borderless mb-0">
            <thead>
              <tr>${headerHtml}</tr>
            </thead>
            <tbody>
              ${rowsHtml}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;

  return col;
}

function createUsersTableCardBase({ title, rows }) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "username", label: "Username" },
    { key: "email", label: "Email" },
    { key: "role_name", label: "Role" },
    { key: "company_name", label: "Company" }
  ];

  return createTableCard({ title, columns, rows });
}

function createUsersTableCardManage({ title, rows }) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "username", label: "Username" },
    { key: "email", label: "Email" },
    { key: "status", label: "Status" },
    { key: "role_name", label: "Role" },
    { key: "company_name", label: "Company" },
    { key: "actions", label: "Actions" }
  ];
  const col = createTableCard({ title, columns, rows });

  // Find the <h5> title
  const titleEl = col.querySelector("h5");
  if (!titleEl) return col;

  // Create the wrapper
  const wrapper = document.createElement("div");
  wrapper.className = "d-flex justify-content-between align-items-center mb-3";

  // Create the new title element (Bootstrap-friendly)
  const newTitle = document.createElement("h5");
  newTitle.className = "mb-0";   // no margin bottom because wrapper adds spacing
  newTitle.textContent = title;

  // Create the Create Admin button
  const btn = document.createElement("button");
  btn.className = "btn btn-primary btn-sm";
  btn.textContent = "Create User";
  btn.addEventListener("click", () => {
    const modalEl = document.getElementById("createUserModal");
    new bootstrap.Modal(modalEl).show();
  });

  // Build wrapper: [Title]    [Button]
  wrapper.appendChild(newTitle);
  wrapper.appendChild(btn);

  // Replace the original <h5> tag with the new wrapper
  titleEl.replaceWith(wrapper);

  return col;
}

function createCompaniesTableCard({ title, rows }) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "name", label: "Name" },
    { key: "field", label: "Field" },
  ];
  return createTableCard({ title, columns, rows });
}

function createItemsTableCard({ title, rows }) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "name", label: "Item Name" },
    { key: "category", label: "Category" },
    { key: "stock", label: "Stock" },
    { key: "price", label: "Price" }
  ];
  return createTableCard({ title, columns, rows });
}

function createOrdersTableCard({ title, rows }) {
  const columns = [
    { key: "id", label: "Order ID" },
    { key: "customer", label: "Customer" },
    { key: "product", label: "Product" },
    { key: "status", label: "Status" },
    { key: "amount", label: "Amount" }
  ];
  return createTableCard({ title, columns, rows });
}

document.addEventListener("click", async (e) => {

  // --- EDIT user ---
  if (e.target.matches("[data-action='edit-user']")) {
    const userId = e.target.dataset.userId;
    console.log("Edit user:", userId);
    showEditUserModal(userId);  // <- you will create this
  }

  // --- DELETE user ---
  if (e.target.matches("[data-action='delete-user']")) {
    const userId = e.target.dataset.userId;
    console.log("Delete user:", userId);
    showDeleteUserModal(userId); // <- also create
  }
});
