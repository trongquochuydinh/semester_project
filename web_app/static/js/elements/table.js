import { apiFetch } from "../utils.js";

/* =========================================================
   INTERNAL: shared fetch + render logic
   ========================================================= */
async function renderTableFromFetcher({
  container,
  title,
  schema,
  actions,
  fetcher,
  afterRender
}) {
  const res = await fetcher();

  container.innerHTML = "";

  const card = createTable({
    title,
    element: container,
    schema,
    rows: res.data,
    actions
  });

  if (afterRender && typeof res.total === "number") {
    afterRender(res.total, card);
  }
}

/* =========================================================
   PAGINATED TABLE
   ========================================================= */
export function createPaginatedTable({
  container,
  title,
  schema,
  tableName,
  actions,
  filters = {},
  pageSize = 5
}) {
  let currentPage = 0;

  async function loadPage(page = 0) {
    currentPage = page;

    await renderTableFromFetcher({
      container,
      title,
      schema,
      actions,
      fetcher: () =>
        apiFetch(`/${tableName}/paginate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            limit: pageSize,
            offset: page * pageSize,
            filters
          })
        }),
      afterRender: renderPagination
    });
  }

  function renderPagination(total, card) {
    const totalPages = Math.ceil(total / pageSize);
    if (totalPages <= 1) return;

    let footer = card.querySelector(".card-footer");
    if (!footer) {
      footer = document.createElement("div");
      footer.className = "card-footer d-flex gap-1 justify-content-end";
      card.appendChild(footer);
    }

    footer.innerHTML = "";

    for (let i = 0; i < totalPages; i++) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = `btn btn-sm ${
        i === currentPage ? "btn-primary" : "btn-outline-primary"
      }`;
      btn.textContent = i + 1;
      btn.onclick = () => loadPage(i);
      footer.appendChild(btn);
    }
  }

  loadPage(0);
}

/* =========================================================
   ONE-SHOT TABLE FROM PAGINATE (NO PAGINATION UI)
   ========================================================= */
export async function createTableFromPaginate({
  container,
  title,
  schema,
  tableName,
  actions,
  filters = {},
  limit = 5
}) {
  await renderTableFromFetcher({
    container,
    title,
    schema,
    actions,
    fetcher: () =>
      apiFetch(`/${tableName}/paginate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          limit,
          offset: 0,
          filters
        })
      })
  });
}

/* =========================================================
   BASE TABLE (PURE RENDER)
   ========================================================= */
export function createTable({
  title,
  element,
  schema,
  rows,
  actions
}) {
  const col = document.createElement("div");
  col.className = "col-12";

  col.innerHTML = `
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5 class="mb-0">${title}</h5>
      ${schema.headerButton || ""}
    </div>

    <div class="card tbl-card">
      <div class="card-body p-0">
        <div class="table-scroll">
          <table class="table table-hover table-borderless mb-0">
            <thead>
              <tr>
                ${schema.columns.map(c => `<th>${c.label}</th>`).join("")}
              </tr>
            </thead>
            <tbody>
              ${rows.map(row => `
                <tr>
                  ${schema.columns.map(c => {
                    if (c.key === "__actions__") return `<td>${actions(row)}</td>`;
                    if (c.render) return `<td>${c.render(row[c.key], row)}</td>`;
                    return `<td>${row[c.key] ?? "—"}</td>`;
                  }).join("")}
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;

  element.appendChild(col);

  // return card so pagination footer can attach
  return col.querySelector(".card");
}
