function randomColor() {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return { r, g, b };
}

function getContrastColor({ r, g, b }) {
  // Luminancia según WCAG
  const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
  return luminance > 186 ? '#000000' : '#ffffff';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.scope-badge').forEach(badge => {
    const color = randomColor();
    const bgColor = `rgb(${color.r}, ${color.g}, ${color.b})`;
    const textColor = getContrastColor(color);

    badge.style.backgroundColor = bgColor;
    badge.style.color = textColor;
  });
});
