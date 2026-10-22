// create element for copy button in code blocks
var codeBlocks = document.querySelectorAll("pre");
codeBlocks.forEach(function (codeBlock) {
  if (
    (codeBlock.querySelector("pre:not(.lineno)") || codeBlock.querySelector("code")) &&
    codeBlock.querySelector("code:not(.language-chartjs)") &&
    codeBlock.querySelector("code:not(.language-diff2html)") &&
    codeBlock.querySelector("code:not(.language-echarts)") &&
    codeBlock.querySelector("code:not(.language-geojson)") &&
    codeBlock.querySelector("code:not(.language-mermaid)") &&
    codeBlock.querySelector("code:not(.language-vega_lite)")
  ) {
    // create copy button
    var copyButton = document.createElement("button");
    copyButton.className = "copy";
    copyButton.type = "button";
    var copyLabel = codeBlock.dataset.copyLabel || "Copy";
    copyButton.ariaLabel = (codeBlock.dataset.copyLabel || "Copy code") + " to clipboard";
    copyButton.textContent = copyLabel;
    var copyStatus = document.createElement("span");
    copyStatus.className = "copy-status";
    copyStatus.setAttribute("role", "status");
    var resetTimer;

    // get code from code block and copy to clipboard
    copyButton.addEventListener("click", async function () {
      // check if code block has line numbers
      // i.e. `kramdown.syntax_highlighter_opts.block.line_numbers` set to true in _config.yml
      // or using `jekyll highlight` liquid tag with `linenos` option
      if (codeBlock.querySelector("pre:not(.lineno)")) {
        // get code from code block ignoring line numbers
        var code = codeBlock.querySelector("pre:not(.lineno)").textContent.trim();
      } else {
        // if (codeBlock.querySelector('code')) {
        // get code from code block when line numbers are not displayed
        var code = codeBlock.querySelector("code").textContent.trim();
      }
      clearTimeout(resetTimer);
      copyButton.disabled = true;
      copyButton.textContent = "Copying…";
      copyStatus.textContent = "";
      try {
        await window.navigator.clipboard.writeText(code);
        copyButton.textContent = "Copied!";
        copyStatus.textContent = "Copied to clipboard.";
        resetTimer = setTimeout(function () {
          copyButton.textContent = copyLabel;
          copyStatus.textContent = "";
        }, 3000);
      } catch (error) {
        copyButton.textContent = copyLabel;
        copyStatus.textContent = "Copy failed. Select the text and copy it manually.";
      } finally {
        copyButton.disabled = false;
      }
    });

    // create wrapper div
    var wrapper = document.createElement("div");
    wrapper.className = "code-display-wrapper";

    // add copy button and code block to wrapper div
    const parent = codeBlock.parentElement;
    parent.insertBefore(wrapper, codeBlock);
    wrapper.append(codeBlock);
    wrapper.append(copyButton);
    wrapper.append(copyStatus);
  }
});
