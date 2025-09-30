
/**
 * Create a Bootstrap card for dashboard stats
 * @param {Object} options - Card config
 * @param {string} options.title - Small title (e.g. "Total Order")
 * @param {string|number} options.value - Main number (e.g. 18800)
 * @param {string} options.badgeText - Badge text (e.g. "27.4%")
 * @param {string} options.badgeColor - Badge color suffix (success, warning, danger)
 * @param {string} options.trendIcon - Icon class for trend (ti ti-trending-up / ti ti-trending-down)
 * @param {string} options.description - Extra description under the value
 * @returns {HTMLElement} - The card element
 */
function createStatCard({ title, value, badgeText, badgeColor, trendIcon, description }) {
  // Create wrapper col
  const col = document.createElement("div");
  col.className = "col-md-6 col-xl-3";

  col.innerHTML = `
    <div class="card">
      <div class="card-body">
        <h6 class="mb-2 f-w-400 text-muted">${title}</h6>
        <h4 class="mb-3">${value}
          <span class="badge bg-light-${badgeColor} border border-${badgeColor}">
            <i class="${trendIcon}"></i> ${badgeText}
          </span>
        </h4>
        <p class="mb-0 text-muted text-sm">${description}</p>
      </div>
    </div>
  `;

  return col;
}