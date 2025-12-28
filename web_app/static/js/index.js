import { createPaginatedTable } from "./elements/table.js";
import { t, apiFetch } from "./utils.js";
import { USERS_SCHEMA_ONLINE_VIEW } from "./schemas/schema_users.js";
import { COMPANIES_SCHEMA_VIEW } from "./schemas/schema_companies.js";
import { createDonutStat } from "./elements/donut_stat.js";
import { createStatCard } from "./elements/card.js"

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

  const total = res.total_users ?? 0;
  const online = res.online_users ?? 0;

  createDonutStat({
    container,
    title: t("Online Users"),
    value: online,
    total: total,
    label: t("users online"),
    color: "#28a745"
  });


  createStatCard({
    container,
    title: t("Orders made"),
    value: 128,
    badgeText: "+12%",
    badgeColor: "success",
    trendIcon: "ti ti-trending-up",
    description: t("this week")
  });

  createStatCard({
    container,
    title: t("Items sold"),
    value: 128,
    badgeText: "+12%",
    badgeColor: "success",
    trendIcon: "ti ti-trending-up",
    description: t("this week")
  });
}

document.addEventListener("DOMContentLoaded", loadUserStats);
