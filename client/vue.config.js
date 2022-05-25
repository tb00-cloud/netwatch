const path = require('path')

module.exports = {
  transpileDependencies: true,

  pluginOptions: {
    'style-resources-loader': {
      preProcessor: 'scss',
      patterns: [path.resolve(__dirname, './src/assets/styles/*.scss'),]
    }
  }
}