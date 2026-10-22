module.exports = {
  content: ["_site/**/*.html", "_site/**/*.js"],
  css: ["_site/assets/css/*.css"],
  output: "_site/assets/css/",
  skippedContentGlobs: ["_site/assets/**/*.html"],
  // MathJax and medium-zoom insert these elements in the browser, after the build.
  safelist: { greedy: [/mjx-container/, /medium-zoom/] },
};
