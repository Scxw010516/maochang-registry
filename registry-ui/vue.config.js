const CompressionWebpackPlugin = require("compression-webpack-plugin");
// const DynamicAntdLess =
//   require("ele-admin-pro/lib/utils/dynamic-theme").DynamicAntdLess;

module.exports = {
  productionSourceMap: false,
  transpileDependencies: ["ele-admin-pro"],
  chainWebpack: (config) => {
    config.plugins.delete("prefetch");
    if (process.env.NODE_ENV !== "development") {
      // 生产环境进行gzip压缩
      config.plugin("compression-webpack-plugin").use(
        new CompressionWebpackPlugin({
          test: /\.(js|css|html)$/,
          threshold: 10240,
        }),
      );
    }
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          javascriptEnabled: true,
          plugins: [
            // new DynamicAntdLess({
            //   replaces: {
            //     "darken(@shadow-color, 5%)": "@shadow-color",
            //   },
            // }),
          ],
        },
      },
    },
  },
};
