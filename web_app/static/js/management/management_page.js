import { createPaginatedTable } from "../elements/table.js";
import { registerAction } from "../elements/action.js";
import { createFormModal } from "../elements/modal.js";

export function initManagementPage(config) {
  const {
    modals = [],
    openActions = [],
    customActions = [],
    table
  } = config;

  document.addEventListener("DOMContentLoaded", () => {

    modals.forEach(createFormModal);

    // ---------------------------
    // Register open-modal actions
    // ---------------------------
    openActions.forEach(({ action, modalId, datasetKey }) => {
      registerAction(action, (id) => {
        const modalEl = document.getElementById(modalId);
        if (datasetKey && id !== undefined) {
          modalEl.dataset[datasetKey] = id;
        }
        new bootstrap.Modal(modalEl).show();
      });
    });

    // ---------------------------
    // Custom actions (API calls, etc.)
    // ---------------------------
    customActions.forEach(({ name, handler }) => {
      registerAction(name, handler);
    });

    // ---------------------------
    // Table
    // ---------------------------
    const container = document.getElementById(table.containerId);

    if (container) {
      createPaginatedTable({
        container,
        title: table.title,
        schema: table.schema,
        tableName: table.tableName,
        pageSize: table.pageSize ?? 10,
        filters: table.filters ?? {},
        actions: table.actions
      });
    }
  });
}
