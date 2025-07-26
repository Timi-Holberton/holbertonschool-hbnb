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


const chaineRequete = window.location.search; // Récupère la chaîne de requête de l'URL (?place_id=xxx)
const parametres = new URLSearchParams(chaineRequete); // Crée un objet pour manipuler les paramètres d'URL
const placeId = parametres.get('place_id'); // Extrait la valeur du paramètre place_id

console.log("ID du lieu extrait de l'URL :", placeId); // Affiche l'ID récupéré pour vérification

fetch(`http://localhost:5000/api/v1/places/${placeId}`) // Envoie une requête GET à l'API pour récupérer les données du lieu
  .then(response => {
    if (!response.ok) throw new Error('Lieu non trouvé'); // Si la réponse est en erreur (404...), on déclenche une exception
    return response.json(); // Sinon, on convertit la réponse en JSON
  })
  .then(data => {
    const section = document.getElementById('place-details'); // Sélectionne la section vide dans le HTML
    section.innerHTML = ''; // Vide son contenu avant d'ajouter de nouveaux éléments

    const titre = document.createElement('h2'); // Crée un élément <h2>
    titre.className = 'titre-details-place'; // Attribue une classe CSS
    titre.textContent = data.title || 'Titre non disponible'; // Met le titre du lieu ou un fallback si absent
    section.appendChild(titre); // Ajoute le <h2> à la section

    const hostSpan = document.createElement('span'); // Crée un <span> pour l’hôte
    hostSpan.className = 'host-label'; // Classe CSS pour le style
    const ownerName = data.owner ? `${data.owner.first_name} ${data.owner.last_name}` : 'Inconnu'; // Construit le nom de l’hôte
    hostSpan.textContent = 'Host : ' + ownerName; // Définit le texte du <span>
    section.appendChild(hostSpan); // Ajoute le <span> à la section

    const infoDiv = document.createElement('div'); // Crée un conteneur <div> pour les infos générales
    infoDiv.className = 'place-info'; // Classe CSS pour styliser

    const description = document.createElement('p'); // Crée un paragraphe pour la description
    description.className = 'description'; // Classe CSS
    description.textContent = data.description || 'Pas de description.'; // Ajoute le texte de la description
    infoDiv.appendChild(description); // Ajoute le paragraphe à la div

    const price = document.createElement('p'); // Crée un paragraphe pour le prix
    price.className = 'price'; // Classe CSS

    const priceLabel = document.createElement('span'); // Crée une étiquette pour le prix
    priceLabel.className = 'text-price'; // Classe CSS
    priceLabel.textContent = 'Price by night : '; // Texte statique
    const priceValue = document.createElement('span'); // Crée une balise pour afficher la valeur
    priceValue.className = 'price-button'; // Classe CSS
    priceValue.textContent = data.price ? `${data.price}€` : 'Non précisé'; // Valeur dynamique du prix

    price.appendChild(priceLabel); // Ajoute l’étiquette au paragraphe
    price.appendChild(priceValue); // Ajoute le prix au paragraphe
    infoDiv.appendChild(price); // Ajoute tout le bloc prix à la div

    const amenitiesTitle = document.createElement('h3'); // Crée un titre pour les équipements
    amenitiesTitle.textContent = 'Amenities :'; // Texte du titre
    infoDiv.appendChild(amenitiesTitle); // Ajoute le titre à la div

    const amenitiesList = document.createElement('ul'); // Crée une liste non ordonnée
    amenitiesList.id = 'place-amenities'; // ID pour le ciblage ou le style

    if (data.amenities && data.amenities.length > 0) { // Vérifie s’il y a des équipements
      data.amenities.forEach(a => { // Pour chaque équipement
        const li = document.createElement('li'); // Crée un élément de liste
        li.textContent = a.name; // Met le nom de l’équipement
        amenitiesList.appendChild(li); // Ajoute à la liste
      });
    } else {
      const li = document.createElement('li'); // Cas où il n’y a aucun équipement
      li.textContent = 'Aucun équipement listé'; // Texte par défaut
      amenitiesList.appendChild(li); // Ajoute l’élément par défaut
    }

    infoDiv.appendChild(amenitiesList); // Ajoute la liste des équipements à la div

    section.appendChild(infoDiv); // Ajoute la div entière à la section principale
  })
  .catch(error => {
    console.error(error); // Affiche l'erreur dans la console
    const section = document.getElementById('place-details'); // Sélectionne la section
    section.textContent = 'Erreur lors du chargement du lieu.'; // Affiche un message d’erreur à l’utilisateur
  });



