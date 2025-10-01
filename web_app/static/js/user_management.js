document.addEventListener("DOMContentLoaded", async () => {
  const roleSelect = document.getElementById("role");
  const companySelect = document.getElementById("company");

  // Fetch roles
  try {
    const res = await fetch("/get_roles");
    if (!res.ok) throw new Error("Failed to fetch roles");
    const data = await res.json(); // matches your FastAPI RolesResponse
    data.roles.forEach(role => {
      const option = document.createElement("option");
      option.value = role.id;
      option.textContent = role.name;
      roleSelect.appendChild(option);
    });
  } catch (err) {
    console.error("Error loading roles:", err);
  }

  // Fetch companies
  try {
    const res = await fetch("/get_companies");
    if (!res.ok) throw new Error("Failed to fetch companies");
    const companies = await res.json(); // matches your FastAPI CompanyResponse[]
    companies.forEach(company => {
      const option = document.createElement("option");
      option.value = company.id;
      option.textContent = company.name;
      companySelect.appendChild(option);
    });
  } catch (err) {
    console.error("Error loading companies:", err);
  }

  // Handle form submission
  document.getElementById("create-user-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    role_id: parseInt(roleSelect.value, 10),
    company_id: parseInt(companySelect.value, 10),
    };

    console.log("Creating user:", payload);

    try {
      const res = await fetch("/create_user", { // adjust endpoint if needed
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to create user");
      alert("User created successfully!");
    } catch (err) {
      console.error("Error creating user:", err);
      alert("Error creating user");
    }
  });
});
