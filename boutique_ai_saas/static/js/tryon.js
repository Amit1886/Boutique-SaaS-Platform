(function () {
  // Shared helpers for try-on UX.
  window.BOUTIQUE_AI = window.BOUTIQUE_AI || {};

  window.BOUTIQUE_AI.fitOverlayToBase = function (baseImg, overlayImg) {
    if (!baseImg || !overlayImg) return;
    overlayImg.style.width = baseImg.clientWidth + "px";
    overlayImg.style.height = "auto";
    overlayImg.style.left = "0px";
    overlayImg.style.top = "0px";
  };

  window.BOUTIQUE_AI.applyOverlayTransform = function (overlayImg, opts) {
    if (!overlayImg) return;
    const scale = Number(opts && opts.scale) || 1;
    const rot = Number(opts && opts.rotation_deg) || 0;
    const x = Number(opts && opts.x_px) || 0;
    const y = Number(opts && opts.y_px) || 0;
    overlayImg.style.transformOrigin = "top center";
    overlayImg.style.transform = `translate(${x}px, ${y}px) rotate(${rot}deg) scale(${scale})`;
  };
})();
