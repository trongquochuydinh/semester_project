import { createPaginatedTable } from "./elements/table.js";
import { t, apiFetch } from "./utils.js";
import { USERS_SCHEMA_ONLINE_VIEW } from "./schemas/schema_users.js";
import { COMPANIES_SCHEMA_VIEW } from "./schemas/schema_companies.js";

// =====================================
// Logout
// =====================================
document.getElementById("logout-link")?.addEventListener("click", (e) => {
  e.preventDefault();
  fetch("/logout", { method: "GET" })
    .then(() => (window.location.href = "/"))
    .catch(() => (window.location.href = "/"));
});

// =====================================
// Dashboard Logic
// =====================================
document.addEventListener("DOMContentLoaded", () => {
  const user_container = document.getElementById("users-table");
  const company_container = document.getElementById("companies-table");

  const pageData = document.getElementById("page-data");
  const role = pageData?.dataset.role;

  // -----------------------------
  // USERS SECTION (online users)
  // -----------------------------
  if (user_container) {
    createPaginatedTable({
      container: user_container,
      title: t("Online Users"),
      schema: USERS_SCHEMA_ONLINE_VIEW,
      tableName: "users",
      pageSize: 5,
      filters: {
        status: "online",
      },
      actions: () => ""     // no action column in dashboard
    });
  }

  // -----------------------------
  // COMPANIES SECTION (superadmin only)
  // -----------------------------
  if (company_container && role === "superadmin") {
    createPaginatedTable({
      container: company_container,
      title: t("Companies"),
      schema: COMPANIES_SCHEMA_VIEW,
      tableName: "companies",
      pageSize: 5,
      filters: {},
      actions: () => ""
    });
  }
});

// =====================================
// User Statistics (superadmin only)
// =====================================
async function loadUserStats() {
  const container = document.getElementById("stats-container");
  if (!container) return;

  container.innerHTML = "";

  const res = await apiFetch("/users/get_user_stats");

  const card = document.createElement("div");
  card.style.border = "1px solid #ccc";
  card.style.borderRadius = "10px";
  card.style.padding = "16px";
  card.style.margin = "8px 0";
  card.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
  card.style.width = "250px";

  card.innerHTML = `
    <h3 class="mb-2">${t("User Statistics")}</h3>
    <p><b>${t("Total Users")}:</b> ${res.total_users ?? "N/A"}</p>
    <p><b>${t("Online Users")}:</b> ${res.online_users ?? "N/A"}</p>
  `;

  container.appendChild(card);
}

document.addEventListener("DOMContentLoaded", loadUserStats);
