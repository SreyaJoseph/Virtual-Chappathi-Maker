import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 1. SCENE SETUP
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 7);

const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#c'),
    antialias: true,
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true; // Enable shadows for more realism

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.minDistance = 2;
controls.maxDistance = 15;


// 2. LIGHTING
scene.add(new THREE.AmbientLight(0xffffff, 0.5));

const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
dirLight.position.set(3, 7, 5);
dirLight.castShadow = true; // This light will cast shadows
dirLight.shadow.mapSize.width = 2048;
dirLight.shadow.mapSize.height = 2048;
scene.add(dirLight);


// 3. ADVANCED TEXTURES
const textureLoader = new THREE.TextureLoader();

// PBR textures for a realistic material
const colorMap = textureLoader.load('http://googleusercontent.com/image_collection/image_retrieval/5698560383455182505_0');
const normalMap = textureLoader.load('http://googleusercontent.com/image_collection/image_retrieval/1191373613339845870_0');
const displacementMap = textureLoader.load('http://googleusercontent.com/image_collection/image_retrieval/11957329501701732718_0');
const roughnessMap = textureLoader.load('http://googleusercontent.com/image_collection/image_retrieval/11617237029228573622_0');


// 4. CREATE THE IRREGULAR CHAPPATHI GEOMETRY
// Start with a high-resolution plane to allow for detailed displacement
const geometry = new THREE.PlaneGeometry(8, 8, 256, 256);

// Deform the plane into an imperfect circle and add thickness
const positions = geometry.attributes.position;
const vertex = new THREE.Vector3();
const center = new THREE.Vector2(0, 0);

for (let i = 0; i < positions.count; i++) {
    vertex.fromBufferAttribute(positions, i);
    let dist = center.distanceTo(new THREE.Vector2(vertex.x, vertex.y));

    // Make the edge slightly irregular by varying the radius
    let radius = 4.0 + (Math.random() - 0.5) * 0.1;

    // Cut off vertices outside the radius to make it circular
    if (dist > radius) {
        // Instead of discarding, push them down to create a rounded edge
        vertex.setZ(-0.2);
    }
    positions.setXYZ(i, vertex.x, vertex.y, vertex.z);
}
geometry.computeVertexNormals(); // Recalculate normals after deformation

// Add a second side to the chappathi to give it thickness
const bottomGeometry = geometry.clone();
bottomGeometry.rotateX(Math.PI); // Flip it
// (Note: For a production model, you would merge these and stitch the edges)


// 5. CREATE THE REALISTIC MATERIAL & MESH
const chappathiMaterial = new THREE.MeshStandardMaterial({
    map: colorMap,
    normalMap: normalMap,         // Adds fine surface detail
    displacementMap: displacementMap,   // Creates large bumps and puffs
    displacementScale: 0.35,      // How high the bumps are. Crucial for realism!
    roughnessMap: roughnessMap,       // Controls shininess vs. matte areas
    roughness: 0.8,               // Base roughness
    metalness: 0.0,               // Non-metallic surface
});

const chappathiTop = new THREE.Mesh(geometry, chappathiMaterial);
chappathiTop.receiveShadow = true;
chappathiTop.castShadow = true;

const chappathiBottom = new THREE.Mesh(bottomGeometry, chappathiMaterial);
chappathiBottom.receiveShadow = true;
chappathiBottom.castShadow = true;

// Group both sides together
const chappathi = new THREE.Group();
chappathi.add(chappathiTop);
chappathi.add(chappathiBottom);

chappathi.rotation.x = -Math.PI / 2; // Lay it flat
scene.add(chappathi);


// Add a simple ground plane to receive shadows
const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({ color: '#FFF', roughness: 0.9 })
);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.2; // Position it just below the chappathi
ground.receiveShadow = true;
scene.add(ground);


// 6. ANIMATION LOOP
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();