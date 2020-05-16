var BundleTracker = require('webpack-bundle-tracker');
const path = require("path");


module.exports = {

  productionSourceMap: false,

  outputDir: path.resolve(__dirname, "../static/dist"),

  configureWebpack: {
    plugins: [
      new BundleTracker({
        path: __dirname,
        filename: './webpack-stats.json',
      }),
    ]
  }

}
