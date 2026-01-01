// modals/orders/modal_order.utils.js
export function extractOrderPayload(modal) {
  return {
    order_type: modal.querySelector("#order_type").value
  };
}


export function renderOrderItemActions(row) {
  return `
    <div class="d-flex align-items-center gap-2">
      <input
        type="checkbox"
        class="form-check-input order-item-check"
        data-item-id="${row.id}"
      >
      <input
        type="number"
        class="form-control form-control-sm order-item-qty"
        data-item-id="${row.id}"
        min="1"
        value="1"
        disabled
        style="width: 80px;"
      >
    </div>
  `;
}
