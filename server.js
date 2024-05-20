const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, 'public')));

app.post('/add', (req, res) => {
    const { a, b } = req.body;
    res.json({ result: a + b });
});

app.post('/subtract', (req, res) => {
    const { a, b } = req.body;
    res.json({ result: a - b });
});

app.post('/multiply', (req, res) => {
    const { a, b } = req.body;
    res.json({ result: a * b });
});

app.post('/divide', (req, res) => {
    const { a, b } = req.body;
    if (b === 0) {
        res.json({ error: 'Division by zero is not allowed' });
    } else {
        res.json({ result: a / b });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
