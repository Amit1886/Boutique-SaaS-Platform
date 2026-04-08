(function () {
  function getCtx() {
    return window.TRYON_CONTEXT || null;
  }

  function fitOverlayToBase(baseImg, overlayImg) {
    if (!baseImg || !overlayImg) return;
    overlayImg.style.width = baseImg.clientWidth + "px";
    overlayImg.style.height = "auto";
    overlayImg.style.left = "0px";
    overlayImg.style.top = "0px";
  }

  function initTryOnTemplateGallery() {
    const ctx = getCtx();
    if (!ctx) return;

    const baseImg = document.getElementById(ctx.userImageId);
    const overlayImg = document.getElementById(ctx.overlayId);
    const selectedTemplateId = document.getElementById(ctx.templateIdInput);
    const selectedNameEl = document.getElementById(ctx.templateNameEl);
    const gallery = document.getElementById(ctx.galleryId);
    if (!baseImg || !overlayImg || !selectedTemplateId || !selectedNameEl || !gallery) return;

    function applyTemplate(templateUrl, templateId, templateName) {
      overlayImg.classList.remove("hidden");
      overlayImg.src = templateUrl;
      selectedTemplateId.value = templateId;
      selectedNameEl.textContent = templateName || "Selected";

      overlayImg.onload = () => fitOverlayToBase(baseImg, overlayImg);
      fitOverlayToBase(baseImg, overlayImg);
    }

    gallery.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-template-id]");
      if (!btn) return;
      applyTemplate(btn.dataset.templateUrl, btn.dataset.templateId, btn.dataset.templateName);
    });

    window.addEventListener("resize", () => fitOverlayToBase(baseImg, overlayImg));
    baseImg.addEventListener("load", () => fitOverlayToBase(baseImg, overlayImg));
  }

  document.addEventListener("DOMContentLoaded", initTryOnTemplateGallery);
})();

