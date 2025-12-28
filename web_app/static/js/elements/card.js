export function createStatCard({
  container,
  title,
  value,
  badgeText,
  badgeColor,
  trendIcon,
  description
}) {
  if (!container) {
    throw new Error("createStatCard: container is required");
  }

  const col = document.createElement("div");
  col.className = "col-md-6 col-xl-3 mb-3";

  col.innerHTML = `
    <div class="card h-100">
      <div class="card-body py-4 text-center">

        <h5 class="mb-3 f-w-400 text-muted">${title}</h5>

        <div class="d-flex justify-content-center align-items-center mb-3">
          <span class="fw-bold" style="font-size: 2.25rem;">
            ${value}
          </span>
        </div>

        ${
          description
            ? `<p class="mb-0 text-muted text-sm">${description}</p>`
            : ""
        }

      </div>
    </div>
  `;

  container.appendChild(col);
}
