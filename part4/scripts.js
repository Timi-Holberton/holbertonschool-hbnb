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
    }
        // on récupère les places
    fetchPlaces(token).then(places => {
        if (places) {
            displayPlaces(places) // affiche les places
        } else {
            console.error("aucun lieu trouvé ou reçu")
        }
    }); // Et on récupère les lieux avec le token
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
    const placesList = document.getElementById('places-list') // Récupère l'élément HTML qui contiendra les lieux

    placesList.innerHTML = ''; // Vide le contenu précédent, super !

    places.forEach(place => { // Parcourt chaque objet "place" du tableau
        const placeDiv = document.createElement('div'); // Crée un nouvel élément <div> pour le lieu
        placeDiv.className='place-list-index'; // Ajoute les classes CSS pour le style

        const imagePlace = {
            "Minas Tirith": "images/Minas-tirith.jpg",
            "Gouffre de Helm": "images/helm.jpg",
            "Fondcombe": "images/fondcombe.jpg",
            "Mordor": "images/mordor.jpg",
            "Mines of Moria": "images/mine-moria.jpg",
            "The Prancing Pony": "images/pony.jpg"
        }

        const image = document.createElement('img');
        image.src = imagePlace[place.title] || "images/default.jpg";
        image.alt = place.title;
        image.classList.add('place-image-index');


        const title = document.createElement('h2'); // Crée un élément <h2> pour le titre
        title.textContent = place.title; // Récupère le titre depuis la base de données

        const price = document.createElement('p');
        price.textContent = `Price by night: ${place.price} €`;

        const viewButton = document.createElement('button');
        viewButton.textContent = 'View détail';
        viewButton.classList.add('details-button-index'); // Applique mon style css

        viewButton.addEventListener('click', () => {
            window.location.href = `place.html?place_id=${place.id}`;
        });


        console.log(place);
        placeDiv.appendChild(image);
        placeDiv.appendChild(title);
        placeDiv.appendChild(price);
        placeDiv.appendChild(viewButton);

        placesList.appendChild(placeDiv); // Ajoute le div au conteneur principal
        placeDiv.setAttribute('data-price', place.price);
    })
}

/*Filtre prix*/
document.addEventListener('DOMContentLoaded', () => { //une fois le DOM chargé, on exécute
    const priceFilter = document.getElementById('price-filter'); // récupère l'élément <select> du filtre prix html

    const options = [ // Option des filtres
        { value: 'all', text: 'All' },
        { value: '10', text: '10 €' },
        { value: '50', text: '50 €' },
        { value: '100', text: '100 €' }
    ];

    options.forEach(opt => { // parcourt chaque option et l'ajoute dans le menu déroulant du filtre
        const option = document.createElement('option'); // créer l'élément <option>
        option.value = opt.value; // définit la valeur de l'option
        option.textContent = opt.text; // affiche l'option dans le menu déroulant
        priceFilter.appendChild(option); // ajoute l'option à l'élément <select>
    });

    // écoute si changement de valeur du filtre par l'utilisateur
    priceFilter.addEventListener('change', () => {
        const selected = priceFilter.value; // récupère la valeur
        const maxPrice = selected === 'all' ? Infinity : parseInt(selected); // convertir la veleur en nombre, et all = infini

        // parcourt tous les lieux
        document.querySelectorAll('.place-list-index').forEach(placeCard => {
            const price = parseInt(placeCard.getAttribute('data-price')); // récup le prix de la place grâce à l'attribut data
            if (price <= maxPrice) {
                placeCard.style.display = 'block'; // affiche le lieu si correspond au filtre
            } else {
                placeCard.style.display = 'none'; // ne l'affiche pas dans le cas contraire
            }
        });
    });
});


const chaineRequete = window.location.search; // Récupérer la chaîne de requête dans l'URL (tout ce qui suit le ?)
const parametres = new URLSearchParams(chaineRequete); // réer un objet URLSearchParams pour manipuler facilement les paramètres
const placeId = parametres.get('place_id'); // Récupérer la valeur du paramètre 'place_id' (ou le nom que tu utilises)

console.log("ID du lieu extrait de l'URL :", placeId); // Afficher dans la console pour vérification

// Faire la requête vers l'API pour récupérer les détails
fetch(`http://localhost:5000/api/v1/places/${placeId}`) // Requête vers l'API pour obtenir les données d’un lieu par son ID
    .then(response => {
        if (!response.ok) { // Vérifie si la réponse est correcte
            throw new Error('Lieu non trouvé'); // Gère le cas d'erreur HTTP
        }
        return response.json(); // Convertit la réponse en JSON
    })
    .then(data => {
        document.getElementById('place-title').textContent = data.title; // Affiche le titre du lieu
        document.getElementById('host-name').textContent =
    'Host : ' + (data.owner ? `${data.owner.first_name} ${data.owner.last_name}` : 'Inconnu'); // Affiche le nom de l'hôte ou "Inconnu"
        document.getElementById('place-description').textContent = data.description; // Affiche la description du lieu
        document.getElementById('place-price').textContent = `${data.price}€`; // Affiche le prix du lieu

        const amenitiesList = document.getElementById('place-amenities'); // Récupère l’élément <ul> pour les équipements
        if (data.amenities && data.amenities.length > 0) { // Vérifie s'il y a des équipements
            amenitiesList.innerHTML = data.amenities
                .map(a => `<li>${a.name}</li>`) // Crée une <li> par équipement
                .join(''); // Assemble toutes les <li> en une seule chaîne HTML
        } else {
            amenitiesList.innerHTML = '<li>Aucun équipement listé</li>'; // Affiche un message si aucun équipement
        }
    })
    .catch(error => {
        console.error(error); // Affiche une erreur en cas d’échec de la requête
    });


