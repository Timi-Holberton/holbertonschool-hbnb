/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });


document.querySelectorAll('.review-card').forEach(review => {
    const placeName = review.dataset.place;
    const place = document.querySelector(`.place-info[data-place-name="${placeName}"]`);

    if (place) {
        // Crée une div pour les reviews si elle n’existe pas
        let reviewSection = place.querySelector('.place-reviews');
        if (!reviewSection) {
            reviewSection = document.createElement('div');
            reviewSection.classList.add('place-reviews');
            place.appendChild(reviewSection);
        }

        reviewSection.appendChild(review);
    }
});
