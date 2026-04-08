(function () {
  function ctx() {
    return window.TEMPLATE_SELECTOR_CONTEXT || null;
  }

  function init() {
    const c = ctx();
    if (!c) return;

    const gallery = document.getElementById(c.galleryId);
    const baseImg = document.getElementById(c.baseImageId);
    const overlayImg = document.getElementById(c.overlayImageId);
    const selectedId = document.getElementById(c.selectedTemplateIdInput);
    const selectedName = document.getElementById(c.selectedTemplateNameEl);
    if (!gallery || !baseImg || !overlayImg || !selectedId || !selectedName) return;

    function applyTemplate(url, id, name) {
      overlayImg.classList.remove("hidden");
      overlayImg.src = url;
      selectedId.value = id;
      selectedName.textContent = name || "Selected";
      overlayImg.onload = () => window.BOUTIQUE_AI.fitOverlayToBase(baseImg, overlayImg);
      window.BOUTIQUE_AI.fitOverlayToBase(baseImg, overlayImg);

      // expose selected URL for AR module
      window.BOUTIQUE_AI.selectedTemplateUrl = url;
    }

    gallery.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-template-id]");
      if (!btn) return;
      applyTemplate(btn.dataset.templateUrl, btn.dataset.templateId, btn.dataset.templateName);
    });

    window.addEventListener("resize", () => window.BOUTIQUE_AI.fitOverlayToBase(baseImg, overlayImg));
    baseImg.addEventListener("load", () => window.BOUTIQUE_AI.fitOverlayToBase(baseImg, overlayImg));
  }

  document.addEventListener("DOMContentLoaded", init);
})();

