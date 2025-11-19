function createModal({ id, title, bodyHtml, footerHtml }) {
  const modal = document.createElement("div");
  modal.className = "modal fade";
  modal.id = id;
  modal.tabIndex = -1;
  modal.innerHTML = `
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">${title}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          ${bodyHtml}
        </div>

        <div class="modal-footer">
          ${footerHtml}
        </div>

      </div>
    </div>
  `;

  document.body.appendChild(modal);
  return modal;
}


function createUserFormModal() {

  // 1️⃣ Create modal from template
  createModal({
    id: "createUserModal",
    title: "Create User",
    bodyHtml: `
      <form id="create-user-form">

        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" class="form-control" id="username" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" id="email" required>
        </div>

        <div class="mb-3">
          <label class="form-label">Role</label>
          <select class="form-select" id="role"></select>
        </div>

        <div class="mb-3">
          <label class="form-label">Company</label>
          <select class="form-select" id="company"></select>
        </div>

        <div id="password-display" class="mt-3" style="display:none;">
          <strong>Initial password:</strong>
          <input id="generated-password" readonly class="form-control mt-1" />
        </div>

      </form>
    `,
    footerHtml: `
      <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      <button class="btn btn-primary" id="submit-admin-btn">Create</button>
    `
  });

  // 2️⃣ Populate roles + companies when modal is shown
  const modalEl = document.getElementById("createUserModal");

  modalEl.addEventListener("shown.bs.modal", async () => {
    const roleSelect = document.getElementById("role");
    const companySelect = document.getElementById("company");

    roleSelect.innerHTML = "";
    companySelect.innerHTML = "";

    // Get current user
    let currentUser = null;
    try {
      const res = await fetch("/get_current_user");
      if (res.ok) currentUser = await res.json();
    } catch {}

    // Load roles
    try {
      const res = await fetch("/users/get_subroles");
      const data = await res.json();
      data.roles.forEach(role => {
        const opt = document.createElement("option");
        opt.value = role.id;
        opt.textContent = role.name;
        roleSelect.appendChild(opt);
      });
    } catch (err) {
      console.error("Error loading roles:", err);
    }

    // Load companies
    try {
      const res = await fetch("/companies/get");
      const companies = await res.json();
      companies.forEach(company => {
        const opt = document.createElement("option");
        opt.value = company.id;
        opt.textContent = company.name;
        companySelect.appendChild(opt);
      });

      // Auto-lock for admins/managers
      if (currentUser && ["admin", "manager"].includes(currentUser.role)) {
        companySelect.disabled = true;
        companySelect.value = currentUser.company_id;
      } else {
        companySelect.disabled = false;
      }
    } catch (err) {
      console.error("Error loading companies:", err);
    }
  });

  // 3️⃣ Submit handler
  document.addEventListener("click", async (e) => {
    if (e.target && e.target.id === "submit-admin-btn") {
      const username = document.getElementById("username").value;
      const email = document.getElementById("email").value;
      const role_id = parseInt(document.getElementById("role").value);
      const company_id = parseInt(document.getElementById("company").value);

      const payload = { username, email, role_id, company_id };

      try {
        const res = await fetch("/users/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const result = await res.json();

        if (!result.success) {
          alert("Failed: " + (result.message || "Unknown error"));
          return;
        }

        document.getElementById("generated-password").value = result.initial_password;
        document.getElementById("password-display").style.display = "block";

      } catch (err) {
        console.error("Error creating user:", err);
      }
    }
  });
}
