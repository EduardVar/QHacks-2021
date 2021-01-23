const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const distDir = path.join(__dirname, '../dist');
const htmlEntry = path.join(__dirname, 'index.html');
const port = process.env.PORT || 3003;

app.use(express.static(distDir));

app.get('/', (req ,res) => {
    res.sendFile(htmlEntry);
});

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});
