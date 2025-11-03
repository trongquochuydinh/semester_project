document.addEventListener("DOMContentLoaded", async () => {
  const roleSelect = document.getElementById("role");
  const companySelect = document.getElementById("company");
  
  // Get current user information
  let currentUser = null;
  try {
    const res = await fetch("/get_current_user");
    if (res.ok) {
      currentUser = await res.json();
    }
  } catch (err) {
    console.error("Error getting current user:", err);
  }

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
    const companies = await res.json();
    companies.forEach(company => {
      const option = document.createElement("option");
      option.value = company.id;
      option.textContent = company.name;
      companySelect.appendChild(option);
    });
    
    // Handle company select based on current user role
    if (currentUser && (currentUser.role === 'admin' || currentUser.role === 'manager')) {
      // Disable company select and set to current user's company
      companySelect.disabled = true;
      if (currentUser.company_id) {
        companySelect.value = currentUser.company_id;
      }
    }
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

    // If company select is disabled and user is admin/manager, use their company_id
    if (companySelect.disabled && currentUser && currentUser.company_id) {
      payload.company_id = currentUser.company_id;
    }

    try {
      const res = await fetch("/create_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to create user");

      const result = await res.json();

      if (result.success) {
        // Show password div
        const pwDiv = document.getElementById("password-display");
        const pwInput = document.getElementById("generated-password");
        pwInput.value = result.initial_password || "(not provided)";
        pwDiv.style.display = "block";
        alert("New admin was successfully created.")
      } else {
        alert("Failed: " + (result.message || "Unknown error"));
      }
    } catch (err) {
      console.error("Error creating user:", err);
      alert("Error creating user");
    }
  });
});
