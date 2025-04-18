<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bloch Sphere Visualization</title>
  <style>
    body { margin: 0; }
    canvas { display: block}
  </style>
</head>
<body>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <script>
    // Create a scene
    var scene = new THREE.Scene();

    // Set up camera and renderer
    var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Create a sphere geometry for the Bloch sphere
    var sphereGeometry = new THREE.SphereGeometry(5, 32, 32);
    var sphereMaterial = new THREE.MeshBasicMaterial({ color: 0x7f7f7f, wireframe: true });
    var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    scene.add(sphere);

    // Function to plot a quantum state on the Bloch sphere
    function plotQuantumState(theta, phi, color) {
      var x = 5 * Math.sin(theta) * Math.cos(phi);
      var y = 5 * Math.sin(theta) * Math.sin(phi);
      var z = 5 * Math.cos(theta);
      
      var pointGeometry = new THREE.SphereGeometry(0.2, 8, 8);
      var pointMaterial = new THREE.MeshBasicMaterial({ color: color });
      var point = new THREE.Mesh(pointGeometry, pointMaterial);
      point.position.set(x, y, z);
      scene.add(point);
    }

    // Plot some example quantum states on the Bloch sphere
    // |0⟩ state at the north pole (0,0)
    plotQuantumState(0, 0, 0xff0000); // Red

    // |1⟩ state at the south pole (pi,0)
    plotQuantumState(Math.PI, 0, 0x0000ff); // Blue

    // |+⟩ state on the equator (pi/2,0)
    plotQuantumState(Math.PI / 2, 0, 0x00ff00); // Green

    // |−⟩ state on the equator (pi/2, pi)
    plotQuantumState(Math.PI / 2, Math.PI, 0xffff00); // Yellow

    // Set camera position
    camera.position.z = 15;

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
