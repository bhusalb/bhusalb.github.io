document.querySelectorAll("[data-muon-explorer]").forEach(function (explorer) {
  const slider = explorer.querySelector('input[type="range"]');
  const originalAngle = (Math.atan2(-0.5, 2.5) * 180) / Math.PI;
  const format = (value, digits) => value.toFixed(digits).replace("-", "−");

  function update(announce = false) {
    const threshold = Number(slider.value);
    // Clip G1 = [[4, 0], [0, 0]] and G2 = [[0, 1], [0, 1]] independently,
    // then average. The threshold is positive, so this mean has positive determinant.
    const a = Math.min(4, threshold) / 2;
    const b = Math.min(1, threshold / Math.SQRT2) / 2;
    const d = b;
    const angle = (Math.atan2(-b, a + d) * 180) / Math.PI;
    const change = Math.abs(angle - originalAngle);

    explorer.querySelector("[data-muon-threshold]").textContent = format(threshold, 2);
    explorer.querySelector("[data-muon-a]").textContent = format(a, 4);
    explorer.querySelector("[data-muon-b]").textContent = format(b, 4);
    explorer.querySelector("[data-muon-d]").textContent = format(d, 4);
    explorer.querySelector("[data-muon-angle]").textContent = format(angle, 2) + "°";
    explorer.querySelector("[data-muon-change]").textContent = format(change, 2) + "°";
    slider.setAttribute("aria-valuetext", "C = " + format(threshold, 2));
    if (announce) {
      explorer.querySelector("[data-muon-status]").textContent =
        "At C = " + format(threshold, 2) + ", the polar rotation is " + format(angle, 2) + " degrees, a change of " + format(change, 2) + " degrees.";
    }
  }

  slider.addEventListener("input", () => update());
  slider.addEventListener("change", () => update(true));
  explorer.querySelectorAll("[data-muon-preset]").forEach(function (button) {
    button.addEventListener("click", function () {
      slider.value = button.dataset.muonPreset;
      update(true);
    });
  });
  update();
  explorer.hidden = false;
});
