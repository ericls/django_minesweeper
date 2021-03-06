const path = require("path");
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');


module.exports = {
    context: __dirname,

    entry: './assets/js/index', // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs

    output: {
        path: path.resolve('./assets/bundles/'),
        filename: "[name]-[hash].js",
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
    ],

    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['es2015', 'es2016', 'react']
                }
            },
            {
                test: /\.s(c|a)ss$/,
                // loader: ExtractTextPlugin.extract("style-loader", "css-loader", "sass-loader"),
                loaders: ["style-loader", "css-loader", "sass-loader"]
            }
        ],
    },

    resolve: {
        modulesDirectories: ['node_modules', 'bower_components'],
        extensions: ['', '.js', '.jsx']
    },
};