export function validateCompanyModal(modal) {
  const inputs = modal.querySelectorAll("input");
  for (const input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return false;
    }
  }
  return true;
}

export function extractCompanyPayload(modal) {
  return {
    company_name: modal.querySelector("#company_name").value,
    field: modal.querySelector("#field").value
  };
}
