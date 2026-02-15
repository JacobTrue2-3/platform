export function formatDate(el) {
  el.textContent = new Date(el.textContent).toLocaleString();
}

document.querySelectorAll(".date-field").forEach(el => {
  formatDate(el);
});