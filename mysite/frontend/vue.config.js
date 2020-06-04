var BundleTracker = require('webpack-bundle-tracker');
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
      }),

      new BundleAnalyzerPlugin(),
    ]
  },

  devServer: {
    https: {
          key: fs.readFileSync('./certs/example.com+5-key.pem'),
          cert: fs.readFileSync('./certs/example.com+5.pem'),
        },
    public: 'https://localhost:8080/'
  },



}
