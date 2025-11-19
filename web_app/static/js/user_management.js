document.addEventListener("DOMContentLoaded", async () => {
    createUserFormModal();

    const user_container = document.getElementById("users-table");

    if (user_container) {
      const resUsers = await fetch("/paginate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table_name: "users", limit: 5, offset: 0, filters: {} })
      });
      const users = await resUsers.json();
      user_container.appendChild(
        createUsersTableCardManage({ title: "Users", rows: users.data })
      );
    }
});
