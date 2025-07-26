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
    const response = await fetch('http://localhost:5000/api/v1/auth/login', { // Envoi de la requête POST à l'API d'authentification
        method: 'POST', // Méthode HTTP POST
        headers: {
            'Content-Type': 'application/json' // Spécifie que le corps de la requête est au format JSON
        },
        body: JSON.stringify({ email, password }) // Corps de la requête contenant l'email et le mot de passe au format JSON
    });

    if (response.ok) { // Si la réponse est positive (code HTTP 2xx)
        const data = await response.json(); // Extraction du JSON de la réponse
        document.cookie = `token=${data.access_token}; path=/`; // Stockage du token JWT dans un cookie accessible sur tout le site

        const params = new URLSearchParams(window.location.search); // Récupération des paramètres de l'URL actuelle
        const next = params.get('next') || '/index.html';  // Récupération de la valeur du paramètre 'next', ou page d'accueil par défaut

        window.location.href = next; // Redirection vers la page demandée dans 'next'
    } else {
        alert('Login failed: ' + response.statusText); // Affichage d'une alerte en cas d'échec de connexion
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

function getUserIdFromToken(token) { // récupère l'id dans le token
    try {
        const base64Url = token.split('.')[1]; // Partie payload encodée en base64url
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Conversion base64url -> base64 standard
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
            '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2) // Décodage URL-encoding caractère par caractère
        ).join('')); // Reconstruction de la chaîne JSON
        const payload = JSON.parse(jsonPayload); // Conversion JSON en objet JS
        return payload.user_id || payload.sub; // Retourne user_id ou sub selon champ présent dans token
    } catch (e) {
        console.error("Erreur décodage token:", e); // Affiche erreur en cas de problème
        return null; // Retourne null si échec du décodage
    }
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
let rating = 0; // Note sélectionnée, initialisée à 0

function updateStars(rating) { // Fonction globale pour mettre à jour l'affichage des étoiles
    const stars = document.querySelectorAll('#star-rating i'); // Sélectionne toutes les étoiles
    stars.forEach(star => {
        const starValue = parseInt(star.getAttribute('data-value'), 10); // Récupère la valeur de l'étoile
        if (starValue <= rating) { // Si valeur de l'étoile <= note sélectionnée
            star.classList.remove('far'); // Enlève la classe étoile vide (far)
            star.classList.add('fas'); // Ajoute la classe étoile pleine (fas)
        } else {
            star.classList.remove('fas'); // Enlève la classe étoile pleine (fas)
            star.classList.add('far'); // Ajoute la classe étoile vide (far)
        }
    });
}

document.addEventListener('DOMContentLoaded', () => { // Quand le DOM est entièrement chargé
    const stars = document.querySelectorAll('#star-rating i'); // Sélectionne toutes les étoiles dans le container
    stars.forEach(star => { // Pour chaque étoile
        star.addEventListener('click', () => { // Ajoute un écouteur sur le clic
            rating = parseInt(star.getAttribute('data-value'), 10); // Récupère la valeur de l'étoile cliquée (1 à 5)
            updateStars(rating); // Met à jour l'affichage des étoiles en fonction de la note choisie
        });
    });

    const reviewForm = document.getElementById('review-form'); // Récupère le formulaire d'avis
    const token = getCookie('token'); // Récupère le token JWT dans les cookies
    const placeId = getPlaceIdFromURL(); // Récupère l'ID du lieu depuis l'URL

    if (!token && reviewForm) { // Si pas de token et formulaire présent
        reviewForm.style.display = 'none'; // Cache le formulaire
    }

    if (placeId) { // Si un ID de lieu est présent dans l'URL
        loadReviews(placeId); // Charge les avis existants pour ce lieu
    }

    if (reviewForm && token) { // Si formulaire présent et utilisateur connecté
        reviewForm.addEventListener('submit', async (event) => { // Ecoute la soumission du formulaire
            event.preventDefault(); // Empêche le rechargement automatique de la page

            const reviewText = document.getElementById('review-text').value.trim(); // Récupère et nettoie le texte de l'avis

            if (!placeId) { // Vérifie si l'ID du lieu est absent
                alert("Erreur : Identifiant du lieu manquant."); // Affiche une alerte d'erreur
                return; // Stoppe l'exécution de la fonction
            }
            if (!reviewText) { // Vérifie si le texte de l'avis est vide
                alert("Erreur : Le texte de la review est vide."); // Affiche une alerte d'erreur
                return; // Stoppe l'exécution de la fonction
            }
            if (rating === 0) { // Vérifie si aucune note n'a été sélectionnée
                alert("Merci de sélectionner une note."); // Affiche une alerte pour demander la note
                return; // Stoppe l'exécution de la fonction
            }

            console.log({ place_id: placeId, text: reviewText, rating: rating }); // Log des données de review

            const response = await soumettreReview(token, placeId, reviewText, rating); // Envoie la requête d'avis à l'API
            gestionResponse(response); // Traite la réponse de l'API
        });
    }
});

document.addEventListener('DOMContentLoaded', () => { // Quand le DOM est entièrement chargé
    const addReviewTitle = document.getElementById('add-review-title'); // Récupère le titre "Add review"
    const token = getCookie('token'); // Récupère le token JWT

    if (addReviewTitle && !token) { // Si le titre existe et pas de token (utilisateur non connecté)
        addReviewTitle.style.cursor = 'pointer'; // Change le curseur pour indiquer un clic possible
        addReviewTitle.addEventListener('click', () => { // Ajoute un écouteur de clic sur le titre
            const placeId = getPlaceIdFromURL(); // Récupère l'ID du lieu dans l'URL
            const nextPage = placeId ? `/place.html?place_id=${placeId}` : '/index.html'; // Définit la page de retour après login
            window.location.href = `/login.html?next=${encodeURIComponent(nextPage)}`; // Redirige vers login avec la page suivante encodée
        });
    }
});

async function soumettreReview(token, placeId, reviewText, rating) {
    try {
        const userId = getUserIdFromToken(token); // Extraction de l'ID utilisateur depuis le token
        if (!userId) { // Vérifie si l'ID utilisateur est absent ou invalide
            alert("Erreur : utilisateur non authentifié. Veuillez vous reconnecter."); // Alerte utilisateur en cas de problème
            return; // Interrompt l'exécution si pas d'utilisateur authentifié
        }

        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST', // Méthode POST
            headers: {
                'Content-Type': 'application/json', // Envoi JSON
                'Authorization': `Bearer ${token}` // Token JWT
            },
            body: JSON.stringify({
                place_id: placeId, // ID du lieu
                text: reviewText, // Texte de l'avis
                rating: rating, // Note de l'avis
                user_id: userId // ID utilisateur
            })
        });

        if (!response.ok) { // Si réponse négative
            const errorData = await response.json(); // Récupérer erreur JSON

            if (errorData.error === 'You cannot evaluate your own location.') {
                alert('Vous ne pouvez pas noter votre propre maison'); // Message personnalisé
            } else {
                alert('Erreur lors de la soumission : ' + (errorData.message || '400 Bad Request')); // Message générique
            }

            console.error('Erreur API:', errorData); // Log erreur dans console
        }

        return response; // Retourne réponse serveur
    } catch (error) {
        console.error('Erreur lors de l\'envoi de l\'avis :', error); // Log erreur réseau
        alert('Erreur réseau. Veuillez réessayer.'); // Message d'alerte réseau
    }
}

function gestionResponse(response) { // Fonction pour gérer la réponse de l'API
    if (!response) return; // Si pas de réponse, ne fait rien

    if (response.ok) { // Si la réponse HTTP est OK (status 2xx)
        alert('Review submitted successfully!'); // Affiche message de succès
        document.getElementById('review-form').reset(); // Réinitialise le formulaire d'avis
        rating = 0; // Réinitialise la note sélectionnée
        updateStars(0); // Réinitialise l'affichage des étoiles (vides)
        location.reload(); // Recharge la page pour afficher les avis mis à jour
    } else {
        alert('Failed to submit review'); // Alerte en cas d'échec (status non 2xx)
    }
}

function loadReviews(placeId) { // Fonction qui charge et affiche les avis pour un lieu donné
    fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`) // Envoie une requête GET à l'API pour récupérer les avis du lieu
        .then(response => response.json()) // Convertit la réponse HTTP en objet JSON
        .then(data => { // Quand les données JSON sont reçues
            const reviewContainer = document.getElementById('reviews'); // Récupère l'élément HTML où afficher les avis
            reviewContainer.innerHTML = ''; // Vide ce conteneur pour réinitialiser l'affichage

            data.forEach(review => { // Pour chaque avis dans les données reçues
                const div = document.createElement('div'); // Crée un nouvel élément <div>
                div.classList.add('review'); // Ajoute la classe CSS 'review' à ce div pour le style

                const userName = review.user_name || 'Utilisateur inconnu'; // Récupère le nom utilisateur ou met un texte par défaut

                div.innerHTML = `
                    <p><strong>${userName}</strong> a écrit :</p>
                    <p>${review.text}</p>
                    <p>Note : ${displayStars(review.rating)}</p>
                `;

                reviewContainer.appendChild(div); // Ajoute ce div dans le conteneur des avis sur la page
            });
        })
        .catch(error => { // Si une erreur survient lors de la requête ou du traitement
            console.error('Erreur lors du chargement des avis :', error); // Affiche l'erreur dans la console du navigateur
        });
}

function displayStars(rating) { // Fonction qui génère le HTML des étoiles dorées selon la note reçue
    let starsHTML = ''; // Initialise une chaîne vide pour contenir les étoiles

    for (let i = 1; i <= 5; i++) { // Pour 5 étoiles au total
        starsHTML += i <= rating  // Si l'indice est inférieur ou égal à la note
            ? '<i class="fas fa-star" style="color: gold;"></i>'  // Ajoute une étoile pleine dorée
            : '<i class="far fa-star" style="color: gold;"></i>'; // Sinon une étoile vide dorée
    }

    return starsHTML; // Retourne le HTML complet des étoiles pour affichage
}
