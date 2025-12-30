import { apiFetch } from "../utils.js";

export const BASE_USER_MODAL = {
  fields: [
    { label: "Username", html: `<input id="username" class="form-control">` },
    { label: "Email", html: `<input type="email" id="email" class="form-control">` },
    { label: "Role", html: `<select id="role" class="form-select"></select>` },
    { label: "Company", html: `<select id="company" class="form-select"></select>` }
  ]
};

export async function loadRoles(container) {
  const roleSelect = container.querySelector("#role");
  if (!roleSelect) return;

  roleSelect.innerHTML = "";

  try {
    const data = await apiFetch("/users/get_subroles");

    data.roles.forEach(role => {
      const opt = document.createElement("option");
      opt.value = role.name;
      opt.textContent = role.name;
      roleSelect.appendChild(opt);
    });

  } catch (err) {
    console.error("Failed to load roles:", err);
  }
}

export async function loadCompanies(container) {
  const companySelect = container.querySelector("#company");
  if (!companySelect) return;

  companySelect.innerHTML = "";

  try {
    const companies = await apiFetch("/companies/get_companies");

    companies.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      opt.textContent = c.name;
      companySelect.appendChild(opt);
    });

  } catch (err) {
    console.error("Failed to load companies:", err);
  }
}
