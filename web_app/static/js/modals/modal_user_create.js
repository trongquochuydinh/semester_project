export const CREATE_USER_MODAL = {
  id: "createUserModal",
  title: "Create User",

  fields: [
    { label: "Username", html: `<input id="username" class="form-control">` },
    { label: "Email", html: `<input id="email" class="form-control">` },
    { label: "Role", html: `<select id="role" class="form-select"></select>` },
    { label: "Company", html: `<select id="company" class="form-select"></select>` }
  ],

  onLoad: async () => {
    await loadRoles();
    await loadCompanies();
  },

  onSubmit: async (writeResult) => {
    const payload = {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      role_id: document.getElementById("role").value,
      company_id: document.getElementById("company").value
    };

    try {
      const res = await fetch("/users/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      console.log("Backend response:", data); // 🔍 Helpful for debugging

      if (!res.ok || !data.success) {
        writeResult(`
          <div class="text-danger">${data.message || "Failed to create user"}</div>
        `);
        return;
      }

      // ⭐ Display initial password inside modal
      writeResult(`
        <div class="alert alert-success">
          <b>User created successfully!</b><br>
          <b>Password:</b> <code>${data.initial_password ?? "(none returned)"}</code>
        </div>
      `);

    } catch (err) {
      console.error("Create user error:", err);
      writeResult(`<div class="text-danger">Unexpected error occurred.</div>`);
    }
  }

};

export async function loadRoles() {
  const roleSelect = document.getElementById("role");
  if (!roleSelect) return;

  // Clear previous values
  roleSelect.innerHTML = "";

  try {
    const res = await fetch("/users/get_subroles");
    if (!res.ok) throw new Error("Failed to fetch roles");

    const data = await res.json();  // { roles: [...] }

    data.roles.forEach(role => {
      const opt = document.createElement("option");
      opt.value = role.id;
      opt.textContent = role.name;
      roleSelect.appendChild(opt);
    });

  } catch (err) {
    console.error("Error loading roles:", err);
  }
}


export async function loadCompanies() {
  const companySelect = document.getElementById("company");
  if (!companySelect) return;

  // Clear any previous content
  companySelect.innerHTML = "";

  try {
    // 1. Load companies from API
    const res = await fetch("/companies/get");
    if (!res.ok) throw new Error("Failed to fetch companies");
    const companies = await res.json();

    companies.forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      companySelect.appendChild(opt);
    });

    // 2. Load role & company_id from DOM <body>
    const pageData = document.getElementById("page-data");
    const role = pageData.dataset.role;
    const companyId = pageData.dataset.companyId;

    // 3. Apply restrictions for admin/manager
    if (role === "admin" || role === "manager") {
      companySelect.disabled = true;
      if (companyId) companySelect.value = companyId;
    } else {
      companySelect.disabled = false;
    }

  } catch (err) {
    console.error("Error loading companies:", err);
  }
}