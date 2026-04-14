// Fallback Magic Studio UI so /magic/ works without React build.
// Uses plain JS + fetch against /magic/api.

"use strict";

const API = "/magic/api";
const app = document.getElementById("app");

const state = {
  route: (location.hash || "#/").replace("#", ""),
  adminToken: localStorage.getItem("magic.admin") || "",
  userName: localStorage.getItem("magic.user") || "Guest",
  sarees: [],
  blouses: [],
  accessories: [],
  selected: { saree: null, blouse: null, accessories: [] },
  flags: {},
  toastOpen: false,
  toastLine: "",
  toastKey: 0,
  selectedSareeId: null,
};

const jinnLines = [
  "Madam, this saree suits your aura!",
  "Perfect pallu flow detected!",
  "Neon border glow engaged.",
  "Magic mirror ready — tilt for gravity!",
  "Tap fabric to reveal hidden patterns.",
];

function escapeHtml(s) {
  return String(s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeXml(s) {
  return String(s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function setMagicColor(hex) {
  document.documentElement.style.setProperty("--magic", hex || "#db2777");
}

function toast(msg) {
  state.toastLine = msg || jinnLines[Math.floor(Math.random() * jinnLines.length)];
  state.toastKey = Date.now();
  state.toastOpen = true;
  render();
  setTimeout(() => {
    state.toastOpen = false;
    render();
  }, 2600);
}

async function apiGet(path, headers) {
  const res = await fetch(`${API}${path}`, { headers: headers || {} });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "Request failed");
  return json;
}

async function apiPost(path, body, headers) {
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: JSON.stringify(body || {}),
  });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "Request failed");
  return json;
}

async function apiPut(path, body, headers) {
  const res = await fetch(`${API}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...(headers || {}) },
    body: JSON.stringify(body || {}),
  });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "Request failed");
  return json;
}

async function apiDel(path, headers) {
  const res = await fetch(`${API}${path}`, { method: "DELETE", headers: headers || {} });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "Request failed");
  return json;
}

function hdrAdmin() {
  return { "X-Admin-Token": state.adminToken };
}

async function uploadFile(path, file, query) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await fetch(`${API}${path}${query || ""}`, { method: "POST", headers: hdrAdmin(), body: fd });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "upload failed");
  return json.path;
}

async function loadCatalog() {
  const [s, b, a] = await Promise.all([apiGet("/sarees"), apiGet("/blouses"), apiGet("/accessories")]);
  state.sarees = s.items || [];
  state.blouses = b.items || [];
  state.accessories = a.items || [];
  if (!state.selected.saree && state.sarees[0]) state.selected.saree = state.sarees[0];
  if (!state.selected.blouse && state.blouses[0]) state.selected.blouse = state.blouses[0];
  if (state.selected.saree?.primary_color) setMagicColor(state.selected.saree.primary_color);
}

async function loadUx() {
  const r = await apiGet("/uxflags");
  const map = {};
  for (const f of r.items || []) map[f.key] = !!f.enabled;
  state.flags = map;
}

function isOn(key) {
  const v = state.flags[key];
  return v === undefined ? true : !!v;
}

function navLink(href, label) {
  const active = state.route === href;
  return `<a class="${active ? "active" : ""}" href="#${href}">${label}</a>`;
}

function topbar() {
  return `
    <div class="topbar">
      <div class="topbar-inner">
        <div class="row" style="gap:10px">
          <div class="brand">Magic<span class="accent">Studio</span></div>
          <div class="pill">/magic</div>
        </div>
        <div class="nav">
          <a class="btn small ghost" href="/">Back to Django Home</a>
          <a class="btn small ${state.route === "/admin" ? "primary" : ""}" href="#/admin">Admin</a>
        </div>
      </div>
    </div>
  `;
}

function bottomNav() {
  return `
    <div class="bottom">
      <div class="bottom-inner">
        ${navLink("/", "Home")}
        ${navLink("/studio", "Try-On")}
        ${navLink("/mirror", "Mirror")}
        ${navLink("/looks", "Looks")}
      </div>
    </div>
  `;
}

function toastUi() {
  const open = state.toastOpen
    ? "opacity:1; transform: translateY(0);"
    : "opacity:0; transform: translateY(6px); pointer-events:none;";
  return `
    <div class="toast">
      <div style="transition: all 160ms ease; ${open}">
        <div class="bubble">
          <div class="name">Tailor Jinn</div>
          <div class="line">${escapeHtml(state.toastLine)}</div>
        </div>
      </div>
    </div>
  `;
}

function homePage() {
  const s = state.selected.saree;
  return `
    <div class="wrap">
      <div class="card">
        <div class="bd">
          <div class="h1">Magic Boutique Studio</div>
          <div class="muted" style="margin-top:8px">Fallback UI (no React build required).</div>
          <div class="row" style="margin-top:14px">
            <a class="btn primary" href="#/studio">Open Try-On Studio</a>
            <a class="btn" href="#/mirror">Magic Mirror</a>
            <a class="btn" href="#/looks">Saved Looks</a>
          </div>
          <div class="divider"></div>
          <div class="h2">Quick Select Saree</div>
          <div class="muted" style="margin-top:6px">Saree select karo → theme color change.</div>
          <div class="row" style="margin-top:10px">
            ${(state.sarees || []).slice(0, 10).map(it => `
              <button class="btn small ${s?.id===it.id?"primary":""}" data-act="pickSaree" data-id="${it.id}">${escapeHtml(it.name).slice(0, 16)}</button>
            `).join("")}
          </div>
        </div>
      </div>
    </div>
  `;
}

function studioPage() {
  const saree = state.selected.saree;
  const blouse = state.selected.blouse;
  const acc = state.selected.accessories;
  const body = saree?.layer_body_png ? `<img class="layer teleport aura" style="mix-blend-mode:multiply; opacity:.92" src="${saree.layer_body_png}" />` : "";
  const border = saree?.layer_border_png ? `<img class="layer teleport aura" style="mix-blend-mode:screen; opacity:.92" src="${saree.layer_border_png}" />` : "";
  const pallu = saree?.layer_pallu_png ? `<img id="palluLayer" class="layer teleport aura" style="mix-blend-mode:multiply; opacity:.92" src="${saree.layer_pallu_png}" />` : "";
  const blouseLayer = blouse?.template_png ? `<img class="layer teleport aura" style="mix-blend-mode:screen; opacity:.92" src="${blouse.template_png}" />` : "";
  const accLayers = (acc || []).map((a, i) => a.image_png ? `<img class="layer teleport aura" style="mix-blend-mode:screen; opacity:.92; transform: translate(${i*3-4}%, ${i*2-2}%) scale(.75)" src="${a.image_png}" />` : "").join("");
  return `
    <div class="wrap">
      <div class="card"><div class="bd">
        <div class="h1">Try-On Studio</div>
        <div class="muted" style="margin-top:8px">Tap stage for ripple reveal. Live overlays.</div>
      </div></div>

      <div class="grid two" style="margin-top:14px">
        <div class="card">
          <div class="hd">
            <div class="row" style="justify-content: space-between">
              <div><div class="h2">Live Preview</div><div class="muted">Teleport + Aura + Ripple</div></div>
              <div class="pill">Teleport</div>
            </div>
          </div>
          <div class="bd">
            <div class="stage" id="stage">
              <img class="layer base" src="https://picsum.photos/seed/magic_user/900/1200" />
              <div class="sparkle-overlay"></div>
              ${body}${border}${pallu}${blouseLayer}${accLayers}
            </div>
          </div>
        </div>

        <div class="card"><div class="bd">
          <div class="h2">Controls</div>
          <div class="divider"></div>
          <div class="label">User Name</div>
          <input class="input" value="${escapeHtml(state.userName)}" data-act="setUser" />
          <div style="height:10px"></div>
          <div class="label">Hue</div>
          <input class="range" type="range" min="-45" max="45" value="0" data-act="hue" />
          <div class="divider"></div>
          <div class="label">Sarees</div>
          <div class="row">
            ${(state.sarees || []).slice(0, 10).map(it => `<button class="btn small ${saree?.id===it.id?"primary":""}" data-act="pickSaree" data-id="${it.id}">${escapeHtml(it.name).slice(0, 14)}</button>`).join("")}
          </div>
          <div style="height:10px"></div>
          <div class="label">Blouses</div>
          <div class="row">
            ${(state.blouses || []).slice(0, 10).map(it => `<button class="btn small ${blouse?.id===it.id?"primary":""}" data-act="pickBlouse" data-id="${it.id}">${escapeHtml(it.name).slice(0, 14)}</button>`).join("")}
          </div>
          <div style="height:10px"></div>
          <div class="label">Accessories</div>
          <div class="row">
            ${(state.accessories || []).slice(0, 12).map(it => {
              const on = (state.selected.accessories || []).some(a => a.id === it.id);
              return `<button class="btn small ${on?"primary":""}" data-act="toggleAcc" data-id="${it.id}">${escapeHtml(it.name).slice(0, 14)}</button>`;
            }).join("")}
          </div>
        </div></div>
      </div>
    </div>
  `;
}

function mirrorPage() {
  const saree = state.selected.saree;
  return `
    <div class="wrap">
      <div class="card"><div class="bd">
        <div class="h1">Magic Mirror</div>
        <div class="muted" style="margin-top:8px">Camera ON + overlay saree layers + tilt gravity.</div>
        <div class="row" style="margin-top:12px">
          <button class="btn primary" data-act="startCam">Start</button>
          <button class="btn" data-act="stopCam">Stop</button>
          <button class="btn" data-act="tiltPerm">Enable Tilt</button>
        </div>
      </div></div>

      <div class="grid two" style="margin-top:14px">
        <div class="card"><div class="bd">
          <div class="stage" style="background:#000">
            <video id="cam" class="layer base" playsinline style="transform: scaleX(-1)" muted></video>
            <div class="layer" style="box-shadow: inset 0 -80px 120px rgba(0,0,0,0.25)"></div>
            ${saree?.layer_body_png ? `<img class="layer teleport aura" style="mix-blend-mode:multiply; opacity:.92" src="${saree.layer_body_png}" />` : ""}
            ${saree?.layer_border_png ? `<img class="layer teleport aura" style="mix-blend-mode:screen; opacity:.92" src="${saree.layer_border_png}" />` : ""}
            ${saree?.layer_pallu_png ? `<img id="mirrorPallu" class="layer teleport aura" style="mix-blend-mode:multiply; opacity:.92; transform-origin: 40% 20%" src="${saree.layer_pallu_png}" />` : ""}
          </div>
          <div class="muted" style="margin-top:10px">Tip: mobile browser pe tilt best.</div>
        </div></div>
        <div class="card"><div class="bd">
          <div class="h2">Choose Saree</div>
          <div class="row" style="margin-top:10px">
            ${(state.sarees || []).slice(0, 12).map(it => `<button class="btn small ${saree?.id===it.id?"primary":""}" data-act="pickSaree" data-id="${it.id}">${escapeHtml(it.name).slice(0, 14)}</button>`).join("")}
          </div>
        </div></div>
      </div>
    </div>
  `;
}

function looksShell() {
  return `
    <div class="wrap">
      <div class="card"><div class="bd">
        <div class="h1">Saved Looks</div>
        <div class="muted" style="margin-top:8px">Card save + WhatsApp share.</div>
        <div class="row" style="margin-top:12px">
          <button class="btn primary" data-act="saveLook">Save Card</button>
          <button class="btn" data-act="share">Share WhatsApp</button>
        </div>
      </div></div>

      <div class="card" style="margin-top:14px"><div class="bd">
        <div class="h2">History</div>
        <div class="muted" style="margin-top:6px">Latest saves are listed here.</div>
        <div class="divider"></div>
        <div id="looksList" class="list"></div>
      </div></div>
    </div>
  `;
}

function adminPage() {
  return `
    <div class="wrap">
      <div class="card"><div class="bd">
        <div class="h1">Admin</div>
        <div class="muted" style="margin-top:8px">Token-protected CRUD + uploads.</div>
        <div class="divider"></div>
        <div class="label">Admin Token</div>
        <input class="input" value="${escapeHtml(state.adminToken)}" placeholder="MAGIC_ADMIN_TOKEN" data-act="setToken" />
        <div class="row" style="margin-top:10px">
          <button class="btn primary" data-act="saveToken">Save Token</button>
          <button class="btn" data-act="refreshAdmin">Refresh</button>
        </div>
      </div></div>

      <div class="grid two" style="margin-top:14px">
        <div class="card"><div class="bd">
          <div class="row" style="justify-content: space-between">
            <div class="h2">Products</div>
            <div class="row">
              <button class="btn small primary" data-act="addSaree">Add Saree</button>
              <button class="btn small" data-act="addBlouse">Add Blouse</button>
              <button class="btn small" data-act="addAcc">Add Accessory</button>
            </div>
          </div>
          <div class="divider"></div>
          <div class="h2" style="font-size:14px">Sarees (select one for layer upload)</div>
          <div id="adminSarees" class="list" style="margin-top:10px"></div>
          <div class="divider"></div>
          <div class="h2" style="font-size:14px">Blouses</div>
          <div id="adminBlouses" class="list" style="margin-top:10px"></div>
          <div class="divider"></div>
          <div class="h2" style="font-size:14px">Accessories</div>
          <div id="adminAcc" class="list" style="margin-top:10px"></div>
        </div></div>

        <div class="card"><div class="bd">
          <div class="h2">Uploads</div>
          <div class="muted" style="margin-top:6px">Saree layers for better fit.</div>
          <div class="divider"></div>
          <div class="label">Selected Saree ID</div>
          <input class="input" value="${escapeHtml(String(state.selectedSareeId || ""))}" data-act="setSelectedSaree" placeholder="Click a saree in list" />
          <div style="height:10px"></div>
          <div class="row">
            <input type="file" id="upBody" />
            <button class="btn small primary" data-act="uploadLayer" data-kind="body">Upload Body</button>
          </div>
          <div class="row" style="margin-top:8px">
            <input type="file" id="upPallu" />
            <button class="btn small primary" data-act="uploadLayer" data-kind="pallu">Upload Pallu</button>
          </div>
          <div class="row" style="margin-top:8px">
            <input type="file" id="upBorder" />
            <button class="btn small primary" data-act="uploadLayer" data-kind="border">Upload Border</button>
          </div>
          <div class="divider"></div>
          <div class="h2">Magic UX ON/OFF</div>
          <div id="adminFlags" class="row" style="margin-top:10px"></div>
        </div></div>
      </div>
    </div>
  `;
}

function routeView() {
  if (state.route === "/studio") return studioPage();
  if (state.route === "/mirror") return mirrorPage();
  if (state.route === "/looks") return looksShell();
  if (state.route === "/admin") return adminPage();
  return homePage();
}

async function render() {
  app.innerHTML = topbar() + routeView() + toastUi() + bottomNav();
  wireActions();
  if (state.route === "/looks") await refreshLooks();
  if (state.route === "/admin") await refreshAdmin();
}

async function refreshLooks() {
  const listEl = document.getElementById("looksList");
  if (!listEl) return;
  try {
    const r = await apiGet("/gallery/looks");
    const items = r.items || [];
    listEl.innerHTML = items.slice(0, 30).map(l => `
      <div class="item">
        <div class="t">Look #${l.id}</div>
        <div class="s">${escapeHtml(l.user_name || "Guest")} · ${escapeHtml(l.created_at || "")}</div>
        ${l.image_card_png ? `<div class="s"><a href="${l.image_card_png}" target="_blank">Card image</a></div>` : ""}
      </div>
    `).join("");
  } catch (e) {
    listEl.innerHTML = `<div class="muted">Failed to load looks: ${escapeHtml(e.message)}</div>`;
  }
}

async function refreshAdmin() {
  if (!state.adminToken) return;
  const sEl = document.getElementById("adminSarees");
  const bEl = document.getElementById("adminBlouses");
  const aEl = document.getElementById("adminAcc");
  const fEl = document.getElementById("adminFlags");
  if (!sEl || !bEl || !aEl || !fEl) return;

  try {
    const flags = await apiGet("/admin/uxflags", hdrAdmin());
    const fItems = flags.items || [];
    fEl.innerHTML = fItems.map(f => `<button class="btn small ${f.enabled?"primary":""}" data-act="toggleFlag" data-key="${escapeHtml(f.key)}" data-enabled="${f.enabled ? "1" : "0"}">${escapeHtml(f.key)}: ${f.enabled?"ON":"OFF"}</button>`).join("");
  } catch (e) {
    fEl.innerHTML = `<div class="muted">Enter valid token to manage flags.</div>`;
  }

  sEl.innerHTML = (state.sarees || []).slice(0, 30).map(s => `
    <div class="item">
      <div class="t">#${s.id} ${escapeHtml(s.name)}</div>
      <div class="s">₹${s.price} · ${escapeHtml(s.primary_color || "")}</div>
      <div class="row" style="margin-top:8px">
        <button class="btn small" data-act="selectSareeAdmin" data-id="${s.id}">Select</button>
        <button class="btn small" data-act="delSaree" data-id="${s.id}">Delete</button>
      </div>
    </div>
  `).join("");

  bEl.innerHTML = (state.blouses || []).slice(0, 30).map(b => `
    <div class="item">
      <div class="t">#${b.id} ${escapeHtml(b.name)}</div>
      <div class="s">₹${b.price}</div>
      <div class="row" style="margin-top:8px">
        <input type="file" data-kind="blouse" data-id="${b.id}" />
        <button class="btn small primary" data-act="uploadBlouse" data-id="${b.id}">Upload</button>
        <button class="btn small" data-act="delBlouse" data-id="${b.id}">Delete</button>
      </div>
    </div>
  `).join("");

  aEl.innerHTML = (state.accessories || []).slice(0, 30).map(a => `
    <div class="item">
      <div class="t">#${a.id} ${escapeHtml(a.name)}</div>
      <div class="s">₹${a.price}</div>
      <div class="row" style="margin-top:8px">
        <input type="file" data-kind="acc" data-id="${a.id}" />
        <button class="btn small primary" data-act="uploadAcc" data-id="${a.id}">Upload</button>
        <button class="btn small" data-act="delAcc" data-id="${a.id}">Delete</button>
      </div>
    </div>
  `).join("");

  wireActions();
}

let camStream = null;

async function startCam() {
  try {
    const video = document.getElementById("cam");
    camStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
    video.srcObject = camStream;
    await video.play();
    toast("Camera started.");
  } catch (e) {
    toast(e.message || "Camera error");
  }
}

function stopCam() {
  if (camStream) camStream.getTracks().forEach(t => t.stop());
  camStream = null;
  const video = document.getElementById("cam");
  if (video) video.srcObject = null;
  toast("Camera stopped.");
}

async function enableTilt() {
  try {
    if (typeof DeviceOrientationEvent?.requestPermission === "function") {
      const res = await DeviceOrientationEvent.requestPermission();
      if (res !== "granted") throw new Error("Tilt permission denied");
    }
  } catch {
    // continue anyway
  }

  window.addEventListener("deviceorientation", (ev) => {
    const gamma = Number(ev.gamma || 0);
    const beta = Number(ev.beta || 0);
    const x = Math.max(-12, Math.min(12, gamma / 4));
    const y = Math.max(-12, Math.min(12, beta / 8));
    const p = document.getElementById("mirrorPallu");
    if (p) p.style.transform = `translate(${x}px, ${y}px) rotate(${x * 0.6}deg)`;
  });
  toast("Tilt enabled.");
}

function applyHue(deg) {
  const stage = document.getElementById("stage");
  if (!stage) return;
  stage.querySelectorAll("img.layer").forEach((img) => {
    if (img.classList.contains("base")) return;
    img.style.filter = `hue-rotate(${deg}deg) saturate(1.15)`;
  });
}

async function saveLook() {
  const saree = state.selected.saree;
  const total =
    (saree?.price || 0) +
    (state.selected.blouse?.price || 0) +
    (state.selected.accessories || []).reduce((s, a) => s + (a.price || 0), 0);
  const title = (saree?.name || "My Look").replaceAll("&", "and");
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="${escapeXml(saree?.primary_color || "#db2777")}" stop-opacity="0.45"/>
          <stop offset="1" stop-color="#0b1220" stop-opacity="1"/>
        </linearGradient>
      </defs>
      <rect width="900" height="1200" fill="url(#g)"/>
      <text x="60" y="120" fill="white" font-size="46" font-weight="800">Boutique Magic</text>
      <text x="60" y="190" fill="rgba(255,255,255,.82)" font-size="26">Look Card</text>
      <text x="60" y="300" fill="white" font-size="40" font-weight="700">${escapeXml(title).slice(0, 26)}</text>
      <text x="60" y="360" fill="rgba(255,255,255,.82)" font-size="26">By ${escapeXml(state.userName)}</text>
      <text x="60" y="470" fill="white" font-size="44" font-weight="900">₹${total}</text>
      <text x="60" y="530" fill="rgba(255,255,255,.72)" font-size="22">${escapeXml(new Date().toLocaleDateString())}</text>
    </svg>
  `.trim();
  const dataUrl = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
  await apiPost("/gallery/save", {
    user_name: state.userName,
    saree_id: saree?.id || null,
    blouse_id: state.selected.blouse?.id || null,
    accessories_json: JSON.stringify((state.selected.accessories || []).map(a => a.id)),
    image_card_png: dataUrl,
  });
  toast("Saved look card.");
  location.hash = "#/looks";
  state.route = "/looks";
  await render();
}

async function share() {
  const saree = state.selected.saree;
  const total =
    (saree?.price || 0) +
    (state.selected.blouse?.price || 0) +
    (state.selected.accessories || []).reduce((s, a) => s + (a.price || 0), 0);
  const r = await apiPost("/look/share", { user_name: state.userName, look_name: saree?.name || "My Look", price: `₹${total}` });
  window.open(r.whatsapp_url, "_blank");
  toast("WhatsApp share opened.");
}

function wireActions() {
  document.querySelectorAll("[data-act]").forEach((el) => {
    const act = el.getAttribute("data-act");
    if (el._wired) return;
    el._wired = true;
    el.addEventListener("click", async (e) => {
      const t = e.currentTarget;
      try {
        if (act === "pickSaree") {
          const id = Number(t.getAttribute("data-id"));
          const s = state.sarees.find((x) => x.id === id);
          state.selected.saree = s || null;
          if (s?.primary_color) setMagicColor(s.primary_color);
          toast("Perfect pallu flow detected!");
          render();
        }
        if (act === "pickBlouse") {
          const id = Number(t.getAttribute("data-id"));
          state.selected.blouse = state.blouses.find((x) => x.id === id) || null;
          toast("Neon border glow engaged.");
          render();
        }
        if (act === "toggleAcc") {
          const id = Number(t.getAttribute("data-id"));
          const item = state.accessories.find((x) => x.id === id);
          if (!item) return;
          const on = state.selected.accessories.some((x) => x.id === id);
          state.selected.accessories = on
            ? state.selected.accessories.filter((x) => x.id !== id)
            : [...state.selected.accessories, item];
          toast("Tap fabric to reveal hidden patterns.");
          render();
        }
        if (act === "startCam") await startCam();
        if (act === "stopCam") stopCam();
        if (act === "tiltPerm") await enableTilt();
        if (act === "saveLook") await saveLook();
        if (act === "share") await share();

        if (act === "saveToken") {
          localStorage.setItem("magic.admin", state.adminToken);
          toast("Saved admin token.");
          await refreshAdmin();
        }
        if (act === "refreshAdmin") await refreshAdmin();

        if (act === "addSaree") {
          await apiPost("/sarees", { name: "New Saree", price: 1999, primary_color: "#db2777", tags: "festive" }, hdrAdmin());
          await loadCatalog(); toast("Saree added."); await refreshAdmin();
        }
        if (act === "addBlouse") {
          await apiPost("/blouses", { name: "New Blouse", price: 799, primary_color: "#7c3aed", tags: "match" }, hdrAdmin());
          await loadCatalog(); toast("Blouse added."); await refreshAdmin();
        }
        if (act === "addAcc") {
          await apiPost("/accessories", { name: "New Accessory", price: 299, primary_color: "#0ea5e9", tags: "sparkle" }, hdrAdmin());
          await loadCatalog(); toast("Accessory added."); await refreshAdmin();
        }
        if (act === "delSaree") {
          const id = Number(t.getAttribute("data-id"));
          await apiDel(`/sarees/${id}`, hdrAdmin()); await loadCatalog(); toast("Deleted."); await refreshAdmin();
        }
        if (act === "delBlouse") {
          const id = Number(t.getAttribute("data-id"));
          await apiDel(`/blouses/${id}`, hdrAdmin()); await loadCatalog(); toast("Deleted."); await refreshAdmin();
        }
        if (act === "delAcc") {
          const id = Number(t.getAttribute("data-id"));
          await apiDel(`/accessories/${id}`, hdrAdmin()); await loadCatalog(); toast("Deleted."); await refreshAdmin();
        }
        if (act === "selectSareeAdmin") {
          state.selectedSareeId = Number(t.getAttribute("data-id"));
          toast(`Selected saree #${state.selectedSareeId}`);
          render();
          await refreshAdmin();
        }
        if (act === "uploadLayer") {
          const kind = t.getAttribute("data-kind");
          if (!state.selectedSareeId) throw new Error("Select a saree first");
          const inputId = kind === "body" ? "upBody" : kind === "pallu" ? "upPallu" : "upBorder";
          const inp = document.getElementById(inputId);
          const file = inp?.files?.[0];
          if (!file) throw new Error("Choose file");
          const path = await uploadFile(`/upload/saree-layer`, file, `?kind=${encodeURIComponent(kind)}`);
          const field = kind === "body" ? "layer_body_png" : kind === "pallu" ? "layer_pallu_png" : "layer_border_png";
          await apiPut(`/sarees/${state.selectedSareeId}`, { [field]: path }, hdrAdmin());
          await loadCatalog();
          toast(`Uploaded ${kind}.`);
          await refreshAdmin();
        }
        if (act === "uploadBlouse") {
          const id = Number(t.getAttribute("data-id"));
          const file = document.querySelector(`input[type=file][data-kind="blouse"][data-id="${id}"]`)?.files?.[0];
          if (!file) throw new Error("Choose file");
          const path = await uploadFile(`/upload/blouse-template`, file);
          await apiPut(`/blouses/${id}`, { template_png: path }, hdrAdmin());
          await loadCatalog();
          toast("Uploaded blouse template.");
          await refreshAdmin();
        }
        if (act === "uploadAcc") {
          const id = Number(t.getAttribute("data-id"));
          const file = document.querySelector(`input[type=file][data-kind="acc"][data-id="${id}"]`)?.files?.[0];
          if (!file) throw new Error("Choose file");
          const path = await uploadFile(`/upload/accessory`, file);
          await apiPut(`/accessories/${id}`, { image_png: path }, hdrAdmin());
          await loadCatalog();
          toast("Uploaded accessory.");
          await refreshAdmin();
        }
        if (act === "toggleFlag") {
          const key = t.getAttribute("data-key");
          const enabled = t.getAttribute("data-enabled") === "1";
          await apiPost(`/admin/uxflags/${encodeURIComponent(key)}`, { enabled: !enabled }, hdrAdmin());
          toast(`${key} -> ${!enabled ? "ON" : "OFF"}`);
          await refreshAdmin();
        }
      } catch (err) {
        toast(err.message || "Error");
      }
    });
  });

  document.querySelectorAll('input[data-act="setToken"]').forEach((el) => {
    if (el._wired) return;
    el._wired = true;
    el.addEventListener("input", (e) => (state.adminToken = e.target.value));
  });
  document.querySelectorAll('input[data-act="setUser"]').forEach((el) => {
    if (el._wired) return;
    el._wired = true;
    el.addEventListener("input", (e) => {
      state.userName = e.target.value;
      localStorage.setItem("magic.user", state.userName);
    });
  });
  document.querySelectorAll('input[data-act="setSelectedSaree"]').forEach((el) => {
    if (el._wired) return;
    el._wired = true;
    el.addEventListener("input", (e) => {
      const v = Number(e.target.value || 0);
      state.selectedSareeId = v || null;
    });
  });
  document.querySelectorAll('input[data-act="hue"]').forEach((el) => {
    if (el._wired) return;
    el._wired = true;
    el.addEventListener("input", (e) => applyHue(Number(e.target.value || 0)));
  });

  const stage = document.getElementById("stage");
  if (stage && !stage._wired) {
    stage._wired = true;
    stage.addEventListener("click", (e) => {
      if (!isOn("ripple_reveal")) return;
      const r = stage.getBoundingClientRect();
      const x = e.clientX - r.left;
      const y = e.clientY - r.top;
      const span = document.createElement("span");
      span.className = "ripple";
      span.style.left = `${x}px`;
      span.style.top = `${y}px`;
      stage.appendChild(span);
      setTimeout(() => span.remove(), 700);
      toast("Tap fabric to reveal hidden patterns.");
    });
  }
}

function onRoute() {
  state.route = (location.hash || "#/").replace("#", "") || "/";
  render();
}

(async function boot() {
  try {
    await Promise.all([loadCatalog(), loadUx()]);
  } catch {
    // ignore
  }
  if (!location.hash) location.hash = "#/";
  window.addEventListener("hashchange", onRoute);
  onRoute();
})();
