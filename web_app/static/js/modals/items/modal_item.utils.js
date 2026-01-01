export function validateInputs(modal) {
  const inputs = modal.querySelectorAll("input");
  for (const input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return false;
    }
  }
  return true;
}

export function extractPayload(modal, keys) {
  return keys.reduce((acc, key) => {
    acc[key] = modal.querySelector(`#${key}`).value;
    return acc;
  }, {});
}

export function renderSuccess(writeResult, message) {
  writeResult(`
    <div class="alert alert-success">
      <b>${message}</b>
    </div>
  `);
}

export function renderError(writeResult, message) {
  writeResult(`
    <div class="text-danger">${message}</div>
  `);
}
