import { initManagementPage } from "../management_page.js";
import { COMPANIES_SCHEMA_MANAGE } from "../../schemas/schema_companies.js";
import { CREATE_COMPANY_MODAL } from "../../modals/companies/modal_company_create.js";
import { EDIT_COMPANY_MODAL } from "../../modals/companies/modal_company_edit.js";
import { deleteCompany } from "./company_handers.js";
import { renderCompanyActions } from "./company_actions.js";
import { t } from "../../utils.js";

initManagementPage({
  modals: [
    CREATE_COMPANY_MODAL,
    EDIT_COMPANY_MODAL
  ],

  openActions: [
    {
      action: "open-create-company-modal",
      modalId: "createCompanyModal"
    },
    {
      action: "edit-company",
      modalId: "editCompanyModal",
      datasetKey: "companyId"
    }
  ],

  customActions: [
    {
      name: "delete-company",
      handler: deleteCompany
    }
  ],

  table: {
    containerId: "companies-table",
    title: t("Companies"),
    schema: COMPANIES_SCHEMA_MANAGE,
    tableName: "companies",
    pageSize: 10,
    filters: {},
    actions: renderCompanyActions
  }
});
