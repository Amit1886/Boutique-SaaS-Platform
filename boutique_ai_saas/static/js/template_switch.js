(function () {
  function ctx() {
    return window.TEMPLATE_SELECTOR_CONTEXT || null;
  }

  function init() {
    const c = ctx();
    if (!c) return;
    const gallery = document.getElementById(c.galleryId);
    if (!gallery) return;

    gallery.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-template-id]");
      if (!btn) return;
      const detail = {
        templateId: btn.dataset.templateId,
        templateUrl: btn.dataset.templateUrl,
        templateName: btn.dataset.templateName,
      };
      window.dispatchEvent(new CustomEvent("boutique:template_selected", { detail }));
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();

