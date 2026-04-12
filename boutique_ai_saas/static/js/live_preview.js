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

  let activeController = null;

  async function preview(templateId) {
    const c = ctx();
    if (!c || !c.previewApiUrl) return;

    if (activeController) {
      try {
        activeController.abort();
      } catch (e) {}
    }
    activeController = new AbortController();

    const token = getCookie("csrftoken");
    const body = new URLSearchParams();
    body.set("session_id", String(c.sessionId));
    body.set("template_id", String(templateId));
    if (c.fit) {
      const scaleEl = document.getElementById(c.fit.scaleId);
      const rotEl = document.getElementById(c.fit.rotateId);
      const xEl = document.getElementById(c.fit.xId);
      const yEl = document.getElementById(c.fit.yId);
      if (scaleEl) body.set("scale", String((Number(scaleEl.value || 100) || 100) / 100.0));
      if (rotEl) body.set("rotation_deg", String(Number(rotEl.value || 0) || 0));
      if (xEl) body.set("x_offset_frac", String((Number(xEl.value || 0) || 0) / 100.0));
      if (yEl) body.set("y_offset_frac", String((Number(yEl.value || 12) || 12) / 100.0));
      if (c._saveFit === true) body.set("save_fit", "1");
    }

    const res = await fetch(c.previewApiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-CSRFToken": token,
      },
      body: body.toString(),
      signal: activeController.signal,
    });
    let json = null;
    try {
      json = await res.json();
    } catch (e) {
      throw new Error("Invalid server response");
    }
    if (!res.ok || !json || !json.ok) throw new Error((json && json.error) || `Preview failed (${res.status})`);
    return json;
  }

  function init() {
    const c = ctx();
    if (!c) return;

    const afterImg = document.getElementById(c.afterImageId || "afterImg");
    const slider = document.getElementById(c.beforeAfterSliderId || "beforeAfterSlider");
    const fittingBox = document.getElementById(c.fittingBoxId || "fittingBox");
    const previewStatus = document.getElementById(c.previewStatusId || "previewStatus");
    const previewLoading = document.getElementById(c.previewLoadingId || "previewLoading");
    if (!afterImg || !slider) return;

    setClip(afterImg, slider.value);
    slider.addEventListener("input", () => setClip(afterImg, slider.value));

    window.addEventListener("boutique:template_selected", async (ev) => {
      const templateId = ev && ev.detail && ev.detail.templateId;
      if (!templateId) return;
      try {
        if (previewStatus) previewStatus.textContent = "Generating preview…";
        if (previewLoading) previewLoading.classList.remove("hidden");
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

        if (c.fit && data.applied) {
          const scaleEl = document.getElementById(c.fit.scaleId);
          const rotEl = document.getElementById(c.fit.rotateId);
          const xEl = document.getElementById(c.fit.xId);
          const yEl = document.getElementById(c.fit.yId);
          if (scaleEl && typeof data.applied.scale === "number") scaleEl.value = String(Math.round(data.applied.scale * 100));
          if (rotEl && typeof data.applied.rotation_deg === "number") rotEl.value = String(Math.round(data.applied.rotation_deg));
          if (xEl && typeof data.applied.x_offset_frac === "number") xEl.value = String(Math.round(data.applied.x_offset_frac * 100));
          if (yEl && typeof data.applied.y_offset_frac === "number") yEl.value = String(Math.round(data.applied.y_offset_frac * 100));
        }

        if (fittingBox && data.fitting) {
          fittingBox.textContent = `Fitting: neck=${data.fitting.neck_design}, sleeve=${data.fitting.sleeve_type}, back=${data.fitting.back_design}, pattern=${data.fitting.blouse_pattern || "-"}`;
          fittingBox.classList.remove("hidden");
        }
        if (previewStatus) previewStatus.textContent = "Preview updated";
      } catch (e) {
        if (e && String(e.name || "").toLowerCase() === "aborterror") {
          return;
        }
        if (fittingBox) {
          fittingBox.textContent = `Preview failed. ${e && e.message ? e.message : "Try Generate Try-On."}`;
          fittingBox.classList.remove("hidden");
        }
        if (previewStatus) previewStatus.textContent = "Preview failed";
      } finally {
        if (previewLoading) previewLoading.classList.add("hidden");
      }
    });

    // Auto fit resets sliders to defaults, then triggers a re-preview on the last selected template.
    const autoBtn = c.fit && document.getElementById(c.fit.autoBtnId);
    const saveBtn = c.fit && document.getElementById(c.fit.saveBtnId);
    let lastTemplateId = null;
    window.addEventListener("boutique:template_selected", (ev) => {
      lastTemplateId = ev && ev.detail && ev.detail.templateId ? String(ev.detail.templateId) : lastTemplateId;
    });
    if (autoBtn) {
      autoBtn.addEventListener("click", () => {
        const scaleEl = document.getElementById(c.fit.scaleId);
        const rotEl = document.getElementById(c.fit.rotateId);
        const xEl = document.getElementById(c.fit.xId);
        const yEl = document.getElementById(c.fit.yId);
        if (scaleEl) scaleEl.value = "100";
        if (rotEl) rotEl.value = "0";
        if (xEl) xEl.value = "0";
        if (yEl) yEl.value = "12";
        if (lastTemplateId) window.dispatchEvent(new CustomEvent("boutique:template_selected", { detail: { templateId: lastTemplateId } }));
      });
    }
    if (saveBtn) {
      saveBtn.addEventListener("click", async () => {
        if (!lastTemplateId) return;
        try {
          c._saveFit = true;
          await preview(lastTemplateId);
        } catch (e) {
        } finally {
          c._saveFit = false;
        }
      });
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
