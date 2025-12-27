import { apiFetch } from "../utils.js";

export function createPaginatedTable({
  container,
  title,
  schema,
  tableName,
  actions,
  filters = {},
  pageSize = 10
}) {
  let currentPage = 0;

  async function loadPage(page = 0) {
    currentPage = page;

    const res = await apiFetch(`/${tableName}/paginate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        limit: pageSize,
        offset: page * pageSize,
        filters
      })
    });

    container.innerHTML = "";

    createTable({
      title,
      element: container,
      schema,
      rows: res.data,
      actions
    });

    renderPagination(res.total);
  }

  function renderPagination(total) {
    const totalPages = Math.ceil(total / pageSize);

    let pagination = container.nextElementSibling;
    if (!pagination || !pagination.classList.contains("pagination-controls")) {
      pagination = document.createElement("div");
      pagination.className = "pagination-controls mt-3 d-flex gap-1";
      container.after(pagination);
    }

    pagination.innerHTML = "";

    for (let i = 0; i < totalPages; i++) {
      const btn = document.createElement("button");
      btn.className = `btn btn-sm ${
        i === currentPage ? "btn-primary" : "btn-outline-primary"
      }`;
      btn.textContent = i + 1;

      btn.onclick = () => loadPage(i);

      pagination.appendChild(btn);
    }
  }

  // initial load
  loadPage(0);
}

export function createTable({
  title,
  element,
  schema,
  rows,
  actions
}) {
  const col = document.createElement("div");
  col.className = "col-12";

  const header = `
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="mb-0">${title}</h5>
      ${schema.headerButton || ""}
    </div>
  `;

  const thead = `
    <thead>
      <tr>
        ${schema.columns.map(c => `<th>${c.label}</th>`).join("")}
      </tr>
    </thead>
  `;

  const tbody = `
    <tbody>
    ${rows.map(row => {
      return `
        <tr>
          ${schema.columns.map(c => {
            if (c.key === "__actions__") return `<td>${actions(row)}</td>`;
            if (c.render) return `<td>${c.render(row[c.key], row)}</td>`;
            return `<td>${row[c.key] ?? "—"}</td>`;
          }).join("")}
        </tr>
      `;
    }).join("")}
    </tbody>
  `;

  col.innerHTML = `
    ${header}
    <div class="card tbl-card">
      <div class="card-body">
        <table class="table table-hover table-borderless mb-0">
          ${thead}
          ${tbody}
        </table>
      </div>
    </div>
  `;

  element.appendChild(col);
}
