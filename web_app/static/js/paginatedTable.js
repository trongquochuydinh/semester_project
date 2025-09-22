// paginatedTable.js
// Usage: paginatedTable({
//   endpoint: '/paginate',
//   tableName: 'users',
//   columns: [ {key: 'id', label: 'ID'}, ... ],
//   containerId: 'table-container',
//   pageSize: 10,
//   filters: {...}
// })

export async function paginatedTable({endpoint, tableName, columns, containerId, pageSize=10, filters={}}) {
    let currentPage = 1;
    const container = document.getElementById(containerId);
    if (!container) return;

    async function loadPage(page) {
        const offset = (page-1)*pageSize;
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                table_name: tableName,
                limit: pageSize,
                offset,
                filters
            })
        });
        const data = await res.json();
        renderTable(data.data, data.total, page);
    }

    function renderTable(rows, total, page) {
        let html = '<div class="table-responsive">';
        html += '<table class="table table-striped table-bordered align-middle">';
        html += '<thead class="table-dark"><tr>';
        columns.forEach(col => {
            html += `<th>${col.label}</th>`;
        });
        html += '</tr></thead><tbody>';
        rows.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                html += `<td>${row[col.key] ?? ''}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table></div>';
        // Pagination controls
        const totalPages = Math.ceil(total/pageSize);
        html += '<nav><ul class="pagination justify-content-center">';
        for(let i=1;i<=totalPages;i++){
            html += `<li class="page-item${i===page?' active':''}"><button class="page-link" ${i===page?'disabled':''} onclick="window._paginateGoToPage_${containerId}(${i})">${i}</button></li>`;
        }
        html += '</ul></nav>';
        container.innerHTML = html;
        window[`_paginateGoToPage_${containerId}`] = (p) => {
            currentPage = p;
            loadPage(p);
        };
    }

    loadPage(currentPage);
}
