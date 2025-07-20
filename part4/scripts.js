/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
  });

/* Mettre reviews dans bonne place */
document.addEventListener("DOMContentLoaded", () => {
  // Pour chaque review
  document.querySelectorAll(".review-card").forEach(review => {
    const placeId = review.getAttribute("data-place");
    const placeArticle = document.getElementById(placeId);
    if (placeArticle) {
      placeArticle.appendChild(review); // On ajoute la review au bon article
    }
  });
});

/* Login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Your code to handle form submission
        });
    }
});

async function loginUser(email, password) {
    const response = await fetch('https://your-api-url/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle the response
}

if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
} else {
    alert('Login failed: ' + response.statusText);
}
*/
