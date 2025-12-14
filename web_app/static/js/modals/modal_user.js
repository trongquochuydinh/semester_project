export const BASE_USER_MODAL = {
  fields: [
    { label: "Username", html: `<input id="username" class="form-control">` },
    { label: "Email", html: `<input id="email" class="form-control">` },
    { label: "Role", html: `<select id="role" class="form-select"></select>` },
    { label: "Company", html: `<select id="company" class="form-select"></select>` }
  ]
};

export async function loadRoles(container) {
  const roleSelect = container.querySelector("#role");
  if (!roleSelect) return;

  // Remove this problematic line:
  // if (roleSelect.options.length > 0) return;

  // Always clear and reload to ensure fresh options
  roleSelect.innerHTML = "";

  const res = await fetch("/users/get_subroles");
  const data = await res.json();

  data.roles.forEach(role => {
    const opt = document.createElement("option");
    opt.value = role.name;;
    opt.textContent = role.name;
    roleSelect.appendChild(opt);
  });
}
export async function loadCompanies(container) {
  const companySelect = container.querySelector("#company");
  if (!companySelect) return;

  companySelect.innerHTML = "";

  const res = await fetch("/companies/get");
  const companies = await res.json();

  companies.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = c.name;
    companySelect.appendChild(opt);
  });
}
