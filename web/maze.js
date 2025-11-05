class Maze {
    constructor(rows, cols) {
        this.rows = rows;
        this.cols = cols;
        this.grid = [];
        this.start = { row: 1, col: 1 };
        this.end = { row: rows - 2, col: cols - 2 };
        this.initGrid();
    }

    initGrid() {
        this.grid = [];
        for (let i = 0; i < this.rows; i++) {
            this.grid[i] = [];
            for (let j = 0; j < this.cols; j++) {
                // Border walls
                if (i === 0 || i === this.rows - 1 || j === 0 || j === this.cols - 1) {
                    this.grid[i][j] = 1; // wall
                } else {
                    this.grid[i][j] = 0; // empty
                }
            }
        }
        // Ensure start and end are clear
        this.grid[this.start.row][this.start.col] = 0;
        this.grid[this.end.row][this.end.col] = 0;
    }

    generateRandom(wallProb) {
        this.initGrid();
        for (let i = 1; i < this.rows - 1; i++) {
            for (let j = 1; j < this.cols - 1; j++) {
                if ((i === this.start.row && j === this.start.col) ||
                    (i === this.end.row && j === this.end.col)) {
                    continue;
                }
                this.grid[i][j] = Math.random() < wallProb ? 1 : 0;
            }
        }
    }

    generatePerfect() {
        // DFS maze generation
        this.grid = [];
        for (let i = 0; i < this.rows; i++) {
            this.grid[i] = new Array(this.cols).fill(1);
        }

        const stack = [{ row: 1, col: 1 }];
        this.grid[1][1] = 0;

        while (stack.length > 0) {
            const current = stack[stack.length - 1];
            const neighbors = this.getUnvisitedNeighbors(current, 2);

            if (neighbors.length === 0) {
                stack.pop();
            } else {
                const next = neighbors[Math.floor(Math.random() * neighbors.length)];
                // Carve path
                const midRow = current.row + (next.row - current.row) / 2;
                const midCol = current.col + (next.col - current.col) / 2;
                this.grid[midRow][midCol] = 0;
                this.grid[next.row][next.col] = 0;
                stack.push(next);
            }
        }

        this.grid[this.end.row][this.end.col] = 0;
    }

    getUnvisitedNeighbors(cell, step) {
        const neighbors = [];
        const directions = [
            { dr: -step, dc: 0 },
            { dr: step, dc: 0 },
            { dr: 0, dc: -step },
            { dr: 0, dc: step }
        ];

        for (const dir of directions) {
            const newRow = cell.row + dir.dr;
            const newCol = cell.col + dir.dc;

            if (newRow > 0 && newRow < this.rows - 1 &&
                newCol > 0 && newCol < this.cols - 1 &&
                this.grid[newRow][newCol] === 1) {
                neighbors.push({ row: newRow, col: newCol });
            }
        }

        return neighbors;
    }

    getNeighbors(row, col) {
        const neighbors = [];
        const directions = [
            { dr: -1, dc: 0 },
            { dr: 1, dc: 0 },
            { dr: 0, dc: -1 },
            { dr: 0, dc: 1 }
        ];

        for (const dir of directions) {
            const newRow = row + dir.dr;
            const newCol = col + dir.dc;

            if (this.isValid(newRow, newCol) && this.grid[newRow][newCol] !== 1) {
                neighbors.push({ row: newRow, col: newCol });
            }
        }

        return neighbors;
    }

    isValid(row, col) {
        return row >= 0 && row < this.rows && col >= 0 && col < this.cols;
    }

    setWall(row, col, isWall) {
        if ((row === this.start.row && col === this.start.col) ||
            (row === this.end.row && col === this.end.col)) {
            return;
        }
        this.grid[row][col] = isWall ? 1 : 0;
    }

    setStart(row, col) {
        if (this.grid[row][col] !== 1) {
            this.start = { row, col };
        }
    }

    setEnd(row, col) {
        if (this.grid[row][col] !== 1) {
            this.end = { row, col };
        }
    }

    clear() {
        this.initGrid();
    }
}
