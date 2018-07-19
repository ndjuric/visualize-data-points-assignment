const webpack = require('webpack');

module.exports = {
    entry: [
        './App.jsx'
    ],
    output: {
        path: __dirname + '/../backend/web/static/js/',
        filename: "bundle.js"
    },
    module: {
        loaders: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel',
            query: {
                presets: ['es2015', 'react'],
                plugins: ['transform-class-properties', 'transform-object-rest-spread'],
                env: {
                    development: {
                        presets: ['react-hmre'],
                    },
                },
            },
        }],
    },
    watchOptions: {
        poll: 1000,
    },
    devServer: {
        historyApiFallback: {
            index: '/',
        },
    },
};
