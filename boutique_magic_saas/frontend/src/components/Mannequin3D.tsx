import { useEffect, useRef, useState } from "react";
import * as THREE from "three";

export default function Mannequin3D({
  textureUrl,
  bodyScale
}: {
  textureUrl: string | null;
  bodyScale: number;
}) {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!mountRef.current) return;
    const mount = mountRef.current;
    const w = mount.clientWidth;
    const h = Math.max(320, Math.round(w * 1.05));

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf1f5f9);

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100);
    camera.position.set(0, 1.4, 3.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(w, h);
    mount.appendChild(renderer.domElement);

    const light1 = new THREE.DirectionalLight(0xffffff, 0.9);
    light1.position.set(2, 3, 2);
    scene.add(light1);
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));

    const group = new THREE.Group();
    group.scale.setScalar(bodyScale);
    scene.add(group);

    // Simple mannequin (dummy 3D body)
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xf8d7c4, roughness: 0.75, metalness: 0.0 });
    const torso = new THREE.Mesh(new THREE.CapsuleGeometry(0.5, 1.05, 6, 16), bodyMat);
    torso.position.set(0, 1.2, 0);
    group.add(torso);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.28, 16, 16), bodyMat);
    head.position.set(0, 2.15, 0);
    group.add(head);
    const hips = new THREE.Mesh(new THREE.SphereGeometry(0.55, 16, 16), bodyMat);
    hips.scale.set(1.05, 0.7, 1.0);
    hips.position.set(0, 0.75, 0);
    group.add(hips);

    // Saree wrap (plane with texture)
    const wrapGeom = new THREE.CylinderGeometry(0.72, 0.86, 1.55, 40, 1, true);
    const wrapMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.9,
      metalness: 0.0,
      transparent: true,
      opacity: 0.95,
      side: THREE.DoubleSide
    });
    const wrap = new THREE.Mesh(wrapGeom, wrapMat);
    wrap.position.set(0, 1.05, 0);
    group.add(wrap);

    if (textureUrl) {
      const loader = new THREE.TextureLoader();
      loader.load(
        textureUrl,
        (tex) => {
          tex.wrapS = THREE.RepeatWrapping;
          tex.wrapT = THREE.RepeatWrapping;
          tex.repeat.set(1.2, 1.2);
          wrapMat.map = tex;
          wrapMat.needsUpdate = true;
          setReady(true);
        },
        undefined,
        () => setReady(true)
      );
    } else {
      setReady(true);
    }

    // Drag rotate
    let dragging = false;
    let lastX = 0;
    const onDown = (e: PointerEvent) => {
      dragging = true;
      lastX = e.clientX;
      (e.target as any).setPointerCapture?.(e.pointerId);
    };
    const onMove = (e: PointerEvent) => {
      if (!dragging) return;
      const dx = e.clientX - lastX;
      lastX = e.clientX;
      group.rotation.y += dx * 0.01;
    };
    const onUp = () => {
      dragging = false;
    };
    renderer.domElement.addEventListener("pointerdown", onDown);
    renderer.domElement.addEventListener("pointermove", onMove);
    renderer.domElement.addEventListener("pointerup", onUp);
    renderer.domElement.addEventListener("pointercancel", onUp);

    let raf = 0;
    const tick = () => {
      raf = requestAnimationFrame(tick);
      renderer.render(scene, camera);
    };
    tick();

    const onResize = () => {
      const nw = mount.clientWidth;
      const nh = Math.max(320, Math.round(nw * 1.05));
      camera.aspect = nw / nh;
      camera.updateProjectionMatrix();
      renderer.setSize(nw, nh);
    };
    window.addEventListener("resize", onResize);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", onResize);
      renderer.domElement.removeEventListener("pointerdown", onDown);
      renderer.domElement.removeEventListener("pointermove", onMove);
      renderer.domElement.removeEventListener("pointerup", onUp);
      renderer.domElement.removeEventListener("pointercancel", onUp);
      mount.removeChild(renderer.domElement);
      renderer.dispose();
    };
  }, [textureUrl, bodyScale]);

  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
      <div className="p-3 flex items-center justify-between">
        <div>
          <div className="font-bold">3D Mannequin (Simple Mode)</div>
          <div className="text-xs opacity-70">Drag to rotate 360°</div>
        </div>
        <div className="text-xs opacity-70">{ready ? "Ready" : "Loading"}</div>
      </div>
      <div ref={mountRef} className="w-full" />
    </div>
  );
}

