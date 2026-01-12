function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
    hash |= 0; // convierte a 32bit
  }
  return hash;
}

function colorFromString(str) {
  const hash = hashString(str);

  const r = (hash >> 16) & 255;
  const g = (hash >> 8) & 255;
  const b = hash & 255;

  return { r: Math.abs(r), g: Math.abs(g), b: Math.abs(b) };
}

function getContrastColor({ r, g, b }) {
  const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
  return luminance > 186 ? '#000000' : '#ffffff';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.scope-badge').forEach(badge => {
    const text = badge.dataset.scope || badge.textContent.trim();
    const color = colorFromString(text);

    badge.style.backgroundColor = `rgb(${color.r}, ${color.g}, ${color.b})`;
    badge.style.color = getContrastColor(color);
  });
});
