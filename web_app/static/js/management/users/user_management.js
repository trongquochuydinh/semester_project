import { initManagementPage } from "../management_page.js";
import { USERS_SCHEMA_MANAGE } from "../../schemas/schema_users.js";
import { CREATE_USER_MODAL } from "../../modals/users/modal_user_create.js";
import { EDIT_USER_MODAL } from "../../modals/users/modal_user_edit.js";
import { toggleUser } from "./user_handlers.js";
import { renderUserActions } from "./user_actions.js";
import { t } from "../../utils.js";

initManagementPage({
  modals: [
    CREATE_USER_MODAL,
    EDIT_USER_MODAL
  ],

  openActions: [
    {
      action: "open-create-user-modal",
      modalId: "createUserModal"
    },
    {
      action: "edit-user",
      modalId: "editUserModal",
      datasetKey: "userId"
    }
  ],

  customActions: [
    {
      name: "toggle-user",
      handler: toggleUser
    }
  ],

  table: {
    containerId: "users-table",
    title: t("Users"),
    schema: USERS_SCHEMA_MANAGE,
    tableName: "users",
    pageSize: 5,
    filters: { include_self: false },
    actions: renderUserActions
  }
});
