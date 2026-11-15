// 首页「估值与仓位建议」区块：读取 docs/valuation_reports.json 的最新一期

function escapeHtml(value) {
    return String(value == null ? '' : value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function actionClass(action) {
    if (action === '加仓') return 'add';
    if (action === '减仓') return 'reduce';
    return 'hold';
}

function formatNumber(value) {
    if (value === null || value === undefined) return 'N/A';
    return Number(value).toFixed(2);
}

function renderValuationCard(item) {
    const position = typeof item.range_position === 'number'
        ? `${(item.range_position * 100).toFixed(0)}%`
        : 'N/A';

    return `
        <div class="valuation-card">
            <div class="valuation-card-head">
                <div>
                    <h3 class="valuation-name">${escapeHtml(item.name)}</h3>
                    <span class="valuation-ticker">${escapeHtml(item.ticker)}</span>
                </div>
                <span class="valuation-badge ${actionClass(item.action)}">${escapeHtml(item.action)}</span>
            </div>
            <p class="valuation-meta">现价 ${escapeHtml(formatNumber(item.price))}｜52 周位置 ${escapeHtml(position)}</p>
            <p class="valuation-meta">估值 ${escapeHtml(item.rating)}（${escapeHtml(item.confidence)}）｜${escapeHtml(item.position_hint)}</p>
            <p class="valuation-reason">${escapeHtml(item.action_reason || item.thesis || '暂无说明')}</p>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', async () => {
    const grid = document.getElementById('valuationGrid');
    if (!grid) return;

    try {
        const response = await fetch('valuation_reports.json', { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const payload = await response.json();
        const latest = (payload.reports || [])[0];
        const items = latest && Array.isArray(latest.items) ? latest.items : [];

        if (!items.length) {
            grid.innerHTML = '<div class="valuation-empty">暂无估值建议，工作日 10:00 自动更新后显示。</div>';
            return;
        }

        grid.innerHTML = items.map(renderValuationCard).join('')
            + `<div class="valuation-updated">更新时间：${escapeHtml((latest.version ? latest.version + ' · ' : '') + (latest.date || ''))}</div>`;
    } catch (error) {
        console.warn('估值数据加载失败:', error);
        grid.innerHTML = '<div class="valuation-empty">估值数据暂不可用，请稍后重试。</div>';
    }
});
