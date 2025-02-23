/**
 * Navigator.js
 *
 * Navigate between slides
 */


window.addEventListener("keydown", e => {
  const root = `${window.location.protocol}//${window.location.host}/`;

  let target = null;
  switch (e.key) {
    case "0":
      if (window.sxp.prev) {
        target = `${root}${window.sxp.first}`;
      }
      break;
    case "ArrowLeft":
      if (window.sxp.prev) {
        target = `${root}${window.sxp.prev}`;
      }
      break;
    case "ArrowRight":
      if (window.sxp.next) {
        target = `${root}${window.sxp.next}`;
      }
      break;
    case "Escape":
      target = root;
      break;
  }
  if (target !== null) {
    window.location.href = target;
    e.preventDefault();
  }
});
