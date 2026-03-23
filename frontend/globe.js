/**
 * Wireframe rotating globe — vanilla JS port of DotGlobeHero.
 * Requires Three.js loaded before this script.
 */
(function () {
  'use strict';

  function initGlobe() {
    const canvas = document.getElementById('globe-canvas');
    if (!canvas || typeof THREE === 'undefined') return;

    const W = () => canvas.parentElement.offsetWidth;
    const H = () => canvas.parentElement.offsetHeight;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(W(), H());
    renderer.setClearColor(0x000000, 0);

    // Scene + camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, W() / H(), 0.1, 100);
    camera.position.set(0, 0, 3.2);

    // Globe geometry — wireframe sphere
    const radius = 1;
    const geo = new THREE.SphereGeometry(radius, 36, 24);
    const mat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      wireframe: true,
      transparent: true,
      opacity: 0.13,
    });
    const globe = new THREE.Mesh(geo, mat);
    scene.add(globe);

    // Equator ring (slightly brighter)
    const ringGeo = new THREE.TorusGeometry(radius, 0.003, 6, 80);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.25 });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    scene.add(ring);

    // Ambient dot particles scattered around the globe
    const dotCount = 120;
    const dotGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(dotCount * 3);
    for (let i = 0; i < dotCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = radius + 0.02 + Math.random() * 0.18;
      positions[i * 3]     = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.cos(phi);
      positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
    }
    dotGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const dotMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.022, transparent: true, opacity: 0.35 });
    const dots = new THREE.Points(dotGeo, dotMat);
    scene.add(dots);

    // Mouse-influenced tilt
    let targetTiltX = 0;
    let targetTiltY = 0;
    let currentTiltX = 0;
    let currentTiltY = 0;

    window.addEventListener('mousemove', (e) => {
      targetTiltX = ((e.clientY / window.innerHeight) - 0.5) * 0.3;
      targetTiltY = ((e.clientX / window.innerWidth)  - 0.5) * 0.3;
    }, { passive: true });

    // Resize
    window.addEventListener('resize', () => {
      camera.aspect = W() / H();
      camera.updateProjectionMatrix();
      renderer.setSize(W(), H());
    });

    // Animation loop
    let frame = 0;
    function animate() {
      requestAnimationFrame(animate);
      frame++;

      // Slow auto-rotation
      globe.rotation.y += 0.0018;
      dots.rotation.y  += 0.0012;
      ring.rotation.y  += 0.0018;

      // Smooth mouse tilt
      currentTiltX += (targetTiltX - currentTiltX) * 0.05;
      currentTiltY += (targetTiltY - currentTiltY) * 0.05;
      globe.rotation.x = currentTiltX;
      dots.rotation.x  = currentTiltX * 0.6;
      ring.rotation.x  = currentTiltX + Math.PI / 2;

      renderer.render(scene, camera);
    }
    animate();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlobe);
  } else {
    initGlobe();
  }
})();
