module.exports = {
  // ... webpack configuration options
  resolve: {
    fallback: {
      "path": require.resolve("path-browserify"),
      "stream": require.resolve("stream-browserify"),
      "fs": false
    }
  }
};
