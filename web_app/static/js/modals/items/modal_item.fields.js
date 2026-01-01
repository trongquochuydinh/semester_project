export const ITEM_FIELDS = [
  {
    id: "name",
    label: "Name",
    html: `<input id="name" class="form-control" required>`
  },
  {
    id: "price",
    label: "Price",
    html: `
      <input
        id="price"
        type="number"
        class="form-control"
        min="0"
        step="0.01"
        required
      >
    `
  },
  {
    id: "quantity",
    label: "Quantity",
    html: `
      <input
        id="quantity"
        type="number"
        class="form-control"
        min="0"
        step="1"
        required
      >
    `
  }
];
