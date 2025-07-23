/* Login */
document.addEventListener('DOMContentLoaded', () => { // Quand le DOM est entièrement chargé
    const loginForm = document.getElementById('login-form'); // On récupère le formulaire de connexion

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => { // On intercepte la soumission du formulaire
            event.preventDefault(); // On empêche le rechargement de la page
            const email = document.getElementById('email').value; // On récupère l'email
            const password = document.getElementById('password').value; // On récupère le mot de passe
            await loginUser(email, password); // On appelle la fonction de connexion
        });
    }
});

async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', { // Envoi d'une requête POST à l'API de login
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Indique que les données sont envoyées en JSON
        },
        body: JSON.stringify({ email, password }) // Corps de la requête contenant les identifiants
    });

    if (response.ok) {
        const data = await response.json(); // Si la réponse est OK, on parse les données JSON
        document.cookie = `token=${data.access_token}; path=/`; // On stocke le token dans un cookie
        window.location.href = 'index.html'; // On redirige l'utilisateur vers la page d'accueil
    } else {
        alert('Login failed: ' + response.statusText); // Affichage d'une alerte en cas d'échec
    }
}


/* Mettre reviews dans bonne place */
document.addEventListener("DOMContentLoaded", () => { // Quand le DOM est prêt
    document.querySelectorAll(".review-card").forEach(review => { // Pour chaque review
        const placeId = review.getAttribute("data-place"); // On récupère l'identifiant du lieu associé
        const placeArticle = document.getElementById(placeId); // On récupère l'article HTML correspondant à ce lieu
        if (placeArticle) {
            placeArticle.appendChild(review); // On insère la review dans l'article correspondant
        }
    });
});


/* Vérifier authentification du user */
function checkAuthentication() {
    console.log('checkAuthentication appelé'); // Log de débogage
    const token = getCookie('token'); // Récupération du token depuis les cookies
    console.log('token dans cookie:', token); // Log du token
    const loginLink = document.getElementById('login-link'); // On récupère le lien de connexion

    if (!token) {
        console.log("Aucun token => affichage du lien de connexion"); // Si pas de token, on montre le lien
        loginLink.style.display = 'block';
    } else {
        console.log("Token trouvé => on masque le lien de connexion"); // Sinon, on le masque
        loginLink.style.display = 'none';
        // on récupère les places
        fetchPlaces(token).then(places => {
            if (places) {
                displayPlaces(places) // affiche les places
            } else {
                console.error("aucun lieu trouvé ou reçu")
            }
        }); // Et on récupère les lieux avec le token
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';'); // On sépare tous les cookies
    for (let cookie of cookies) {
        cookie = cookie.trim(); // On enlève les espaces superflus
        if (cookie.startsWith(name + '=')) { // Si on trouve le cookie voulu
            return cookie.substring(name.length + 1); // On retourne sa valeur
        }
    }
    return null; // Si rien trouvé, on retourne null
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication(); // Appel de la vérification d'authentification à chaque chargement de page
});


async function fetchPlaces(token) {
    console.log("Je vais chercher les places...");
    const response = await fetch("http://localhost:5000/api/v1/places", { // Requête GET vers l'API des lieux
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Envoi du token dans l'en-tête Authorization
        },
    });

    if (response.ok) {
        const data = await response.json(); // Si tout va bien, on récupère les données JSON
        console.log("Lieux récupérés :", data); // Log des lieux
        return data; // On retourne les données
    } else {
        console.error("Erreur lors de la récupération des lieux :", response.status); // En cas d'erreur
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById('places-list')

    placesList.innerHTML = ''; // Vide le contenu précédent, super !

    places.forEach(place => {
        const placeDiv = document.createElement('div'); // Crée un nouvel élément <div> pour le lieu
        placeDiv.className='place-info';
        placeDiv.textContent = place.title; //affiche le titre des places
        placesList.appendChild(placeDiv); // Ajoute le div au conteneur principal
    })
}
