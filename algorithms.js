class PathfindingAlgorithms {
    static manhattanDistance(a, b) {
        return Math.abs(a.row - b.row) + Math.abs(a.col - b.col);
    }

    static euclideanDistance(a, b) {
        return Math.sqrt(Math.pow(a.row - b.row, 2) + Math.pow(a.col - b.col, 2));
    }

    static async dfs(maze, onVisit) {
        const start = performance.now();
        const stack = [maze.start];
        const visited = new Set();
        const parent = new Map();
        let nodesExplored = 0;

        visited.add(`${maze.start.row},${maze.start.col}`);

        while (stack.length > 0) {
            const current = stack.pop();
            nodesExplored++;

            await onVisit(current, 'exploring');

            if (current.row === maze.end.row && current.col === maze.end.col) {
                const path = this.reconstructPath(parent, maze.start, maze.end);
                const time = performance.now() - start;
                return { path, nodesExplored, time, optimal: false };
            }

            const neighbors = maze.getNeighbors(current.row, current.col);
            for (const neighbor of neighbors) {
                const key = `${neighbor.row},${neighbor.col}`;
                if (!visited.has(key)) {
                    visited.add(key);
                    parent.set(key, current);
                    stack.push(neighbor);
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: false };
    }

    static async bfs(maze, onVisit) {
        const start = performance.now();
        const queue = [maze.start];
        const visited = new Set();
        const parent = new Map();
        let nodesExplored = 0;

        visited.add(`${maze.start.row},${maze.start.col}`);

        while (queue.length > 0) {
            const current = queue.shift();
            nodesExplored++;

            await onVisit(current, 'exploring');

            if (current.row === maze.end.row && current.col === maze.end.col) {
                const path = this.reconstructPath(parent, maze.start, maze.end);
                const time = performance.now() - start;
                return { path, nodesExplored, time, optimal: true };
            }

            const neighbors = maze.getNeighbors(current.row, current.col);
            for (const neighbor of neighbors) {
                const key = `${neighbor.row},${neighbor.col}`;
                if (!visited.has(key)) {
                    visited.add(key);
                    parent.set(key, current);
                    queue.push(neighbor);
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: true };
    }

    static async dijkstra(maze, onVisit) {
        const start = performance.now();
        const distances = new Map();
        const parent = new Map();
        const visited = new Set();
        const pq = new PriorityQueue();
        let nodesExplored = 0;

        const startKey = `${maze.start.row},${maze.start.col}`;
        distances.set(startKey, 0);
        pq.enqueue(maze.start, 0);

        while (!pq.isEmpty()) {
            const current = pq.dequeue();
            const currentKey = `${current.row},${current.col}`;

            if (visited.has(currentKey)) continue;
            visited.add(currentKey);
            nodesExplored++;

            await onVisit(current, 'exploring');

            if (current.row === maze.end.row && current.col === maze.end.col) {
                const path = this.reconstructPath(parent, maze.start, maze.end);
                const time = performance.now() - start;
                return { path, nodesExplored, time, optimal: true };
            }

            const neighbors = maze.getNeighbors(current.row, current.col);
            for (const neighbor of neighbors) {
                const neighborKey = `${neighbor.row},${neighbor.col}`;
                const newDist = distances.get(currentKey) + 1;

                if (!distances.has(neighborKey) || newDist < distances.get(neighborKey)) {
                    distances.set(neighborKey, newDist);
                    parent.set(neighborKey, current);
                    pq.enqueue(neighbor, newDist);
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: true };
    }

    static async astar(maze, onVisit, heuristic = 'manhattan') {
        const start = performance.now();
        const gScore = new Map();
        const fScore = new Map();
        const parent = new Map();
        const visited = new Set();
        const pq = new PriorityQueue();
        let nodesExplored = 0;

        const heuristicFunc = heuristic === 'euclidean' ? 
            this.euclideanDistance : this.manhattanDistance;

        const startKey = `${maze.start.row},${maze.start.col}`;
        gScore.set(startKey, 0);
        fScore.set(startKey, heuristicFunc(maze.start, maze.end));
        pq.enqueue(maze.start, fScore.get(startKey));

        while (!pq.isEmpty()) {
            const current = pq.dequeue();
            const currentKey = `${current.row},${current.col}`;

            if (visited.has(currentKey)) continue;
            visited.add(currentKey);
            nodesExplored++;

            await onVisit(current, 'exploring');

            if (current.row === maze.end.row && current.col === maze.end.col) {
                const path = this.reconstructPath(parent, maze.start, maze.end);
                const time = performance.now() - start;
                return { path, nodesExplored, time, optimal: true, heuristic };
            }

            const neighbors = maze.getNeighbors(current.row, current.col);
            for (const neighbor of neighbors) {
                const neighborKey = `${neighbor.row},${neighbor.col}`;
                const tentativeGScore = gScore.get(currentKey) + 1;

                if (!gScore.has(neighborKey) || tentativeGScore < gScore.get(neighborKey)) {
                    parent.set(neighborKey, current);
                    gScore.set(neighborKey, tentativeGScore);
                    const h = heuristicFunc(neighbor, maze.end);
                    fScore.set(neighborKey, tentativeGScore + h);
                    pq.enqueue(neighbor, fScore.get(neighborKey));
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: true, heuristic };
    }

    static async greedy(maze, onVisit) {
        const start = performance.now();
        const parent = new Map();
        const visited = new Set();
        const pq = new PriorityQueue();
        let nodesExplored = 0;

        pq.enqueue(maze.start, this.manhattanDistance(maze.start, maze.end));
        visited.add(`${maze.start.row},${maze.start.col}`);

        while (!pq.isEmpty()) {
            const current = pq.dequeue();
            nodesExplored++;

            await onVisit(current, 'exploring');

            if (current.row === maze.end.row && current.col === maze.end.col) {
                const path = this.reconstructPath(parent, maze.start, maze.end);
                const time = performance.now() - start;
                return { path, nodesExplored, time, optimal: false };
            }

            const neighbors = maze.getNeighbors(current.row, current.col);
            for (const neighbor of neighbors) {
                const key = `${neighbor.row},${neighbor.col}`;
                if (!visited.has(key)) {
                    visited.add(key);
                    parent.set(key, current);
                    const h = this.manhattanDistance(neighbor, maze.end);
                    pq.enqueue(neighbor, h);
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: false };
    }

    static async bidirectional(maze, onVisit) {
        const start = performance.now();
        const queueStart = [maze.start];
        const queueEnd = [maze.end];
        const visitedStart = new Set([`${maze.start.row},${maze.start.col}`]);
        const visitedEnd = new Set([`${maze.end.row},${maze.end.col}`]);
        const parentStart = new Map();
        const parentEnd = new Map();
        let nodesExplored = 0;

        while (queueStart.length > 0 && queueEnd.length > 0) {
            // Expand from start
            if (queueStart.length > 0) {
                const current = queueStart.shift();
                nodesExplored++;
                await onVisit(current, 'exploring');

                const currentKey = `${current.row},${current.col}`;
                if (visitedEnd.has(currentKey)) {
                    const path = this.reconstructBidirectionalPath(
                        parentStart, parentEnd, maze.start, current, maze.end
                    );
                    const time = performance.now() - start;
                    return { path, nodesExplored, time, optimal: true };
                }

                const neighbors = maze.getNeighbors(current.row, current.col);
                for (const neighbor of neighbors) {
                    const key = `${neighbor.row},${neighbor.col}`;
                    if (!visitedStart.has(key)) {
                        visitedStart.add(key);
                        parentStart.set(key, current);
                        queueStart.push(neighbor);
                    }
                }
            }

            // Expand from end
            if (queueEnd.length > 0) {
                const current = queueEnd.shift();
                nodesExplored++;
                await onVisit(current, 'exploring');

                const currentKey = `${current.row},${current.col}`;
                if (visitedStart.has(currentKey)) {
                    const path = this.reconstructBidirectionalPath(
                        parentStart, parentEnd, maze.start, current, maze.end
                    );
                    const time = performance.now() - start;
                    return { path, nodesExplored, time, optimal: true };
                }

                const neighbors = maze.getNeighbors(current.row, current.col);
                for (const neighbor of neighbors) {
                    const key = `${neighbor.row},${neighbor.col}`;
                    if (!visitedEnd.has(key)) {
                        visitedEnd.add(key);
                        parentEnd.set(key, current);
                        queueEnd.push(neighbor);
                    }
                }
            }
        }

        const time = performance.now() - start;
        return { path: null, nodesExplored, time, optimal: true };
    }

    static reconstructPath(parent, start, end) {
        const path = [];
        let current = end;
        const startKey = `${start.row},${start.col}`;

        while (current) {
            path.unshift(current);
            const key = `${current.row},${current.col}`;
            if (key === startKey) break;
            current = parent.get(key);
        }

        return path;
    }

    static reconstructBidirectionalPath(parentStart, parentEnd, start, meeting, end) {
        const pathStart = [];
        let current = meeting;
        const startKey = `${start.row},${start.col}`;

        while (current) {
            pathStart.unshift(current);
            const key = `${current.row},${current.col}`;
            if (key === startKey) break;
            current = parentStart.get(key);
        }

        const pathEnd = [];
        current = parentEnd.get(`${meeting.row},${meeting.col}`);
        while (current) {
            pathEnd.push(current);
            const key = `${current.row},${current.col}`;
            const endKey = `${end.row},${end.col}`;
            if (key === endKey) break;
            current = parentEnd.get(key);
        }

        return [...pathStart, ...pathEnd];
    }
}

class PriorityQueue {
    constructor() {
        this.values = [];
    }

    enqueue(item, priority) {
        this.values.push({ item, priority });
        this.values.sort((a, b) => a.priority - b.priority);
    }

    dequeue() {
        return this.values.shift()?.item;
    }

    isEmpty() {
        return this.values.length === 0;
    }
}
