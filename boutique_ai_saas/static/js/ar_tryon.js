(function () {
  async function startCamera(videoEl) {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
    videoEl.srcObject = stream;
    return stream;
  }

  function stopCamera(stream, videoEl) {
    if (stream) stream.getTracks().forEach((t) => t.stop());
    if (videoEl) videoEl.srcObject = null;
  }

  function hexToRgba(hex, alpha) {
    const h = (hex || "").replace("#", "");
    if (h.length !== 6) return `rgba(255,0,128,${alpha})`;
    const r = parseInt(h.slice(0, 2), 16);
    const g = parseInt(h.slice(2, 4), 16);
    const b = parseInt(h.slice(4, 6), 16);
    return `rgba(${r},${g},${b},${alpha})`;
  }

  function init() {
    const c = window.TEMPLATE_SELECTOR_CONTEXT;
    if (!c || !c.ar) return;

    const startBtn = document.getElementById(c.ar.startBtnId);
    const stopBtn = document.getElementById(c.ar.stopBtnId);
    const videoEl = document.getElementById(c.ar.videoId);
    const canvasEl = document.getElementById("arCanvas");
    if (!startBtn || !stopBtn || !videoEl || !canvasEl) return;

    const ctx = canvasEl.getContext("2d");
    let stream = null;
    let overlayImg = new Image();
    overlayImg.crossOrigin = "anonymous";

    function draw() {
      if (!stream) return;
      const w = videoEl.videoWidth || 640;
      const h = videoEl.videoHeight || 480;
      canvasEl.width = w;
      canvasEl.height = h;
      ctx.drawImage(videoEl, 0, 0, w, h);

      // Dummy AR overlay: draw selected template if any
      const selectedUrl = window.BOUTIQUE_AI && window.BOUTIQUE_AI.selectedTemplateUrl;
      if (selectedUrl) {
        if (overlayImg.src !== selectedUrl) overlayImg.src = selectedUrl;
        const ow = w;
        const oh = Math.floor((overlayImg.height / Math.max(1, overlayImg.width)) * ow) || Math.floor(h * 0.9);
        const x = 0;
        const y = Math.floor(h * 0.08);
        ctx.globalAlpha = 0.75;
        ctx.drawImage(overlayImg, x, y, ow, oh);
        ctx.globalAlpha = 1.0;
      } else {
        ctx.fillStyle = "rgba(0,0,0,0.35)";
        ctx.fillRect(0, 0, w, 40);
        ctx.fillStyle = "white";
        ctx.font = "16px sans-serif";
        ctx.fillText("Select a template for overlay", 12, 26);
      }

      requestAnimationFrame(draw);
    }

    startBtn.addEventListener("click", async () => {
      try {
        stream = await startCamera(videoEl);
        canvasEl.classList.remove("hidden");
        draw();
      } catch (e) {
        alert("Camera access blocked.");
      }
    });

    stopBtn.addEventListener("click", () => {
      stopCamera(stream, videoEl);
      stream = null;
      canvasEl.classList.add("hidden");
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();

