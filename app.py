<!DOCTYPE html>
<html lang="en">
<head>
    <title>Math Solver App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        input { padding: 10px; width: 300px; }
        button { padding: 10px 20px; cursor: pointer; }
        #result { margin-top: 20px; font-weight: bold; color: blue; }
    </style>
</head>
<body>
    <h1>Math Solver AI</h1>
    <input type="text" id="problem" placeholder="Enter equation (e.g. x**2 - 4)">
    <button onclick="solve()">Solve</button>
    <div id="result"></div>

    <script>
        async function solve() {
            const problem = document.getElementById('problem').value;
            const resDiv = document.getElementById('result');
            resDiv.innerText = "Solving...";

            try {
                const response = await fetch('http://127.0.0.1:5000/solve', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({problem: problem})
                });
                const data = await response.json();
                resDiv.innerText = "Solution: " + data.solution;
            } catch (err) {
                resDiv.innerText = "Error connecting to backend!";
            }
        }
    </script>
</body>
</html>
