(function () {
  function getCtx() {
    return window.MEASUREMENT_AI_CONTEXT || null;
  }

  async function detect(apiUrl, file) {
    const fd = new FormData();
    fd.append("photo", file);
    function getCookie(name) {
      const v = document.cookie.split(";").map((c) => c.trim());
      for (const c of v) {
        if (c.startsWith(name + "=")) return decodeURIComponent(c.slice(name.length + 1));
      }
      return "";
    }
    const csrf = getCookie("csrftoken");
    const headers = csrf ? { "X-CSRFToken": csrf } : {};
    const res = await fetch(apiUrl, { method: "POST", body: fd, headers, credentials: "same-origin" });
    if (!res.ok) throw new Error("Measurement API failed");
    return res.json();
  }

  function init() {
    const c = getCtx();
    if (!c) return;

    const form = document.getElementById(c.formId);
    const btn = document.getElementById(c.buttonId);
    const status = document.getElementById(c.statusId);
    if (!form || !btn || !status) return;

    const bust = form.querySelector(`[name="${c.bustName}"]`);
    const waist = form.querySelector(`[name="${c.waistName}"]`);
    const height = form.querySelector(`[name="${c.heightName}"]`);
    const fileInput = form.querySelector(`[name="${c.fileInputName}"]`);

    btn.addEventListener("click", async () => {
      try {
        if (!fileInput || !fileInput.files || !fileInput.files[0]) {
          status.textContent = "Select a photo first.";
          return;
        }
        btn.disabled = true;
        status.textContent = "Detecting measurements…";
        const payload = await detect(c.apiUrl, fileInput.files[0]);
        if (!payload.ok) throw new Error(payload.error || "Unknown error");
        const m = payload.data || {};
        if (bust) bust.value = m.bust_in ?? "";
        if (waist) waist.value = m.waist_in ?? "";
        if (height) height.value = m.height_in ?? "";
        status.textContent = `Detected (confidence: ${m.confidence ?? "?"}).`;
      } catch (e) {
        status.textContent = "Detection failed (dummy API).";
      } finally {
        btn.disabled = false;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
