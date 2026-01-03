import { apiFetch } from "../../utils.js";

export async function loadRoles(container) {
  const select = container.querySelector("#role");
  if (!select) return;

  select.innerHTML = "";

  const data = await apiFetch("/users/get_subroles");
  data.roles.forEach(role => {
    const opt = document.createElement("option");
    opt.value = role.name;
    opt.textContent = role.name;
    select.appendChild(opt);
  });
}

export async function loadCompanies(container) {
  const select = container.querySelector("#company");
  if (!select) return;

  select.innerHTML = "";

  const res = await apiFetch("/companies/get_companies");

  res.companies.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = c.name;
    select.appendChild(opt);
  });
}
