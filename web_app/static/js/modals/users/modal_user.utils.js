export function validateModal(modal) {
  const inputs = modal.querySelectorAll("input, select");
  for (const el of inputs) {
    if (!el.checkValidity()) {
      el.reportValidity();
      return false;
    }
  }
  return true;
}

export function extractUserPayload(modal) {
  return {
    username: modal.querySelector("#username").value,
    email: modal.querySelector("#email").value,
    role: modal.querySelector("#role").value,
    company_id: modal.querySelector("#company").value
  };
}
