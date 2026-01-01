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
