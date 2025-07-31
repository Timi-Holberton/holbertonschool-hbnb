/*---------------------------------------------------------------------------*/
/*-----------------------------------Login-----------------------------------*/
/*---------------------------------------------------------------------------*/

/**
* @file login.js
* @description Handles the login form submission once the DOM is loaded.
* Intercepts the form submission to prevent the page from reloading.
* Retrieves the user's credentials and calls the login function.
*
* @event DOMContentLoaded
* Triggered when the DOM is fully loaded.
*
* @function loginUser
* Function called to authenticate the user (must be defined elsewhere).
*/
document.addEventListener('DOMContentLoaded', () => {                   // Quand le DOM est entièrement chargé
    const loginForm = document.getElementById('login-form');            // On récupère le formulaire de connexion

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {         // On intercepte la soumission du formulaire
            event.preventDefault();                                     // On empêche le rechargement de la page
            const email = document.getElementById('email').value;       // On récupère l'email
            const password = document.getElementById('password').value; // On récupère le mot de passe
            await loginUser(email, password);                           // On appelle la fonction de connexion
        });
    }
});


/**
* Sends a POST request to the API to authenticate a user with an email address and password.
* If the login is successful, stores the JWT token in a cookie and redirects to the next page.
* Otherwise, displays an alert with the error message.
*
* @param {string} email - The user's email address
* @param {string} password - The user's password
* @returns {Promise<void>} Returns nothing, redirects, or displays an alert
*/
async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {  // Envoi de la requête POST à l'API d'authentification
        method: 'POST',                                             // Méthode HTTP POST
        headers: {
            'Content-Type': 'application/json'                      // Spécifie que le corps de la requête est au format JSON
        },
        body: JSON.stringify({ email, password })                   // Corps de la requête contenant l'email et le mot de passe au format JSON
    });

    if (response.ok) {                                              // Si la réponse est positive (code HTTP 2xx)
        const data = await response.json();                         // Extraction du JSON de la réponse
        document.cookie = `token=${data.access_token}; path=/`;     // Stockage du token JWT dans un cookie accessible sur tout le site

        const params = new URLSearchParams(window.location.search); // Récupération des paramètres de l'URL actuelle
        const next = params.get('next') || '/index.html';           // Récupération de la valeur du paramètre 'next', ou page d'accueil par défaut

        window.location.href = next;                                // Redirection vers la page demandée dans 'next'
    } else {
        alert('Login failed: ' + response.statusText);              // Affichage d'une alerte en cas d'échec de connexion
    }
}

/**
* Checks for the presence of a JWT token to determine the user's authentication status.
* Dynamically updates the "Login" or "Logout" link based on login.
* Handles logout by removing the token and redirecting to the home page.
* If the page contains a list of locations, retrieves and displays those locations via the API.
*/
function checkAuthentication() {
    console.log('checkAuthentication sur la page :', window.location.pathname); // Affiche la page actuelle dans la console

    const token = getCookie('token');                           // Récupère le token JWT dans les cookies
    const loginLink = document.getElementById('login-link');    // Récupère le lien "Login" / "Logout"

    if (!loginLink) return;                     // Sort si le lien n'existe pas dans le DOM

    if (!token) {                               // Pas de token => utilisateur non connecté, affiche "Login"
        loginLink.style.display = 'block';
        loginLink.textContent = 'Login';
        loginLink.href = '/login.html';
        loginLink.onclick = null;               // Supprime tout gestionnaire d'événement
    } else {                                    // Token présent => utilisateur connecté, affiche "Logout"
        loginLink.style.display = 'block';
        loginLink.textContent = 'Logout';
        loginLink.href = '#';

        loginLink.onclick = (e) => {
            e.preventDefault();                                                 // Empêche le comportement par défaut du lien
            document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'; // Supprime le cookie token
            window.location.href = '/index.html';                               // Redirige vers la page d'accueil
        };
    }
    if (document.getElementById('places-list')) {       // Si la page contient la liste des lieux, récupère et affiche ces lieux
        fetchPlaces(token).then(places => {
            if (places) displayPlaces(places);
            else console.error("no location found or received");
        });
    }
}

/**
* Retrieves the value of a cookie given by its name.
*
* @param {string} name - The name of the cookie to search for
* @returns {string|null} The value of the cookie if found, otherwise null
*/
function getCookie(name) {
    const cookies = document.cookie.split(';');         // On sépare tous les cookies
    for (let cookie of cookies) {
        cookie = cookie.trim();                         // On enlève les espaces superflus
        if (cookie.startsWith(name + '=')) {            // Si on trouve le cookie voulu
            return cookie.substring(name.length + 1);   // On retourne sa valeur
        }
    }
    return null;                                        // Si rien trouvé, on retourne null
}


/**
 * Extracts the user ID from a JWT token payload.
 * Decodes the Base64Url-encoded payload, parses the JSON, and returns the user ID.
 *
 * @param {string} token - The JWT token string
 * @returns {string|null} The user ID found in the token payload (user_id or sub), or null if decoding fails
 */
function getUserIdFromToken(token) {                                            // récupère l'id dans le token
    try {
        const base64Url = token.split('.')[1];                                  // Partie payload encodée en base64url
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');         // Conversion base64url -> base64 standard
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
            '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)               // Décodage URL-encoding caractère par caractère
        ).join(''));                                                            // Reconstruction de la chaîne JSON
        const payload = JSON.parse(jsonPayload);                                // Conversion JSON en objet JS
        return payload.user_id || payload.sub;                                  // Retourne user_id ou sub selon champ présent dans token

    } catch (e) {
        console.error("Token decoding error:", e);      // Affiche erreur en cas de problème
        return null;                                    // Retourne null si échec du décodage
    }
}

/**
* Adds an event listener for when the DOM is fully loaded.
* Calls the `checkAuthentication` function on each page load
* to check the user's login status.
*/
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();                              // Appel de la vérification d'authentification à chaque chargement de page
});

/*---------------------------------------------------------------------------*/
/*------------------------------List Place-----------------------------------*/
/*---------------------------------------------------------------------------*/
/**
* Retrieves the list of locations from the API using an authentication token.
*
* @param {string} token - The JWT token for authentication
* @returns {Promise<Array|undefined>} A promise that resolves to an array of locations if the request succeeds, otherwise undefined
*/
async function fetchPlaces(token) {
    console.log("Je vais chercher les places...");
    const response = await fetch("http://localhost:5000/api/v1/places", {   // Requête GET vers l'API des lieux
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`          // Envoi du token dans l'en-tête Authorization
        },
    });

    if (response.ok) {
        const data = await response.json();             // Si tout va bien, on récupère les données JSON
        console.log("Lieux récupérés :", data);         // Log des lieux
        return data;                                    // On retourne les données
    } else {
        console.error("Error retrieving locations:", response.status);      // En cas d'erreur
    }
}


/**
 * Affiche une liste de lieux dans l'élément HTML avec l'id 'places-list'.
 * Pour chaque lieu, crée dynamiquement un bloc contenant une image, un titre,
 * un prix et un bouton permettant de voir les détails.
 *
 * @param {Array} places - Tableau d'objets représentant les lieux à afficher
 */
function displayPlaces(places) {
    const placesList = document.getElementById('places-list')// Récupère l'élément HTML qui contiendra les lieux
    console.log('Dans displayPlaces, placesList =', placesList);
    if (!placesList) {
        console.error('The #places-list element was not found in the DOM at runtime');
        return;                                             // éviter de planter le script
    }

    placesList.innerHTML = '';                              // Vide les ancienne place affiché avant

    places.forEach(place => {                               // Parcourt chaque objet "place" du tableau
        const placeDiv = document.createElement('div');     // Crée un nouvel élément <div> pour le lieu
        placeDiv.className='place-list-index';              // Ajoute les classes CSS pour le style

        const imagePlace = {
            "Minas Tirith": "images/Minas-tirith.jpg",      // Mappage titre → image
            "Gouffre de Helm": "images/helm.jpg",
            "Fondcombe": "images/fondcombe.jpg",
            "Mordor": "images/mordor.jpg",
            "Mines of Moria": "images/mine-moria.jpg",
            "The Prancing Pony": "images/pony.jpg"
        }

        const image = document.createElement('img');                    // créer une image
        image.src = imagePlace[place.title] || "images/default.jpg";    // choix de l'image
        image.alt = place.title;                                        // text alternatif
        image.classList.add('place-image-index');                       // classe css image


        const title = document.createElement('h2');     // Crée un élément <h2> pour le titre
        title.textContent = place.title;                // Récupère le titre depuis la base de données

        const price = document.createElement('p');              //créer un paragraphe pour le prix
        price.textContent = `Price by night: ${place.price} €`; // affiche le prix

        const viewButton = document.createElement('button');    // créer un bouton
        viewButton.textContent = 'View détail';                 // texte du bouton
        viewButton.classList.add('details-button-index');       // Applique mon style css

        viewButton.addEventListener('click', () => {            // clic sur bouton qui dirige vers détail place
            window.location.href = `place.html?place_id=${place.id}`;
        });


        console.log(place);
        placeDiv.appendChild(image);        // ajoute les éléments au div
        placeDiv.appendChild(title);
        placeDiv.appendChild(price);
        placeDiv.appendChild(viewButton);

        placesList.appendChild(placeDiv);                 // Ajoute le div au conteneur principal
        placeDiv.setAttribute('data-price', place.price); // Attribut data-price pour le style et pour le filtre
    })
}

/**
* @file price_filter.js
* @description Manages the price filter on the location index page.
* Allows the user to dynamically filter the displayed location cards
* based on the price selected from a drop-down menu.
*
* How it works:
* - Waits for the DOM to fully load.
* - Dynamically inserts options into the price filter.
* - Filters the displayed locations based on the selected value.
*
* Locations must have the `data-price` attribute specified in their HTML tag.
* Encoding: UTF-8
*/
document.addEventListener('DOMContentLoaded', () => {               //une fois le DOM chargé, on exécute
    const priceFilter = document.getElementById('price-filter');    // récupère l'élément <select> du filtre prix html

    if (!priceFilter) return;                                       // quitte la fonction si l'élément n'existe pas (ex : sur place.html)

    const options = [                           // Option des filtres
        { value: 'all', text: 'All' },
        { value: '10', text: '10 €' },
        { value: '50', text: '50 €' },
        { value: '100', text: '100 €' }
    ];

    options.forEach(opt => {                                // parcourt chaque option et l'ajoute dans le menu déroulant du filtre
        const option = document.createElement('option');    // créer l'élément <option>
        option.value = opt.value;                           // définit la valeur de l'option
        option.textContent = opt.text;                      // affiche l'option dans le menu déroulant
        priceFilter.appendChild(option);                    // ajoute l'option à l'élément <select>
    });

    priceFilter.addEventListener('change', () => {                              // écoute si changement de valeur du filtre par l'utilisateur
        const selected = priceFilter.value;                                     // récupère la valeur
        const maxPrice = selected === 'all' ? Infinity : parseInt(selected);    // convertir la veleur en nombre, et all = infini

        document.querySelectorAll('.place-list-index').forEach(placeCard => {   // parcourt tous les lieux
            const price = parseInt(placeCard.getAttribute('data-price'));       // récup le prix de la place grâce à l'attribut data
            if (price <= maxPrice) {
                placeCard.style.display = 'block';                              // affiche le lieu si correspond au filtre
            } else {
                placeCard.style.display = 'none';                               // ne l'affiche pas dans le cas contraire
            }
        });
    });
});

/*---------------------------------------------------------------------------*/
/*------------------------------Place Détail---------------------------------*/
/*---------------------------------------------------------------------------*/
/**
* Retrieves a place's ID (`place_id`) from the page's URL.
* Uses the URLSearchParams object to extract parameters from the query string.
* @returns {string|null} The place's ID if present in the URL, otherwise `null`.
*/
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);     // Crée un objet pour lire les paramètres URL
    return params.get('place_id');                                  // Retourne la valeur de place_id
}

/**
* Retrieves a place's details from the API and displays them on the page.
*
* Sends an authenticated HTTP GET request to the `/places/:place_id` endpoint to retrieve
* the data for a specific accommodation, identified by its ID.
* If successful, the data is passed to the display function.
* If an error occurs, a message is displayed in the appropriate section.
*
* @param {string} token - JWT token used to authenticate the request.
* @param {string} placeId - Unique identifier of the place to retrieve.
*
* @returns {Promise<void>} Returns nothing, but triggers a DOM update.
*/
async function fetchPlaceDetails(token, placeId) {
    try {  // Envoi d'une requête GET vers l'API pour obtenir les détails du lieu identifié par placeId
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',                                                      // Méthode HTTP GET
            headers: {
                'Content-Type': 'application/json',            // Indique que la réponse attendue est au format JSON
                'Authorization': `Bearer ${token}`             // En-tête Authorization avec token JWT pour authentification
            }
        });

        if (!response.ok) {                                             // Vérifie si la réponse HTTP est valide (status 200-299)
            throw new Error(`Erreur API : ${response.status}`);         // En cas d'erreur, lance une exception avec le code statut HTTP
        }

        const data = await response.json();         // Parse la réponse JSON pour obtenir les données du lieu
        displayPlaceDetails(data);                  // Appelle la fonction d'affichage en lui passant les données récupérées
    } catch (error) {
        console.error('Error retrieving details :', error);         // Affiche une erreur dans la console en cas de problème lors de la requête
        const section = document.getElementById('place-details');   // Sélectionne la section HTML qui doit contenir les détails
        section.textContent = 'Error loading location details.';    // Affiche un message d'erreur à l'utilisateur dans la page
    }
}

/**
 * Dynamically creates and inserts DOM elements to display detailed information
 * about a specific place (title, host, description, price, amenities, and image).
 *
 * Clears any existing content in the target section (`#place-details`)
 * and builds the content using the provided `place` object.
 *
 * @param {Object} place - The place data object returned from the API.
 * @param {string} place.title - Title of the place.
 * @param {string} [place.description] - Description of the place.
 * @param {number} [place.price] - Price per night in euros.
 * @param {Object} [place.owner] - Owner information object.
 * @param {string} [place.owner.first_name] - Owner’s first name.
 * @param {string} [place.owner.last_name] - Owner’s last name.
 * @param {Array} [place.amenities] - Array of amenity objects with a `name` property.
 *
 * @returns {void} Does not return anything; modifies the DOM directly.
 */
function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');       // Récupère la section HTML où afficher les détails
    section.innerHTML = '';                                         // Vide le contenu actuel de la section

    const titre = document.createElement('h2');                 // Crée un élément <h2> pour le titre du lieu
    titre.className = 'titre-details-place';                    // Ajoute une classe CSS
    titre.textContent = place.title || 'Title not disponible';  // Définit le texte du titre
    section.appendChild(titre);                                 // Ajoute le titre à la section

    const hostSpan = document.createElement('span');                            // Crée un <span> pour le nom de l'hôte
    hostSpan.className = 'host-label';                                          // Ajoute une classe CSS
    const ownerName = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Inconnu'; // Prépare le nom complet ou 'Inconnu'
    hostSpan.textContent = 'Host : ' + ownerName;                               // Définit le texte du <span>
    section.appendChild(hostSpan);                                              // Ajoute le <span> à la section

    const placeContainer = document.createElement('div');   // Crée un conteneur parent
    placeContainer.className = 'place-container';           // Ajoute une classe CSS pour le style flex

    const infoDiv = document.createElement('div');  // Crée une div pour les infos du lieu
    infoDiv.className = 'place-info';               // Ajoute une classe CSS

    const description = document.createElement('p');                    // Crée un paragraphe description
    description.className = 'description';                              // Ajoute une classe CSS
    description.textContent = place.description || 'No description.';   // Définit le texte ou message par défaut
    infoDiv.appendChild(description);                                   // Ajoute la description dans infoDiv

    const price = document.createElement('p');      // Crée un paragraphe prix
    price.className = 'price';                      // Ajoute une classe CSS

    const priceLabel = document.createElement('span');  // Crée un <span> label prix
    priceLabel.className = 'text-price';                // Ajoute une classe CSS
    priceLabel.textContent = 'Price by night : ';       // Définit le texte label

    const priceValue = document.createElement('span');                          // Crée un <span> valeur prix
    priceValue.className = 'price-button';                                      // Ajoute une classe CSS
    priceValue.textContent = place.price ? `${place.price}€` : 'Not specified'; // Définit le texte prix ou alternatif

    price.appendChild(priceLabel);  // Ajoute le label dans le paragraphe prix
    price.appendChild(priceValue);  // Ajoute la valeur dans le paragraphe prix
    infoDiv.appendChild(price);     // Ajoute le paragraphe prix dans infoDiv

    const amenitiesTitle = document.createElement('h3');    // Crée un titre pour les équipements
    amenitiesTitle.textContent = 'Amenities :';             // Définit le texte du titre
    infoDiv.appendChild(amenitiesTitle);                    // Ajoute le titre dans infoDiv

    const amenitiesList = document.createElement('ul');     // Crée une liste à puces
    amenitiesList.id = 'place-amenities';                   // Ajoute un id pour ciblage

    if (place.amenities && place.amenities.length > 0) {    // Vérifie présence équipements
        place.amenities.forEach(a => {                      // Pour chaque équipement
            const li = document.createElement('li');        // Crée un élément de liste
            li.textContent = a.name;                        // Définit le texte de l'équipement
            amenitiesList.appendChild(li);                  // Ajoute l'élément à la liste
        });
    } else {
        const li = document.createElement('li');    // Sinon crée un élément unique
        li.textContent = 'No Amenities listed';     // Message par défaut
        amenitiesList.appendChild(li);              // Ajoute cet élément à la liste
    }
    infoDiv.appendChild(amenitiesList);             // Ajoute la liste des équipements dans infoDiv
    placeContainer.appendChild(infoDiv);            // Ajoute infoDiv dans le conteneur parent

    const image = document.createElement('img');    // Crée un élément image
    const imagePlace = {                            // Dictionnaire des images par titre
        "Minas Tirith": "images/Minas-tirith.jpg",
        "Gouffre de Helm": "images/helm.jpg",
        "Fondcombe": "images/fondcombe.jpg",
        "Mordor": "images/mordor.jpg",
        "Mines of Moria": "images/mine-moria.jpg",
        "The Prancing Pony": "images/pony.jpg"
    };
    image.src = imagePlace[place.title] || 'images/default.jpg';    // Définit la source ou image par défaut
    image.alt = place.title;                                        // Texte alternatif
    image.classList.add('place-image');                             // Ajoute une classe CSS
    placeContainer.appendChild(image);                              // Ajoute l'image dans le conteneur parent
    section.appendChild(placeContainer);                            // Ajoute le conteneur complet dans la section
}

/**
 * On DOM content loaded, retrieves JWT token from cookies and place ID from the URL,
 * then fetches and displays the details of the specified place, if applicable.
 *
 * Only runs the logic if the element with ID 'place-details' exists on the page
 * (when on place.html). Displays a message if no place ID is found.
 *
 * @returns {void}
 */
document.addEventListener('DOMContentLoaded', () => {
    const token = getCookie('token');                                           // Récupère le token JWT stocké dans les cookies
    const placeId = getPlaceIdFromURL();                                        // Récupère l’ID du lieu depuis les paramètres URL
    const placeDetailsElement = document.getElementById('place-details');       // Cherche l’élément #place-details dans le DOM

    if (placeDetailsElement) {                                                  // Ce bloc ne s'exécute que sur place.html
        if (placeId) {
            fetchPlaceDetails(token, placeId);                                  // Si ID présent, on charge les détails
        } else {
            placeDetailsElement.textContent = 'No location specified in URL.';  // Sinon, message d’erreur
        }
    }
});

/*---------------------------------------------------------------------------*/
/*---------------------------------Reviews-----------------------------------*/
/*---------------------------------------------------------------------------*/

let rating = 0; // Note sélectionnée, initialisée à 0

/**
 * Updates the star rating display visually based on the selected rating value.
 * Converts stars up to the selected rating into filled icons ('fas') and resets the rest to empty ('far').
 *
 * Assumes stars have a 'data-value' attribute and are located inside an element with the ID 'star-rating'.
 *
 * @param {number} rating - The selected rating value (usually between 1 and 5).
 * @returns {void}
 */
function updateStars(rating) {                                              // Fonction globale pour mettre à jour l'affichage des étoiles
    const stars = document.querySelectorAll('#star-rating i');              // Sélectionne toutes les étoiles
    stars.forEach(star => {
        const starValue = parseInt(star.getAttribute('data-value'), 10);    // Récupère la valeur de l'étoile
        if (starValue <= rating) {                                          // Si valeur de l'étoile <= note sélectionnée
            star.classList.remove('far');                                   // Enlève la classe étoile vide (far)
            star.classList.add('fas');                                      // Ajoute la classe étoile pleine (fas)
        } else {
            star.classList.remove('fas');                                   // Enlève la classe étoile pleine (fas)
            star.classList.add('far');                                      // Ajoute la classe étoile vide (far)
        }
    });
}


/**
* Initialize the events once the DOM is fully loaded:
* - Handles clicks on stars for ratings.
* - Checks for the presence of the JWT token to display or hide the review form.
* - Loads reviews associated with a location if there is an ID in the URL.
* - Handles review form submission with validation and submission to the API.
*/
document.addEventListener('DOMContentLoaded', () => {                   // Quand le DOM est entièrement chargé
    const stars = document.querySelectorAll('#star-rating i');          // Sélectionne toutes les étoiles dans le container
    stars.forEach(star => { // Pour chaque étoile
        star.addEventListener('click', () => {                          // Ajoute un écouteur sur le clic
            rating = parseInt(star.getAttribute('data-value'), 10);     // Récupère la valeur de l'étoile cliquée (1 à 5)
            updateStars(rating);                                        // Met à jour l'affichage des étoiles en fonction de la note choisie
        });
    });

    const reviewForm = document.getElementById('review-form');  // Récupère le formulaire d'avis
    const token = getCookie('token');                           // Récupère le token JWT dans les cookies
    const placeId = getPlaceIdFromURL();                        // Récupère l'ID du lieu depuis l'URL

    if (!token && reviewForm) {                 // Si pas de token et formulaire présent
        reviewForm.style.display = 'none';      // Cache le formulaire
    }

    if (placeId) {              // Si un ID de lieu est présent dans l'URL
        loadReviews(placeId);   // Charge les avis existants pour ce lieu
    }

    if (reviewForm && token) {                                      // Si formulaire présent et utilisateur connecté
        reviewForm.addEventListener('submit', async (event) => {    // Ecoute la soumission du formulaire
            event.preventDefault();                                 // Empêche le rechargement automatique de la page

            const reviewText = document.getElementById('review-text').value.trim(); // Récupère et nettoie le texte de l'avis

            if (!placeId) {                             // Vérifie si l'ID du lieu est absent
                alert("Error: Missing location ID.");   // Affiche une alerte d'erreur
                return;                                 // Stoppe l'exécution de la fonction
            }
            if (!reviewText) {                          // Vérifie si le texte de l'avis est vide
                alert("Error: Review text is empty.");  // Affiche une alerte d'erreur
                return;
            }
            if (rating === 0) {                         // Vérifie si aucune note n'a été sélectionnée
                alert("Please select a rating.");       // Affiche une alerte pour demander la note
                return;
            }

            console.log({ place_id: placeId, text: reviewText, rating: rating }); // Log des données de review

            const response = await soumettreReview(token, placeId, reviewText, rating); // Envoie la requête d'avis à l'API
            gestionResponse(response);                                                  // Traite la réponse de l'API
        });
    }
});


/**
* @file review_redirect.js
* @description
* Manages the behavior of the "Add review" title based on the user's login status.
* If the user is not logged in, they are redirected to the login page when they click on this title.
* The `next` parameter in the URL allows you to automatically return to the venue page after logging in.
*
* Features:
* - Detects when the DOM is fully loaded (`DOMContentLoaded`)
* - Checks for the presence of a JWT token in cookies
* - Adds clickable behavior to the review add title if the user is not logged in
* - Dynamic redirection to the login page with a planned return to the venue or home page
*
* Dependencies:
* - `getCookie(name)` function to retrieve the JWT token
* - `getPlaceIdFromURL()` function to extract the venue ID from the URL
*/
document.addEventListener('DOMContentLoaded', () => {                           // Quand le DOM est entièrement chargé
    const addReviewTitle = document.getElementById('add-review-title');         // Récupère le titre "Add review"
    const token = getCookie('token');                                           // Récupère le token JWT

    if (addReviewTitle && !token) {                                             // Si le titre existe et pas de token (utilisateur non connecté)
        addReviewTitle.style.cursor = 'pointer';                                // Change le curseur pour indiquer un clic possible
        addReviewTitle.addEventListener('click', () => {                        // Ajoute un écouteur de clic sur le titre
            const placeId = getPlaceIdFromURL();                                // Récupère l'ID du lieu dans l'URL
            const nextPage = placeId ? `/place.html?place_id=${placeId}` : '/index.html';   // Définit la page de retour après login
            window.location.href = `/login.html?next=${encodeURIComponent(nextPage)}`;      // Redirige vers login avec la page suivante encodée
        });
    }
});

/**
 * Sends a review to the API for a specific place.
 *
 * @async
 * @function soumettreReview
 * @param {string} token - JWT token for user authentication.
 * @param {string} placeId - ID of the place being reviewed.
 * @param {string} reviewText - Text content of the review.
 * @param {number} rating - Rating given to the place.
 * @returns {Promise<Response|undefined>} Returns the fetch Response object if successful, otherwise undefined.
 *
 * @throws Will alert the user and log an error if the user is unauthenticated or if the API responds with an error.
 * @throws Will alert the user if a network or other unexpected error occurs during the request.
 */
async function soumettreReview(token, placeId, reviewText, rating) {
    try {
        const userId = getUserIdFromToken(token);                   // Extraction de l'ID utilisateur depuis le token
        if (!userId) {                                              // Vérifie si l'ID utilisateur est absent ou invalide
            alert("Error: Unauthenticated user. Please log in.");   // Alerte utilisateur en cas de problème
            return;                                                 // Interrompt l'exécution si pas d'utilisateur authentifié
        }

        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',                             // Méthode POST
            headers: {
                'Content-Type': 'application/json',     // Envoi JSON
                'Authorization': `Bearer ${token}`      // Token JWT
            },
            body: JSON.stringify({
                place_id: placeId,  // ID du lieu
                text: reviewText,   // Texte de l'avis
                rating: rating,     // Note de l'avis
                user_id: userId     // ID utilisateur
            })
        });

        if (!response.ok) {                             // Si réponse négative
            const errorData = await response.json();    // Récupérer erreur JSON
            alert('Error: Please check that you have not already posted a review or that this house is yours.'
                    + (errorData.message || '400 Bad Request'));    // Message générique
            console.error('Erreur API:', errorData);                // Log erreur dans console
            return;
        }
        return response;                                            // Retourne réponse serveur
    } catch (error) {
        console.error('Error sending reviews :', error);            // Log erreur réseau
        alert('You cannot rate your own home. Please try again..'); // Message d'alerte réseau
    }
}

/**
* Handles the response received after submitting a review.
*
* @param {Response|undefined} response - Response object from the fetch request or undefined.
*
* If the response is valid and positive, displays a success message, resets the form,
* resets the rating to zero, updates the star rating, and then reloads the page.
* Otherwise, displays an error message.
*/
function gestionResponse(response) {                    // Fonction pour gérer la réponse de l'API
    if (!response) return;                              // Si pas de réponse, ne fait rien

    if (response.ok) {                                  // Si la réponse HTTP est OK (status 2xx)
        alert('Review submitted successfully!');        // Affiche message de succès
        document.getElementById('review-form').reset(); // Réinitialise le formulaire d'avis
        rating = 0;                                     // Réinitialise la note sélectionnée
        updateStars(0);                                 // Réinitialise l'affichage des étoiles (vides)
        location.reload();                              // Recharge la page pour afficher les avis mis à jour
    } else {
        alert('Failed to submit review');               // Alerte en cas d'échec (status non 2xx)
    }
}

/**
* Loads and displays reviews associated with a given place.
*
* Sends a GET request to the API to retrieve reviews for the place identified by placeId,
* then dynamically creates the HTML elements to display each review on the page.
*
* @param {string} placeId - The unique identifier of the place whose reviews are to be displayed.
*
* If an error occurs while retrieving or processing reviews,
* displays an error message in the console.
*/
function loadReviews(placeId) {                                         // Fonction qui charge et affiche les avis pour un lieu donné
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`)     // Envoie une requête GET à l'API pour récupérer les avis du lieu
        .then(response => response.json())                              // Convertit la réponse HTTP en objet JSON
        .then(data => {                                                 // Quand les données JSON sont reçues
            const reviewContainer = document.getElementById('reviews'); // Récupère l'élément HTML où afficher les avis
            reviewContainer.innerHTML = '';                             // Vide ce conteneur pour réinitialiser l'affichage

            data.forEach(review => {                                    // Pour chaque avis dans les données reçues
                const div = document.createElement('div');              // Crée un nouvel élément <div>
                div.classList.add('review');                            // Ajoute la classe CSS 'review' à ce div pour le style
                const userName = review.user_name || 'Unknown user';    // Récupère le nom utilisateur ou met un texte par défaut
                div.innerHTML = `
                    <p><strong>${userName}</strong> a écrit :</p>
                    <p>${review.text}</p>
                    <p>Note : ${displayStars(review.rating)}</p>
                `;
                reviewContainer.appendChild(div);                       // Ajoute ce div dans le conteneur des avis sur la page
            });
        })
        .catch(error => {                                               // Si une erreur survient lors de la requête ou du traitement
            console.error('Error loading reviews :', error);            // Affiche l'erreur dans la console du navigateur
        });
}

/**
* Generates the HTML code to display a rating as gold stars.
*
* @param {number} rating - The numeric rating between 0 and 5.
* @returns {string} An HTML string containing 5 solid or empty star icons.
*/
function displayStars(rating) {                                     // Fonction qui génère le HTML des étoiles dorées selon la note reçue
    let starsHTML = '';                                             // Initialise une chaîne vide pour contenir les étoiles
    for (let i = 1; i <= 5; i++) {                                  // Pour 5 étoiles au total
        starsHTML += i <= rating                                    // Si l'indice est inférieur ou égal à la note
            ? '<i class="fas fa-star" style="color: gold;"></i>'    // Ajoute une étoile pleine dorée
            : '<i class="far fa-star" style="color: gold;"></i>';   // Sinon une étoile vide dorée
    }
    return starsHTML; // Retourne le HTML complet des étoiles pour affichage
}
