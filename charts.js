class SimpleChart {
    constructor(canvas, data, options = {}) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.data = data;
        this.options = options;
        this.padding = 60;
        this.chartWidth = canvas.width - this.padding * 2;
        this.chartHeight = canvas.height - this.padding * 2;
    }

    destroy() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawBarChart() {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        const labels = this.data.labels;
        const datasets = this.data.datasets;
        const numBars = labels.length;
        const numDatasets = datasets.length;
        const barGroupWidth = this.chartWidth / numBars;
        const barWidth = barGroupWidth / (numDatasets + 1);

        // Find max value for scaling
        let maxValue = 0;
        datasets.forEach(dataset => {
            const max = Math.max(...dataset.data);
            if (max > maxValue) maxValue = max;
        });

        // Add some padding to max value
        maxValue = Math.ceil(maxValue * 1.1);

        // Draw Y-axis
        ctx.strokeStyle = '#495057';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(this.padding, this.padding);
        ctx.lineTo(this.padding, this.canvas.height - this.padding);
        ctx.lineTo(this.canvas.width - this.padding, this.canvas.height - this.padding);
        ctx.stroke();

        // Draw Y-axis labels and grid lines
        const numYLabels = 5;
        ctx.fillStyle = '#495057';
        ctx.font = '12px Arial';
        ctx.textAlign = 'right';
        ctx.strokeStyle = '#e9ecef';
        ctx.lineWidth = 1;

        for (let i = 0; i <= numYLabels; i++) {
            const value = Math.round((maxValue / numYLabels) * i);
            const y = this.canvas.height - this.padding - (this.chartHeight / numYLabels) * i;
            
            // Label
            ctx.fillText(value.toString(), this.padding - 10, y + 5);
            
            // Grid line
            ctx.beginPath();
            ctx.moveTo(this.padding, y);
            ctx.lineTo(this.canvas.width - this.padding, y);
            ctx.stroke();
        }

        // Draw bars
        datasets.forEach((dataset, datasetIndex) => {
            dataset.data.forEach((value, index) => {
                const barHeight = (value / maxValue) * this.chartHeight;
                const x = this.padding + (index * barGroupWidth) + (datasetIndex * barWidth) + barWidth / 2;
                const y = this.canvas.height - this.padding - barHeight;

                // Draw bar
                ctx.fillStyle = dataset.backgroundColor;
                ctx.fillRect(x, y, barWidth - 4, barHeight);

                // Draw border
                ctx.strokeStyle = dataset.borderColor;
                ctx.lineWidth = dataset.borderWidth || 1;
                ctx.strokeRect(x, y, barWidth - 4, barHeight);
            });
        });

        // Draw X-axis labels
        ctx.fillStyle = '#495057';
        ctx.font = '11px Arial';
        ctx.textAlign = 'center';
        labels.forEach((label, index) => {
            const x = this.padding + (index * barGroupWidth) + barGroupWidth / 2;
            const y = this.canvas.height - this.padding + 20;
            
            // Wrap long labels
            const words = label.split(' ');
            if (words.length > 1) {
                ctx.fillText(words[0], x, y);
                ctx.fillText(words.slice(1).join(' '), x, y + 12);
            } else {
                ctx.fillText(label, x, y);
            }
        });

        // Draw legend
        const legendY = 20;
        let legendX = this.canvas.width / 2 - (datasets.length * 100);
        
        datasets.forEach((dataset, index) => {
            // Legend box
            ctx.fillStyle = dataset.backgroundColor;
            ctx.fillRect(legendX, legendY, 15, 15);
            ctx.strokeStyle = dataset.borderColor;
            ctx.lineWidth = 2;
            ctx.strokeRect(legendX, legendY, 15, 15);

            // Legend label
            ctx.fillStyle = '#495057';
            ctx.font = '12px Arial';
            ctx.textAlign = 'left';
            ctx.fillText(dataset.label, legendX + 20, legendY + 12);

            legendX += 150;
        });

        // Draw title if provided
        if (this.options.title) {
            ctx.fillStyle = '#495057';
            ctx.font = 'bold 16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(this.options.title, this.canvas.width / 2, 20);
        }
    }
}

// Global chart instance
window.SimpleChart = SimpleChart;
