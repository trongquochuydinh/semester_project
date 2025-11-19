import { createTable } from "./elements/table.js";
import { USERS_SCHEMA_MANAGE, USERS_SCHEMA_ONLINE_VIEW } from "./schemas/schema_users.js";
import { COMPANIES_SCHEMA_VIEW } from "./schemas/schema_companies.js";

// =====================================
// Logout
// =====================================
document.getElementById("logout-link")?.addEventListener("click", (e) => {
  e.preventDefault();
  fetch("/logout", { method: "GET" })
    .then(() => window.location.href = "/")
    .catch(() => window.location.href = "/");
});

// =====================================
// Dashboard Logic
// =====================================
document.addEventListener("DOMContentLoaded", async () => {

  const user_container = document.getElementById("users-table");
  const company_container = document.getElementById("companies-table");

  const pageData = document.getElementById("page-data");
  const role = pageData.dataset.role;

  // -----------------------------
  // USERS SECTION
  // -----------------------------
  if (user_container) {
    const resUsers = await fetch("/paginate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        table_name: "users",
        limit: 5,
        offset: 0,
        filters: { status: "online" }
      })
    });

    const users = await resUsers.json();

    // show online user table
    createTable({
      title: "Online Users",
      element: user_container,
      schema: USERS_SCHEMA_ONLINE_VIEW,
      rows: users.data,
      actions: () => "" // no action column yet
    });
  }

  // -----------------------------
  // COMPANIES SECTION (superadmin only)
  // -----------------------------
  if (company_container && role === "superadmin") {
    const resCompanies = await fetch("/paginate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        table_name: "companies",
        limit: 5,
        offset: 0,
        filters: {}
      })
    });

    const companies = await resCompanies.json();


    createTable({
      title: "Companies",
      element: company_container,
      schema: COMPANIES_SCHEMA_VIEW,
      rows: companies.data,
      actions: () => "" // no action column yet
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

  try {
    const res = await fetch("/users/get_user_stats");
    if (!res.ok) throw new Error("Failed to load stats");

    const data = await res.json();

    const card = document.createElement("div");
    card.style.border = "1px solid #ccc";
    card.style.borderRadius = "10px";
    card.style.padding = "16px";
    card.style.margin = "8px 0";
    card.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
    card.style.width = "250px";

    card.innerHTML = `
      <h3 class="mb-2">User Statistics</h3>
      <p><b>Total Users:</b> ${data.total_users ?? "N/A"}</p>
      <p><b>Online Users:</b> ${data.online_users ?? "N/A"}</p>
    `;

    container.appendChild(card);

  } catch (err) {
    console.error("Error loading stats:", err);
    container.textContent = "Failed to load user statistics.";
    container.style.color = "red";
  }
}

document.addEventListener("DOMContentLoaded", loadUserStats);
