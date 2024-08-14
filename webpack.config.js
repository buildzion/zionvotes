const path = require('path')

module.exports = {
    entry: "./js-src/index.js",
    output: {
        filename: "zionvotes.js",
        path: path.resolve(__dirname, "zionvotes/static/zv")
    },
    resolve: {
        alias: {
            jquery: "jquery/src/jquery"
        }
    }
};
