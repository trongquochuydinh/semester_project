export function createDonutStat({
  container,
  title,
  value,
  total,
  label,
  color
}) {
  const col = document.createElement("div");
  col.className = "col-md-6 col-xl-3 mb-3";

  const percent = total > 0 ? Math.round((value / total) * 100) : 0;

  col.innerHTML = `
    <div class="card text-center h-100">
      <div class="card-body py-3">
        <h6 class="mb-2">${title}</h6>

        <div style="
          width: 90px;
          height: 90px;
          margin: 0 auto 10px;
          border-radius: 50%;
          background: conic-gradient(
            ${color} ${percent}%,
            #e9ecef ${percent}% 100%
          );
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <div style="
            width: 60px;
            height: 60px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
          ">
            ${percent}%
          </div>
        </div>

        <div class="small">
          <b>${value}</b> / ${total}<br>
          <span class="text-muted">${label}</span>
        </div>
      </div>
    </div>
  `;

  container.appendChild(col);
}
