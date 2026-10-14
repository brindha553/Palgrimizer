/* ==========================================================================
   PALGRIMIZER DASHBOARD & STATS CANVAS CHARTS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', async () => {
    const chartCanvas = document.getElementById('analyticsChartCanvas');
    if (!chartCanvas) return;

    try {
        const res = await fetch('/dashboard/api/stats');
        const data = await res.json();
        if (data.status === 'success') {
            renderChart(chartCanvas, data.labels, data.score_trends);
        }
    } catch (e) {
        console.error('Failed to load chart data', e);
    }

    function renderChart(canvas, labels, values) {
        const ctx = canvas.getContext('2d');
        const width = canvas.width = canvas.parentElement.clientWidth;
        const height = canvas.height = 240;

        ctx.clearRect(0, 0, width, height);

        // Grid lines
        ctx.strokeStyle = 'rgba(148, 163, 184, 0.15)';
        ctx.lineWidth = 1;
        for (let y = 40; y < height - 30; y += 40) {
            ctx.beginPath();
            ctx.moveTo(40, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
        }

        // Draw Line Chart
        const padding = 50;
        const xStep = (width - padding * 2) / (values.length - 1);
        const minY = 80;
        const maxY = 100;

        ctx.beginPath();
        values.forEach((val, i) => {
            const x = padding + i * xStep;
            const y = height - 40 - ((val - minY) / (maxY - minY)) * (height - 80);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });

        // Gradient Stroke
        const gradient = ctx.createLinearGradient(0, 0, width, 0);
        gradient.addColorStop(0, '#6366f1');
        gradient.addColorStop(1, '#06b6d4');
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 3;
        ctx.stroke();

        // Draw Dots & Labels
        values.forEach((val, i) => {
            const x = padding + i * xStep;
            const y = height - 40 - ((val - minY) / (maxY - minY)) * (height - 80);

            ctx.fillStyle = '#6366f1';
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();

            // Label
            ctx.fillStyle = 'rgba(148, 163, 184, 0.8)';
            ctx.font = '12px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(labels[i], x, height - 12);
        });
    }
});
