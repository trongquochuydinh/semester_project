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

export const USER_FIELDS = [
  {
    id: "username",
    label: "Username",
    html: `<input id="username" class="form-control" required>`
  },
  {
    id: "email",
    label: "Email",
    html: `
      <input
        type="email"
        id="email"
        class="form-control"
        placeholder="user@example.com"
        required
      >
    `
  },
  {
    id: "role",
    label: "Role",
    html: `<select id="role" class="form-select" required></select>`
  },
  {
    id: "company",
    label: "Company",
    html: `<select id="company" class="form-select" required></select>`
  }
];
