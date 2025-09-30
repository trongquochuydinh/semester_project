// dashboard-ui.js

/**
 * Create a visitor chart card with Month/Week tabs
 * @param {Object} options
 * @param {string} options.title - Title text (e.g. "Unique Visitor")
 * @param {string} options.chartIdMonth - ID for month chart container
 * @param {string} options.chartIdWeek - ID for week chart container
 * @param {Object} options.chartOptionsMonth - ApexCharts config for month view
 * @param {Object} options.chartOptionsWeek - ApexCharts config for week view
 * @returns {{element: HTMLElement, initCharts: Function}}
 */
function createVisitorChartCard({ 
  title, 
  chartIdMonth, 
  chartIdWeek, 
  chartOptionsMonth, 
  chartOptionsWeek 
}) {
  const col = document.createElement("div");
  col.className = "col-md-12 col-xl-8";

  col.innerHTML = `
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h5 class="mb-0">${title}</h5>
      <ul class="nav nav-pills justify-content-end mb-0" id="chart-tab-tab" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link" id="chart-tab-home-tab" data-bs-toggle="pill" 
            data-bs-target="#chart-tab-home" type="button" role="tab" 
            aria-controls="chart-tab-home" aria-selected="true">Month</button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link active" id="chart-tab-profile-tab" data-bs-toggle="pill" 
            data-bs-target="#chart-tab-profile" type="button" role="tab" 
            aria-controls="chart-tab-profile" aria-selected="false">Week</button>
        </li>
      </ul>
    </div>
    <div class="card">
      <div class="card-body">
        <div class="tab-content" id="chart-tab-tabContent">
          <div class="tab-pane" id="chart-tab-home" role="tabpanel" 
               aria-labelledby="chart-tab-home-tab" tabindex="0">
            <div id="${chartIdMonth}"></div>
          </div>
          <div class="tab-pane show active" id="chart-tab-profile" role="tabpanel" 
               aria-labelledby="chart-tab-profile-tab" tabindex="0">
            <div id="${chartIdWeek}"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  function initCharts() {
    if (typeof ApexCharts !== "undefined") {
      const chartMonth = new ApexCharts(document.querySelector(`#${chartIdMonth}`), chartOptionsMonth);
      const chartWeek = new ApexCharts(document.querySelector(`#${chartIdWeek}`), chartOptionsWeek);
      chartMonth.render();
      chartWeek.render();
    }
  }

  return { element: col, initCharts };
}
