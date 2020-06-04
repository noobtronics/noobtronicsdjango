module.exports = ({ file, options, env }) => ({
  plugins: {
    'postcss-import': {},
    'postcss-preset-env': { browsers: '> 1%, last 2 versions' },
    'cssnano': env === 'production' ? options.cssnano : false
  }
})
