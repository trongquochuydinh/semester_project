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
