let maze;
let canvas;
let ctx;
let cellSize = 20;
let editMode = null;
let isDrawing = false;
let animationSpeed = 50;
let allResults = [];

// Initialize
window.onload = function() {
    canvas = document.getElementById('mazeCanvas');
    ctx = canvas.getContext('2d');
    
    // Set up event listeners
    document.getElementById('wallProb').addEventListener('input', (e) => {
        document.getElementById('wallProbValue').textContent = (e.target.value / 100).toFixed(2);
    });
    
    document.getElementById('speed').addEventListener('input', (e) => {
        animationSpeed = 101 - e.target.value;
        document.getElementById('speedValue').textContent = `${animationSpeed} ms`;
    });
    
    // Mouse events
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('mouseleave', handleMouseUp);
    
    // Generate initial maze
    generateMaze();
};

function generateMaze() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    const wallProb = parseFloat(document.getElementById('wallProb').value) / 100;
    
    maze = new Maze(rows, cols);
    maze.generateRandom(wallProb);
    
    resizeCanvas();
    drawMaze();
    clearMetrics();
    hideComparison();
}

function generatePerfectMaze() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    
    maze = new Maze(rows, cols);
    maze.generatePerfect();
    
    resizeCanvas();
    drawMaze();
    clearMetrics();
    hideComparison();
}

function clearMaze() {
    maze.clear();
    drawMaze();
    clearMetrics();
    hideComparison();
}

function resizeCanvas() {
    cellSize = Math.min(30, Math.floor(700 / Math.max(maze.rows, maze.cols)));
    canvas.width = maze.cols * cellSize;
    canvas.height = maze.rows * cellSize;
}

function drawMaze(explored = new Set(), path = []) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let i = 0; i < maze.rows; i++) {
        for (let j = 0; j < maze.cols; j++) {
            const x = j * cellSize;
            const y = i * cellSize;
            
            // Cell background
            if (maze.grid[i][j] === 1) {
                ctx.fillStyle = '#2c3e50';
            } else if (explored.has(`${i},${j}`)) {
                ctx.fillStyle = '#3498db';
            } else {
                ctx.fillStyle = '#ecf0f1';
            }
            
            ctx.fillRect(x, y, cellSize, cellSize);
            
            // Grid lines
            ctx.strokeStyle = '#bdc3c7';
            ctx.lineWidth = 1;
            ctx.strokeRect(x, y, cellSize, cellSize);
        }
    }
    
    // Draw path
    if (path.length > 0) {
        for (const cell of path) {
            const x = cell.col * cellSize;
            const y = cell.row * cellSize;
            ctx.fillStyle = '#f39c12';
            ctx.fillRect(x, y, cellSize, cellSize);
        }
    }
    
    // Draw start
    drawCircle(maze.start.col, maze.start.row, '#2ecc71');
    
    // Draw end
    drawCircle(maze.end.col, maze.end.row, '#e74c3c');
}

function drawCircle(col, row, color) {
    const x = col * cellSize + cellSize / 2;
    const y = row * cellSize + cellSize / 2;
    const radius = cellSize / 3;
    
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}

function setEditMode(mode) {
    // Remove active class from all buttons
    document.querySelectorAll('.edit-btn').forEach(btn => btn.classList.remove('active'));
    
    // Set new mode
    if (editMode === mode) {
        editMode = null;
    } else {
        editMode = mode;
        document.getElementById(mode + 'Btn').classList.add('active');
    }
}

function handleMouseDown(e) {
    isDrawing = true;
    handleEdit(e);
}

function handleMouseMove(e) {
    if (isDrawing) {
        handleEdit(e);
    }
}

function handleMouseUp() {
    isDrawing = false;
}

function handleEdit(e) {
    if (!editMode) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const col = Math.floor(x / cellSize);
    const row = Math.floor(y / cellSize);
    
    if (row < 0 || row >= maze.rows || col < 0 || col >= maze.cols) return;
    
    switch (editMode) {
        case 'wall':
            maze.setWall(row, col, true);
            break;
        case 'erase':
            maze.setWall(row, col, false);
            break;
        case 'start':
            maze.setStart(row, col);
            setEditMode('start'); // Toggle off
            break;
        case 'end':
            maze.setEnd(row, col);
            setEditMode('end'); // Toggle off
            break;
    }
    
    drawMaze();
}

async function runAlgorithm(algoName) {
    clearMetrics();
    hideComparison();
    
    const explored = new Set();
    let result;
    
    const onVisit = async (cell, type) => {
        explored.add(`${cell.row},${cell.col}`);
        drawMaze(explored);
        await sleep(animationSpeed);
    };
    
    const algoMap = {
        'dfs': () => PathfindingAlgorithms.dfs(maze, onVisit),
        'bfs': () => PathfindingAlgorithms.bfs(maze, onVisit),
        'dijkstra': () => PathfindingAlgorithms.dijkstra(maze, onVisit),
        'astar-manhattan': () => PathfindingAlgorithms.astar(maze, onVisit, 'manhattan'),
        'astar-euclidean': () => PathfindingAlgorithms.astar(maze, onVisit, 'euclidean'),
        'greedy': () => PathfindingAlgorithms.greedy(maze, onVisit),
        'bidirectional': () => PathfindingAlgorithms.bidirectional(maze, onVisit)
    };
    
    if (algoMap[algoName]) {
        result = await algoMap[algoName]();
        
        if (result.path) {
            drawMaze(explored, result.path);
        }
        
        displayMetrics(algoName, result);
    }
}

async function runAllAlgorithms() {
    clearMetrics();
    allResults = [];
    
    const algorithms = [
        { name: 'dfs', label: 'DFS' },
        { name: 'bfs', label: 'BFS' },
        { name: 'dijkstra', label: 'Dijkstra' },
        { name: 'astar-manhattan', label: 'A* (Manhattan)' },
        { name: 'astar-euclidean', label: 'A* (Euclidean)' },
        { name: 'greedy', label: 'Greedy' },
        { name: 'bidirectional', label: 'Bidirectional' }
    ];
    
    for (const algo of algorithms) {
        const explored = new Set();
        const onVisit = async (cell) => {
            explored.add(`${cell.row},${cell.col}`);
        };
        
        const algoMap = {
            'dfs': () => PathfindingAlgorithms.dfs(maze, onVisit),
            'bfs': () => PathfindingAlgorithms.bfs(maze, onVisit),
            'dijkstra': () => PathfindingAlgorithms.dijkstra(maze, onVisit),
            'astar-manhattan': () => PathfindingAlgorithms.astar(maze, onVisit, 'manhattan'),
            'astar-euclidean': () => PathfindingAlgorithms.astar(maze, onVisit, 'euclidean'),
            'greedy': () => PathfindingAlgorithms.greedy(maze, onVisit),
            'bidirectional': () => PathfindingAlgorithms.bidirectional(maze, onVisit)
        };
        
        const result = await algoMap[algo.name]();
        allResults.push({
            name: algo.label,
            ...result
        });
    }
    
    displayComparison();
}

function displayMetrics(algoName, result) {
    const algoLabels = {
        'dfs': 'DFS',
        'bfs': 'BFS',
        'dijkstra': 'Dijkstra',
        'astar-manhattan': 'A* (Manhattan)',
        'astar-euclidean': 'A* (Euclidean)',
        'greedy': 'Greedy Best-First',
        'bidirectional': 'Bidirectional BFS'
    };
    
    const html = `
        <div class="metric-item">
            <span class="metric-label">Algorithm:</span>
            <span class="metric-value">${algoLabels[algoName]}</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Path Found:</span>
            <span class="metric-value">${result.path ? '✓ Yes' : '✗ No'}</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Path Length:</span>
            <span class="metric-value">${result.path ? result.path.length : 'N/A'}</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Nodes Explored:</span>
            <span class="metric-value">${result.nodesExplored}</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Execution Time:</span>
            <span class="metric-value">${result.time.toFixed(3)} ms</span>
        </div>
        <div class="metric-item">
            <span class="metric-label">Optimal:</span>
            <span class="metric-value">${result.optimal ? '✓ Yes' : '✗ No'}</span>
        </div>
        ${result.heuristic ? `
        <div class="metric-item">
            <span class="metric-label">Heuristic:</span>
            <span class="metric-value">${result.heuristic}</span>
        </div>
        ` : ''}
    `;
    
    document.getElementById('metrics').innerHTML = html;
}

function clearMetrics() {
    document.getElementById('metrics').innerHTML = '<p class="placeholder">Run an algorithm to see metrics...</p>';
}

function displayComparison() {
    document.getElementById('comparisonPanel').style.display = 'block';
    
    // Create chart
    const chartCanvas = document.getElementById('comparisonChart');
    const chartCtx = chartCanvas.getContext('2d');
    
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
    }
    
    window.comparisonChart = new Chart(chartCtx, {
        type: 'bar',
        data: {
            labels: allResults.map(r => r.name),
            datasets: [
                {
                    label: 'Nodes Explored',
                    data: allResults.map(r => r.nodesExplored),
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Path Length',
                    data: allResults.map(r => r.path ? r.path.length : 0),
                    backgroundColor: 'rgba(243, 156, 18, 0.6)',
                    borderColor: 'rgba(243, 156, 18, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    // Create table
    const optimalPathLength = Math.min(...allResults.filter(r => r.optimal && r.path).map(r => r.path.length));
    const minNodes = Math.min(...allResults.map(r => r.nodesExplored));
    const minTime = Math.min(...allResults.map(r => r.time));
    
    let tableHtml = `
        <table>
            <thead>
                <tr>
                    <th>Algorithm</th>
                    <th>Path Found</th>
                    <th>Path Length</th>
                    <th>Nodes Explored</th>
                    <th>Time (ms)</th>
                    <th>Optimal</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    for (const result of allResults) {
        const pathLength = result.path ? result.path.length : 'N/A';
        const isOptimalPath = result.optimal && result.path && result.path.length === optimalPathLength;
        const isBestNodes = result.nodesExplored === minNodes;
        const isBestTime = result.time === minTime;
        
        tableHtml += `
            <tr>
                <td><strong>${result.name}</strong></td>
                <td>${result.path ? '✓' : '✗'}</td>
                <td class="${isOptimalPath ? 'best-value' : ''}">${pathLength}</td>
                <td class="${isBestNodes ? 'best-value' : ''}">${result.nodesExplored}</td>
                <td class="${isBestTime ? 'best-value' : ''}">${result.time.toFixed(3)}</td>
                <td>${result.optimal ? '✓' : '✗'}</td>
            </tr>
        `;
    }
    
    tableHtml += `
            </tbody>
        </table>
    `;
    
    document.getElementById('comparisonTable').innerHTML = tableHtml;
}

function hideComparison() {
    document.getElementById('comparisonPanel').style.display = 'none';
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
