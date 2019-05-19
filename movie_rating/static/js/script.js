function setRatingColor() {
  console.log('Setting rating color...');
  let userRatingElement = document.querySelector('.rating__user-rating');
  let userRating = Number.parseFloat(userRatingElement.innerHTML);
  greenFactor = (25.5 * userRating);
  redFactor = 255 - greenFactor;
  userRatingElement.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0)`);
}

function setDeltaColor() {
  console.log('Setting delta colors...');
  let ratingDiffs = document.querySelectorAll('.rating__diff');
  for(let i = 0; i < ratingDiffs.length; i++) {
    let text = ratingDiffs[i].innerHTML;
    let value = Number.parseFloat(text);
    if(value >= 0) {
      ratingDiffs[i].classList.toggle('rating__diff--positive');
    }
    else {
      ratingDiffs[i].classList.toggle('rating__diff--negative');
    }
  }
}

function run() {
  setRatingColor();
  setDeltaColor();
}

window.onload = run;