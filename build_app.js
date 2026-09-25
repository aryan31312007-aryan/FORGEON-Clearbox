const fs = require('fs');
const path = require('path');

const wwwDir = path.join(__dirname, 'www');

if (!fs.existsSync(wwwDir)) {
    fs.mkdirSync(wwwDir, { recursive: true });
}

const filesToCopy = [
    'index.html',
    'manifest.json',
    'sw.js',
    'icon-192.png',
    'icon-512.png',
    'favicon.ico'
];

filesToCopy.forEach(file => {
    const src = path.join(__dirname, file);
    const dest = path.join(wwwDir, file);
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
        console.log(`Copied ${file} -> www/`);
    } else {
        console.warn(`Warning: ${file} not found!`);
    }
});

console.log('\n[SUCCESS] Mobile app web bundle prepared in www/ folder!');
