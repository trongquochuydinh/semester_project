export const BASE_ITEM_MODAL = {
  fields: [
    {
      label: "Name",
      html: `<input id="name" class="form-control">`
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
        >
      `
    },
  ]
};
