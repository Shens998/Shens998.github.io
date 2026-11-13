'use strict';
const profileDetails = [...document.querySelectorAll('details')];
let detailState;
window.addEventListener('beforeprint', () => {
  if (detailState) return;
  detailState = profileDetails.map(item => item.open);
  profileDetails.forEach(item => { item.open = true; });
});
window.addEventListener('afterprint', () => {
  if (!detailState) return;
  profileDetails.forEach((item, index) => { item.open = detailState[index]; });
  detailState = undefined;
});
document.querySelector('#print-profile').addEventListener('click', () => window.print());
