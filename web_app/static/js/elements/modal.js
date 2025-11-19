export function createModal({ id, title, bodyHtml, footerHtml }) {
  const modal = document.createElement("div");
  modal.className = "modal fade";
  modal.id = id;
  modal.tabIndex = -1;

  modal.innerHTML = `
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">${title}</h5>
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">${bodyHtml}</div>

        <div class="modal-footer">${footerHtml}</div>

      </div>
    </div>
  `;

  document.body.appendChild(modal);
  return modal;
}


// More advanced: FORM MODAL with loader & submit support
export function createFormModal({
  id,
  title,
  fields,
  onLoad,
  onSubmit
}) {
  const bodyHtml = `
    <form id="${id}-form">
      ${fields.map(f => `
        <div class="mb-3">
          <label>${f.label}</label>
          ${f.html}
        </div>
      `).join("")}
    </form>

    <div id="${id}-result" class="alert alert-info mt-3" style="display:none"></div>
  `;

  const footerHtml = `
    <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button class="btn btn-primary" id="${id}-submit-btn">Save</button>
  `;

  createModal({ id, title, bodyHtml, footerHtml });

  const modalEl = document.getElementById(id);

  modalEl.addEventListener("shown.bs.modal", () => onLoad());

  // Helper for writing to result box
  function writeResult(html) {
    const box = document.getElementById(`${id}-result`);
    if (box) {
      box.innerHTML = html;
      box.style.display = "block";
    }
  }

  document.addEventListener("click", (e) => {
    if (e.target.id === `${id}-submit-btn`) {
      onSubmit(writeResult);   // pass callback
    }
  });
}
