export const USERS_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "username", label: "Username" },
    { key: "email", label: "Email" },
    { key: "status", label: "Status" },
    { key: "role_name", label: "Role" },
    { key: "company_name", label: "Company" },
    { key: "__actions__", label: "Actions" }
  ],

  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-user-modal">
      Create User
    </button>
  `
};

export const USERS_SCHEMA_ONLINE_VIEW = {
  columns: [
    { key: "id", label: "ID" },
    { key: "username", label: "Username" },
    { key: "email", label: "Email" },
    { key: "status", label: "Status" },
    { key: "role_name", label: "Role" },
    { key: "company_name", label: "Company" }
  ],
  headerButton: ""
};

