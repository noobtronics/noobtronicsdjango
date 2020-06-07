var BundleTracker = require('webpack-bundle-tracker');
var webpack = require('webpack');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const fs = require('fs')

const path = require("path");


var filenameHashing = true;

const IS_DEV_SERVER = process.argv[2].indexOf('serve') >= 0;


if(IS_DEV_SERVER){
  filenameHashing = false;
}




module.exports = {

  productionSourceMap: false,

  outputDir: path.resolve(__dirname, "../static/dist"),

  css: {
    extract: true
  },

  filenameHashing: filenameHashing,

  runtimeCompiler: true,

  configureWebpack: {
    plugins: [
      new BundleTracker({
        path: __dirname,
        filename: './webpack-stats.json',
        logTime: true,
      }),

      new BundleAnalyzerPlugin(),

    ],

    optimization: {
         splitChunks: {
            chunks: 'all',
            maxInitialRequests: Infinity,
            minSize: 0,
            cacheGroups: {
              vendor: {
                test: /[\\/]node_modules[\\/]/,
                name(module) {
                  // get the name. E.g. node_modules/packageName/not/this/part.js
                  // or node_modules/packageName
                  const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];

                  // npm package names are URL-safe, but some servers don't like @ symbols
                  return `npm.${packageName.replace('@', '')}`;
                },
              }
            }
          }
      }

  },

  devServer: {
    https: {
          key: fs.readFileSync('./certs/example.com+5-key.pem'),
          cert: fs.readFileSync('./certs/example.com+5.pem'),
        },
    public: 'https://localhost:8080/'
  },



}
