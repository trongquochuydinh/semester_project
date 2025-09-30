// Default style for bar charts
const defaultBarChartOptions = {
  chart: { type: 'bar', height: 365, toolbar: { show: false } },
  plotOptions: { bar: { columnWidth: '45%', borderRadius: 4 } },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  xaxis: {
    categories: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: { show: false },
  grid: { show: false }
};

/**
 * Create a chart card (with ApexCharts container)
 * @param {Object} options - Chart card config
 * @param {string} options.title - Section title (e.g. "Income Overview")
 * @param {string} options.subtitle - Card subtitle (e.g. "This Week Statistics")
 * @param {string|number} options.value - Main value (e.g. "$7,650")
 * @param {string} options.chartId - Unique id for the chart container
 * @param {Object} [options.chartOptions] - ApexCharts overrides (merged with defaults)
 * @returns {Object} - { element, initChart() }
 */
function createChartCard({ title, subtitle, value, chartId, chartOptions = {} }) {
  const col = document.createElement("div");
  col.className = "col-md-12 col-xl-4";

  col.innerHTML = `
    <h5 class="mb-3">${title}</h5>
    <div class="card">
      <div class="card-body">
        <h6 class="mb-2 f-w-400 text-muted">${subtitle}</h6>
        <h3 class="mb-3">${value}</h3>
        <div id="${chartId}"></div>
      </div>
    </div>
  `;

  // Merge defaults with overrides
  const finalChartOptions = {
    ...defaultBarChartOptions,
    ...chartOptions,
    plotOptions: {
      ...defaultBarChartOptions.plotOptions,
      ...chartOptions.plotOptions
    },
    xaxis: {
      ...defaultBarChartOptions.xaxis,
      ...chartOptions.xaxis
    }
  };

  return {
    element: col,
    initChart: () => {
      if (typeof ApexCharts !== "undefined") {
        const chart = new ApexCharts(
          document.querySelector(`#${chartId}`),
          finalChartOptions
        );
        chart.render();
      }
    }
  };
}
