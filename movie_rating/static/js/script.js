function setRatingColor() {
  console.log('Setting rating color...');
  let userRatingElement = document.querySelector('.user-rating__user-rating');
  let memberRatingElements = document.querySelectorAll('.member-rating__value');

  let userRating = Number.parseFloat(userRatingElement.innerHTML);
  let greenFactor = 25.5 * userRating;
  let redFactor = 255 - greenFactor;
  userRatingElement.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0)`);

  for(let i = 0; i < memberRatingElements.length; i++) {
    let memberRating = Number.parseFloat(memberRatingElements[i].innerHTML);
    let greenFactor = 25.5 * memberRating;
    let redFactor = 255 - greenFactor;
    memberRatingElements[i].setAttribute('style', `color: rgb(${redFactor},${greenFactor},0)`);
  }
}

function setDeltaColor() {
  console.log('Setting delta colors...');
  let ratingDiffs = document.querySelectorAll('.user-rating__diff');
  let memberRatingDiffs = document.querySelectorAll('.member-rating__diff');
  for(let i = 0; i < ratingDiffs.length; i++) {
    let text = ratingDiffs[i].innerHTML;
    let value = Number.parseFloat(text);
    if(value >= 0) {
      ratingDiffs[i].classList.toggle('user-rating__diff--positive');
    }
    else {
      ratingDiffs[i].classList.toggle('user-rating__diff--negative');
    }
  }
  for (let i = 0; i < memberRatingDiffs.length; i++) {
    let text = memberRatingDiffs[i].innerHTML;
    if(text.includes("N/A")) {
      continue;
    }
    let value = Number.parseFloat(text);
    if (value >= 0) {
      memberRatingDiffs[i].classList.toggle('rating__diff--positive');
    }
    else {
      memberRatingDiffs[i].classList.toggle('rating__diff--negative');
    }
  }
}

function run() {
  setRatingColor();
  setDeltaColor();
}

window.onload = run;