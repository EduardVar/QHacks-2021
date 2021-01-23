require('dotenv').config();

const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const path = require('path');
const webpack = require('webpack');
const webpackConfig = require("../webpack.config");
const compiler = webpack(webpackConfig);

const Kijiji = require("../src/scrapers/kijiji");

const port = process.env.PORT || 3003;

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Webpack HMR

app.use(
    require("webpack-dev-middleware") (compiler, {
        publicPath: webpackConfig.output.publicPath,
        stats: false,
    })
);

app.use(require("webpack-hot-middleware") (compiler));

app.use(express.static("../dist"));

app.get('/', (req ,res) => {
    res.sendFile(path.resolve(__dirname, "../dist/index.html"));
});

app.get('/test', async (req, res) => {

    let output = await Kijiji.execute();
    res.send(output);
})

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});
