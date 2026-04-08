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
})();

