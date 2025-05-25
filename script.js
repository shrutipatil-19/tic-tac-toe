const boardDiv = document.getElementById('board');
const statusDiv = document.getElementById('status');

async function fetchBoard() {
    const res = await fetch("http://127.0.0.1:5000/board");
    const data = await res.json();
    drawBoard(data.board, data.player, data.winner);
}

function drawBoard(board, player, winner) {
    boardDiv.innerHTML = '';
    board.forEach((row, r) => {
        row.forEach((cell, c) => {
            const div = document.createElement('div');
            div.className = 'cell';
            div.textContent = cell;
            if (!cell && !winner) {
                div.onclick = () => makeMove(r, c);
            }
            boardDiv.appendChild(div);
        });
    });

    if (winner) {
        statusDiv.textContent = winner === 'Draw' ? "It's a Draw!" : `${winner} wins!`;
    } else {
        statusDiv.textContent = `Current Player: ${player}`;
    }
}

async function makeMove(row, col) {
    await fetch("http://127.0.0.1:5000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row, col })
    }).catch(() => alert("Invalid move"));
    fetchBoard();
}

async function resetGame() {
    await fetch("http://127.0.0.1:5000/reset", { method: "POST" });
    fetchBoard();
}

fetchBoard();
