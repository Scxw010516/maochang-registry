import CompressionWebpackPlugin from "compression-webpack-plugin";

export const productionSourceMap = false;
export function chainWebpack(config) {
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
}
export const css = {
  loaderOptions: {
    less: {
      lessOptions: {
        javascriptEnabled: true,
        plugins: [],
      },
    },
  },
};
