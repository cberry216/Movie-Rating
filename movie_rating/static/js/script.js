function setDifferenceFont() {
  let sourceRatingDiffs = document.querySelectorAll('.source-rating__diff');
  if(sourceRatingDiffs) {
    for(let i = 0; i < sourceRatingDiffs.length; i++) {
      let diff = Number.parseFloat(sourceRatingDiffs[i].innerHTML);
      if(diff) {
        if(diff < 0) {
          sourceRatingDiffs[i].classList.toggle('source-rating__diff--red');
        } else {
          sourceRatingDiffs[i].classList.toggle('source-rating__diff--green');
        }
      }
    }
  }
}

function setDifferenceArrows() {
  let sourceRatings = document.querySelectorAll('.source-rating');
  for(let i = 0; i < sourceRatings.length; i++) {
    let diff = Number.parseFloat(sourceRatings[i].querySelector('.source-rating__diff').innerHTML);
    if(diff) {
      let arrow = sourceRatings[i].querySelector('.source-rating__arrow polyline');
      if(diff < 0) {
        arrow.setAttribute('transform', 'rotate(180,10,10)');
        arrow.setAttribute('fill', 'red');
        arrow.setAttribute('stroke', 'red');
      } else {
        arrow.setAttribute('fill', 'green');
        arrow.setAttribute('stroke', 'green');
      }
    }
  }
}

function setRatingColors() {
  let userRating = document.querySelector('.user-rating__rating');
  let imdbRating = document.querySelector('.imdb-rating .source-rating__rating');
  let rtRating = document.querySelector('.rt-rating .source-rating__rating');
  let globalRating = document.querySelector('.global-rating .source-rating__rating');

  if(userRating) {
    let rating = Number.parseFloat(userRating.innerHTML);
    let greenFactor = 25.5 * rating;
    let redFactor = 255 - greenFactor;
    userRating.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0`);
  }

  if(imdbRating) {
    let rating = Number.parseFloat(imdbRating.innerHTML);
    let greenFactor = 25.5 * rating;
    let redFactor = 255 - greenFactor;
    imdbRating.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0`);
  }

  if(rtRating) {
    let rating = Number.parseInt(rtRating.innerHTML);
    let greenFactor = 2.55 * rating;
    let redFactor = 255 - greenFactor;
    rtRating.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0)`);
  }

  if(globalRating) {
    let rating = Number.parseFloat(globalRating.innerHTML);
    let greenFactor = 25.5 * rating;
    let redFactor = 255 - greenFactor;
    globalRating.setAttribute('style', `color: rgb(${redFactor},${greenFactor},0`);
  }
}

function run() {
  setDifferenceArrows();
  setDifferenceFont();
  setRatingColors();
}

window.onload = run;