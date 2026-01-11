import { t } from "../utils.js";

export const USERS_SCHEMA_MANAGE = {
  columns: [
    { key: "id", label: "ID" },
    { key: "username", label: t("username") },
    { key: "email", label: t("email") },
    { key: "status", label: t("Status") },
    { key: "role_name", label: t("role") },
    { key: "company_name", label: t("company") },
    { key: "__actions__", label: t("actions") }
  ],

  headerButton: `
    <button class="btn btn-primary btn-sm" data-action="open-create-user-modal">
      ${t("CreateUser")}
    </button>
  `
};

export const USERS_SCHEMA_ONLINE_VIEW = {
  columns: [
    { key: "id", label: "ID" },
    { key: "username", label: t("username") },
    { key: "email", label: t("email") },
    { key: "status", label: t("Status") },
    { key: "role_name", label: t("role") },
    { key: "company_name", label: t("company") },
  ],
  headerButton: ""
};

export const USER_FIELDS = [
  {
    id: "username",
    label: t("username"),
    html: `<input id="username" class="form-control" required>`
  },
  {
    id: "email",
    label: t("email"),
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
    label: t("role"),
    html: `<select id="role" class="form-select" required></select>`
  },
  {
    id: "company",
    label: t("company"),
    html: `<select id="company" class="form-select" required></select>`
  }
];
