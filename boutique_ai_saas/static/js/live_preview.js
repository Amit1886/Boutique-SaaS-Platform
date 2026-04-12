(function () {
  function ctx() {
    return window.TEMPLATE_SELECTOR_CONTEXT || null;
  }

  function getCookie(name) {
    const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return m ? decodeURIComponent(m[2]) : "";
  }

  function setClip(afterImg, value) {
    const v = Math.max(0, Math.min(100, Number(value) || 0));
    afterImg.style.clipPath = `inset(0 ${100 - v}% 0 0)`;
  }

  async function preview(templateId) {
    const c = ctx();
    if (!c || !c.previewApiUrl) return;

    const token = getCookie("csrftoken");
    const body = new URLSearchParams();
    body.set("session_id", String(c.sessionId));
    body.set("template_id", String(templateId));

    const res = await fetch(c.previewApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-CSRFToken": token,
      },
      body: body.toString(),
    });
    const json = await res.json();
    if (!json.ok) throw new Error(json.error || "preview failed");
    return json;
  }

  function init() {
    const c = ctx();
    if (!c) return;

    const afterImg = document.getElementById(c.afterImageId || "afterImg");
    const slider = document.getElementById(c.beforeAfterSliderId || "beforeAfterSlider");
    const fittingBox = document.getElementById(c.fittingBoxId || "fittingBox");
    if (!afterImg || !slider) return;

    setClip(afterImg, slider.value);
    slider.addEventListener("input", () => setClip(afterImg, slider.value));

    window.addEventListener("boutique:template_selected", async (ev) => {
      const templateId = ev && ev.detail && ev.detail.templateId;
      if (!templateId) return;
      try {
        if (fittingBox) {
          fittingBox.classList.add("hidden");
          fittingBox.textContent = "";
        }
        const data = await preview(templateId);
        if (data.result_url) {
          afterImg.src = data.result_url;
          afterImg.style.position = "absolute";
          afterImg.style.inset = "0";
          afterImg.classList.remove("hidden");
          slider.value = "50";
          setClip(afterImg, 50);
        }
        if (fittingBox && data.fitting) {
          fittingBox.textContent = `Fitting: neck=${data.fitting.neck_design}, sleeve=${data.fitting.sleeve_type}, back=${data.fitting.back_design}, pattern=${data.fitting.blouse_pattern || "-"}`;
          fittingBox.classList.remove("hidden");
        }
      } catch (e) {
        if (fittingBox) {
          fittingBox.textContent = "Preview failed. Try Generate Try-On.";
          fittingBox.classList.remove("hidden");
        }
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
