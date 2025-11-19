// =====================================
// Logout
// =====================================
document.getElementById('logout-link').addEventListener('click', function(e) {
  e.preventDefault();
  fetch('/logout', { method: 'GET' })
    .then(() => window.location.href = '/')
    .catch(() => window.location.href = '/');
});

// =====================================
// Dashboard Logic (modal + tables)
// =====================================

document.addEventListener("DOMContentLoaded", async () => {
  const user_container = document.getElementById("users-table");
  const company_container = document.getElementById("companies-table");
  // const pageData = document.getElementById("page-data");
  // const role = pageData.dataset.role
  // -----------------------------
  // USERS SECTION
  // -----------------------------
  if (user_container) {
    const resUsers = await fetch("/paginate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ table_name: "users", limit: 5, offset: 0, filters: {"status": "online"} })
    });
    const users = await resUsers.json();
    user_container.appendChild(
      createUsersTableCardBase({ title: "Online Users", rows: users.data })
    );
  }

  // -----------------------------
  // COMPANIES SECTION
  // -----------------------------
  if (company_container) {
    const resCompanies = await fetch("/paginate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ table_name: "companies", limit: 5, offset: 0, filters: {} })
    });

    const companies = await resCompanies.json();
    company_container.appendChild(
      createCompaniesTableCard({ title: "Companies", rows: companies.data })
    );
  }
});

async function loadUserStats() {
  const container = document.getElementById("stats-container");
  if (container) {
    container.innerHTML = ""; // Clear previous content

    try {
      // ✅ Only one request needed now
      const res = await fetch("/users/get_user_stats");
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json(); // expected: { total_users: X, online_users: Y }

      // ✅ Create a simple card
      const card = document.createElement("div");
      card.style.border = "1px solid #ccc";
      card.style.borderRadius = "10px";
      card.style.padding = "16px";
      card.style.margin = "8px 0";
      card.style.boxShadow = "0 2px 6px rgba(0,0,0,0.1)";
      card.style.width = "250px";
      card.style.fontFamily = "Arial, sans-serif";

      card.innerHTML = `
        <h3 style="margin: 0 0 8px;">User Statistics</h3>
        <p><b>Total Users:</b> ${data.total_users ?? "N/A"}</p>
        <p><b>Online Users:</b> ${data.online_users ?? "N/A"}</p>
      `;

      container.appendChild(card);
    } catch (err) {
      console.error("Error loading user stats:", err);
      const errorMsg = document.createElement("div");
      errorMsg.textContent = "Failed to load user statistics.";
      errorMsg.style.color = "red";
      container.appendChild(errorMsg);
    }
  }
}

document.addEventListener("DOMContentLoaded", loadUserStats);
