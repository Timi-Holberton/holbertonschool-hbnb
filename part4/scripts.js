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

/* Vérifier authentification du user */
function checkAuthentication() {
    console.log('checkAuthentication sur la page :', window.location.pathname); // Affiche la page actuelle

    const token = getCookie('token'); // Récupère le token JWT depuis les cookies
    const loginLink = document.getElementById('login-link'); // Récupère le lien de connexion dans le DOM

    if (!token) loginLink.style.display = 'block'; // Affiche le lien si pas de token
    else loginLink.style.display = 'none'; // Masque le lien si token présent

    if (document.getElementById('places-list')) { // Vérifie si l'élément 'places-list' existe dans la page
        fetchPlaces(token).then(places => { // Récupère la liste des lieux avec le token
            if (places) displayPlaces(places); // Affiche les lieux s'ils existent
            else console.error("aucun lieu trouvé ou reçu"); // Log d'erreur si aucun lieu reçu
        });
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
    const placesList = document.getElementById('places-list') // Récupère l'élément HTML qui contiendra les lieux
    console.log('Dans displayPlaces, placesList =', placesList);
    if (!placesList) {
        console.error('L’élément #places-list est introuvable dans le DOM au moment de l’exécution');
        return; // éviter de planter le script
    }

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

    if (!priceFilter) return; // quitte la fonction si l'élément n'existe pas (ex : sur place.html)

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


// Fonction pour extraire l'ID du lieu depuis l'URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search); // Crée un objet pour lire les paramètres URL
    return params.get('place_id'); // Retourne la valeur de place_id
}

// Fonction asynchrone qui récupère les détails d'un lieu depuis l'API avec authentification
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, { // Envoi d'une requête GET vers l'API pour obtenir les détails du lieu identifié par placeId
            method: 'GET', // Méthode HTTP GET
            headers: {
                'Content-Type': 'application/json', // Indique que la réponse attendue est au format JSON
                'Authorization': `Bearer ${token}` // En-tête Authorization avec token JWT pour authentification
            }
        });

        if (!response.ok) { // Vérifie si la réponse HTTP est valide (status 200-299)
            throw new Error(`Erreur API : ${response.status}`); // En cas d'erreur, lance une exception avec le code statut HTTP
        }

        const data = await response.json(); // Parse la réponse JSON pour obtenir les données du lieu
        displayPlaceDetails(data); // Appelle la fonction d'affichage en lui passant les données récupérées
    } catch (error) {
        console.error('Erreur lors de la récupération des détails :', error); // Affiche une erreur dans la console en cas de problème lors de la requête
        const section = document.getElementById('place-details'); // Sélectionne la section HTML qui doit contenir les détails
        section.textContent = 'Erreur lors du chargement des détails du lieu.'; // Affiche un message d'erreur à l'utilisateur dans la page
    }
}

// Fonction qui crée et insère dynamiquement les éléments HTML avec les données du lieu
function displayPlaceDetails(place) {
    const section = document.getElementById('place-details'); // Récupère la section HTML où afficher les détails
    section.innerHTML = ''; // Vide le contenu actuel de la section pour repartir à zéro

    const titre = document.createElement('h2'); // Crée un élément <h2> pour le titre du lieu
    titre.className = 'titre-details-place'; // Ajoute une classe CSS pour le style
    titre.textContent = place.title || 'Titre non disponible'; // Remplit le titre avec le nom du lieu ou un texte par défaut
    section.appendChild(titre); // Ajoute ce titre dans la section détails

    const hostSpan = document.createElement('span'); // Crée un élément <span> pour afficher le nom de l'hôte
    hostSpan.className = 'host-label'; // Ajoute une classe CSS pour le style
    const ownerName = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Inconnu'; // Construit le nom complet de l'hôte ou met "Inconnu"
    hostSpan.textContent = 'Host : ' + ownerName; // Affecte le texte dans le <span>
    section.appendChild(hostSpan); // Ajoute le <span> dans la section

    const infoDiv = document.createElement('div'); // Crée une <div> conteneur pour les infos complémentaires
    infoDiv.className = 'place-info'; // Ajoute une classe CSS pour le style

    const description = document.createElement('p'); // Crée un paragraphe pour la description
    description.className = 'description'; // Ajoute une classe CSS
    description.textContent = place.description || 'Pas de description.'; // Ajoute la description ou un message par défaut
    infoDiv.appendChild(description); // Ajoute le paragraphe dans la div info

    const price = document.createElement('p'); // Crée un paragraphe pour le prix
    price.className = 'price'; // Ajoute une classe CSS

    const priceLabel = document.createElement('span'); // Crée un <span> pour le libellé "Price by night"
    priceLabel.className = 'text-price'; // Ajoute une classe CSS
    priceLabel.textContent = 'Price by night : '; // Définit le texte du label

    const priceValue = document.createElement('span'); // Crée un <span> pour la valeur du prix
    priceValue.className = 'price-button'; // Ajoute une classe CSS
    priceValue.textContent = place.price ? `${place.price}€` : 'Non précisé'; // Met le prix ou un texte alternatif

    price.appendChild(priceLabel); // Ajoute le label dans le paragraphe prix
    price.appendChild(priceValue); // Ajoute la valeur du prix dans le paragraphe
    infoDiv.appendChild(price); // Ajoute le paragraphe prix dans la div info

    const amenitiesTitle = document.createElement('h3'); // Crée un titre pour la section équipements
    amenitiesTitle.textContent = 'Amenities :'; // Définit le texte du titre
    infoDiv.appendChild(amenitiesTitle); // Ajoute le titre dans la div info

    const amenitiesList = document.createElement('ul'); // Crée une liste à puces pour les équipements
    amenitiesList.id = 'place-amenities'; // Attribue un id pour ciblage CSS ou JS

    if (place.amenities && place.amenities.length > 0) { // Si des équipements existent
        place.amenities.forEach(a => { // Pour chaque équipement
            const li = document.createElement('li'); // Crée un élément de liste
            li.textContent = a.name; // Met le nom de l'équipement
            amenitiesList.appendChild(li); // Ajoute l'élément à la liste
        });
    } else {
        const li = document.createElement('li'); // Sinon crée un seul élément de liste
        li.textContent = 'Aucun équipement listé'; // Avec un message d'absence d'équipement
        amenitiesList.appendChild(li); // Ajoute cet élément à la liste
    }
    infoDiv.appendChild(amenitiesList); // Ajoute la liste des équipements dans la div info

    section.appendChild(infoDiv); // Ajoute la div info complète à la section principale
}

document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token'); // Récupère le token JWT stocké dans les cookies
    const placeId = getPlaceIdFromURL(); // Récupère l’ID du lieu depuis les paramètres URL
    const placeDetailsElement = document.getElementById('place-details'); // Cherche l’élément #place-details dans le DOM

    if (placeDetailsElement) { // Ce bloc ne s'exécute que sur place.html
        if (placeId) {
            fetchPlaceDetails(token, placeId); // Si ID présent, on charge les détails
        } else {
            placeDetailsElement.textContent = 'Aucun lieu spécifié dans l’URL.'; // Sinon, message d’erreur
        }
    }
});


/*-------------------------Reviews-------------------------*/
// Lorsque la page est entièrement chargée
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form'); // Récupère le formulaire d'envoi d'avis
    const token = checkAuthentication(); // Vérifie si l'utilisateur est connecté (via un token JWT)
    const placeId = getPlaceIdFromURL(); // Récupère l'identifiant du lieu à partir de l'URL

    // Si l'utilisateur n'est pas authentifié, on cache le formulaire de soumission
    if (!token && reviewForm) {
        reviewForm.style.display = 'none';
    }

    // On affiche les avis existants pour tous les visiteurs, connectés ou non
    if (placeId) {
    loadReviews(placeId);
    }

    // Si l'utilisateur est connecté, on lui permet de soumettre un avis
    if (reviewForm && token) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Empêche l'envoi classique du formulaire

            const reviewText = document.getElementById('review-text').value; // Texte saisi par l'utilisateur
            const response = await submitReview(token, placeId, reviewText); // Envoie de la requête POST à l'API
            handleResponse(response); // Traitement de la réponse
        });
    }
});

/* clique sur le titre "Add review" pour rediriger vers le login */
document.addEventListener('DOMContentLoaded', () => {
    const addReviewTitle = document.getElementById('add-review-title');
    const token = getCookie('token');
    if (addReviewTitle && !token) {
        addReviewTitle.style.cursor = 'pointer';
        addReviewTitle.addEventListener('click', () => {
            window.location.href = '/login.html';
        });
    }
});



// Fonction pour envoyer un avis au serveur via l'API
async function submitReview(token, placeId, reviewText) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST', // On envoie une requête POST
            headers: {
                'Content-Type': 'application/json', // On précise qu'on envoie du JSON
                'Authorization': `Bearer ${token}` // On ajoute le jeton JWT dans l'en-tête d'autorisation
            },
            body: JSON.stringify({
                place_id: placeId, // On inclut l'identifiant du lieu
                text: reviewText // Et le contenu de l'avis
            })
        });
        return response; // On retourne la réponse pour qu'elle soit traitée ailleurs
    } catch (error) {
        // Si une erreur réseau survient, on l'affiche et on alerte l'utilisateur
        console.error('Erreur lors de l\'envoi de l\'avis :', error);
        alert('Erreur réseau. Veuillez réessayer.');
    }
}

// Fonction qui gère la réponse de l'API après envoi d'un avis
function handleResponse(response) {
    if (!response) return; // Si aucune réponse n’est retournée, on ne fait rien

    if (response.ok) {
        // Si la réponse est positive (code 2xx)
        alert('Review submitted successfully!'); // Message de confirmation
        document.getElementById('review-form').reset(); // On vide le formulaire
        location.reload(); // Et on recharge la page pour afficher le nouvel avis
    } else {
        // Si la requête a échoué (erreur côté client ou serveur)
        alert('Failed to submit review');
    }
}

// Fonction pour charger et afficher les avis existants d’un lieu donné
function loadReviews(placeId) {
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`)  // Requête pour récupérer les avis d’un lieu donné
        .then(response => response.json())  // Transformation de la réponse en JSON
        .then(data => {
            const reviewContainer = document.getElementById('reviews');  // Récupère le conteneur unique des avis dans la page
            reviewContainer.innerHTML = ''; // Vide le contenu actuel des avis
            data.forEach(review => {
                const div = document.createElement('div');  // Crée un élément div pour chaque avis
                div.classList.add('review');  // Ajoute la classe CSS "review" au div
                div.innerHTML = `<p>${review.text}</p>`;  // Insère le texte de l’avis dans un paragraphe
                reviewContainer.appendChild(div);  // Ajoute le div dans le conteneur des avis
            });
        })
        .catch(error => {
            console.error('Erreur lors du chargement des avis :', error);  // Affiche une erreur en cas d’échec de la requête
        });
}
