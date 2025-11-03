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
  const rowsHtml = rows.map(row => `
    <tr>
      ${columns.map(col => `<td>${row[col.key] ?? "—"}</td>`).join("")}
    </tr>
  `).join("");

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

function createUsersTableCard({ title, rows }) {
  const columns = [
    { key: "id", label: "ID" },
    { key: "username", label: "Username" },
    { key: "email", label: "Email" },
    { key: "role_name", label: "Role" },
    { key: "company_name", label: "Company" }
  ];
  return createTableCard({ title, columns, rows });
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
