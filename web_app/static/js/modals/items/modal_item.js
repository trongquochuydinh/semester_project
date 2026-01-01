export const BASE_ITEM_MODAL = {
  fields: [
    {
      label: "Name",
      html: `<input id="name" class="form-control" required>`
    },
    {
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
    },
  ]
};
