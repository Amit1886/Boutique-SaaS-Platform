(function () {
  function ctx() {
    return window.TEMPLATE_SELECTOR_CONTEXT || null;
  }

  function init() {
    const c = ctx();
    if (!c || !c.fit) return;

    const overlayImg = document.getElementById(c.overlayImageId);
    const baseImg = document.getElementById(c.baseImageId);
    const scaleEl = document.getElementById(c.fit.scaleId);
    const rotEl = document.getElementById(c.fit.rotateId);
    const xEl = document.getElementById(c.fit.xId);
    const yEl = document.getElementById(c.fit.yId);
    if (!overlayImg || !baseImg || !scaleEl || !rotEl || !xEl || !yEl) return;

    function apply() {
      // Keep overlay "fit" and then apply user transform tweaks.
      window.BOUTIQUE_AI.fitOverlayToBase(baseImg, overlayImg);
      const scale = (Number(scaleEl.value || 100) || 100) / 100.0;
      const rotation_deg = Number(rotEl.value || 0) || 0;
      const x_px = Math.round(((Number(xEl.value || 0) || 0) / 100.0) * baseImg.clientWidth);
      const y_px = Math.round(((Number(yEl.value || 12) || 12) / 100.0) * baseImg.clientHeight);
      window.BOUTIQUE_AI.applyOverlayTransform(overlayImg, { scale, rotation_deg, x_px, y_px });
    }

    ["input", "change"].forEach((ev) => {
      scaleEl.addEventListener(ev, apply);
      rotEl.addEventListener(ev, apply);
      xEl.addEventListener(ev, apply);
      yEl.addEventListener(ev, apply);
    });

    baseImg.addEventListener("load", apply);
    window.addEventListener("resize", apply);
    apply();
  }

  document.addEventListener("DOMContentLoaded", init);
})();

