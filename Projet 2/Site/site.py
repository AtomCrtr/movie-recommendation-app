import streamlit as st
import requests
import pandas as pd
from difflib import get_close_matches
import requests
import hashlib

# Configuration TMDB
TMDB_API_KEY = "83c9694912ff3b1a801344c27edcb158"

# Configuration globale de Streamlit
st.set_page_config(
    page_title="CinéMatch23",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS pour l'esthétique globale et animations du carrousel
st.markdown(
    """
    <style>
    body { font-family: 'Arial', sans-serif; background-color: #f5f5f5; }
    h1 { color: #FF5733; text-align: center; white-space: nowrap; }
    [data-testid="stSidebar"] { background-color: #FFD700; border-radius: 10px; padding: 20px; }
    [data-testid="stSidebar"] h1 { color: black !important; }
    .poster { text-align: center; margin: 20px auto; }
    .poster img {
        border-radius: 15px;
        max-width: 400px;
        max-height: 500px;
        transition: transform 0.3s ease, opacity 0.3s ease;
    }
    .poster img:hover { transform: scale(1.1); opacity: 0.85; }
    .stButton > button {
        background-color: #FF5733;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover { background-color: #C70039; }
    .carousel {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }
    .carousel .poster {
        flex: 1 1 200px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    df = pd.read_parquet("..\Site\df_complet_060125.parquet")
    return df


df_complet_060125 = load_data()


# GESTION DES UTILISATEURS
# Fonction pour hacher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Gestion des utilisateurs
def manage_user_profiles():
    # Initialiser l'état des utilisateurs s'il n'existe pas
    if "users" not in st.session_state:
        st.session_state["users"] = {}  # Dictionnaire des utilisateurs
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None  # Aucun utilisateur connecté

    with st.sidebar:
        st.title("Connexion / Inscription")
        menu = st.radio("Choisissez une option", ["Connexion", "Inscription"])

        if menu == "Inscription":
            username = st.text_input("Nom d'utilisateur", key="signup_username")
            password = st.text_input(
                "Mot de passe", type="password", key="signup_password"
            )
            if st.button("Créer un compte"):
                if username in st.session_state["users"]:
                    st.warning("Ce nom d'utilisateur existe déjà.")
                else:
                    st.session_state["users"][username] = {
                        "password": hash_password(password),
                        "favorites": [],
                        "watchlist": [],
                        "search_history": [],
                    }
                    st.success("Compte créé avec succès ! Connectez-vous maintenant.")

        elif menu == "Connexion":
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input(
                "Mot de passe", type="password", key="login_password"
            )
            if st.button("Se connecter"):
                if username in st.session_state["users"]:
                    stored_password = st.session_state["users"][username]["password"]
                    if stored_password == hash_password(password):
                        st.session_state["current_user"] = username
                        st.success(f"Bienvenue, {username} !")
                    else:
                        st.error("Nom d'utilisateur ou mot de passe incorrect.")
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")

        # Déconnexion
        if st.session_state["current_user"]:
            st.sidebar.write(
                f"Connecté en tant que : {st.session_state['current_user']}"
            )
            if st.button("Se déconnecter"):
                st.session_state["current_user"] = None
                st.success("Déconnecté avec succès.")


def get_current_user():
    if "current_user" in st.session_state:
        username = st.session_state["current_user"]
        if username and username in st.session_state["users"]:
            return username
    return None


# Fonction Bande-Annonce
def fetch_movie_details(tconst):
    """Récupère les détails d'un film via tconst (IMDb ID)."""
    url = f"https://api.themoviedb.org/3/find/{tconst}?api_key={TMDB_API_KEY}&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("movie_results", [])
        if results:
            return results[0]
    return None


# Fonction pour obtenir les recommandations en fonction des préférences utilisateur #QUIZZZ
def get_recommendations_by_quiz(genre, start_year, end_year, duration, popularity):
    try:
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": genre,
            "primary_release_date.gte": f"{start_year}-01-01",
            "primary_release_date.lte": f"{end_year}-12-31",
            "with_runtime.lte": duration,
            "language": "fr",
        }
        # Requête API
        response = requests.get(url, params=params).json()

        results = response.get("results", [])
        filtered_results = [
            movie
            for movie in response.get("results", [])
            if movie.get("vote_average", 0) >= popularity
        ]

        return filtered_results
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des recommandations : {e}")
        return []


# Gestion des utilisateurs
manage_user_profiles()

# Vérifiez l'utilisateur connecté
current_username = get_current_user()

# Afficher le message d'accueil
if current_username:
    st.title(f"🎊 Bonjour, {current_username} !")
else:
    st.title(f"Bienvenue chez CinéMatch🎬")
    st.title(f"Le site des creusois cinéphiles🌸")
    st.image(
        "https://png.pngtree.com/background/20231101/original/pngtree-elderly-couple-enjoying-a-3d-movie-with-popcorn-while-lounging-on-picture-image_5840016.jpg"
    )
    st.warning("Veuillez vous connecter pour accéder à toutes les fonctionnalités.")


# Barre de navigation dans le sidebar
st.sidebar.title("À propos de CinéMatch")
st.sidebar.info(
    """
**CinéMatch** utilise des algorithmes de machine learning pour offrir des recommandations 
personnalisées basées sur les données IMDb et TMDB. Découvrez des films qui correspondent à vos goûts !
"""
)

# Menu de navigation
selected_page = st.sidebar.selectbox(
    "Naviguer",
    ["Accueil", "À l'affiche dans la Creuse", "Quizz de Recommandation"],
)

# PAGE ACCUEIL
if current_username and selected_page == "Accueil":
    st.markdown(
        "<h1>🎥 La magie du cinéma, version Creuse !</h1>", unsafe_allow_html=True
    )
    st.markdown(
        """
        Bienvenue sur **CinéMatch**, votre guide personnalisé pour découvrir des films qui vous ressemblent !
        En tant qu'habitant de la Creuse, plongez dans une sélection de films soigneusement adaptés à vos goûts et à votre région.
        """
    )
    input_title = st.text_input("Entrez le nom d'un film :").strip().lower()

    if input_title:
        all_titles = df_complet_060125["titre_fr"].str.lower().values
        if input_title in all_titles:
            input_index = df_complet_060125[
                df_complet_060125["titre_fr"].str.lower() == input_title
            ].index[0]
            tconst = df_complet_060125.loc[input_index]["tconst"]

            # Affichage des détails du film
            st.header(df_complet_060125.loc[input_index]["titre_fr"])
            start_year = df_complet_060125.loc[input_index]["startYear"]
            st.write(f"**Année de sortie du Film :** {start_year}")

            poster_path = df_complet_060125.loc[
                df_complet_060125["tconst"] == tconst, "poster_path"
            ].values[0]
            afficheorigine = (
                f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_path}"
            )
            st.markdown(
                f"<div class='poster'><img src='{afficheorigine}' alt='Affiche'></div>",
                unsafe_allow_html=True,
            )

            # Résumé
            url = f"https://api.themoviedb.org/3/find/{tconst}?api_key={TMDB_API_KEY}&external_source=imdb_id&language=fr"
            response = requests.get(url)
            rep = response.json()
            resume = rep["movie_results"][0]["overview"]
            st.write(f"**Résumé** : {resume}")

            # Bande-annonce
            movie_details = fetch_movie_details(tconst)
            if movie_details:
                movie_id = movie_details["id"]
                video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=fr"
                response = requests.get(video_url)
                videos = response.json().get("results", [])
                if videos:
                    trailer = next(
                        (video for video in videos if video["type"] == "Trailer"), None
                    )
                    if trailer:
                        st.video(f"https://www.youtube.com/watch?v={trailer['key']}")

            # Recommandations
            st.header("🎠 Nos 5 recommandations :")
            st.markdown("<div class='carousel'>", unsafe_allow_html=True)

            for tconst in df_complet_060125.loc[input_index]["tconst_neighbors"]:
                movie_row = df_complet_060125[df_complet_060125["tconst"] == tconst]
                titre = movie_row["titre_fr"].values[0]
                start_year = movie_row["startYear"].values[0]
                poster_path = movie_row["poster_path"].values[0]

                # URL de l'affiche
                affiche = (
                    f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_path}"
                )

                # Affichage structuré des détails
                st.markdown(
                    f"""
                    <div style='display: flex; align-items: center; background-color: #f0f0f0; border-radius: 10px; padding: 15px; margin-bottom: 20px;'>
                        <div style='flex: 1; text-align: center;'>
                            <img src="{affiche}" alt="Affiche" style='border-radius: 10px; max-width: 200px; height: auto;'>
                        </div>
                        <div style='flex: 2; padding-left: 20px;'>
                            <h2 style='color: #FF5733; margin-bottom: 10px;'>{titre} ({start_year})</h2>
                            <p style='margin: 5px 0;'><b>Résumé :</b> {resume}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Notes et avis
            st.markdown("📣 **Donnez votre avis**")
            rating = st.slider("Note (0-10)", 0, 10, 5)
            review = st.text_area("Votre avis")
            if st.button("Soumettre votre avis"):
                if input_title not in st.session_state:
                    st.session_state[input_title] = []
                st.session_state[input_title].append(
                    {"rating": rating, "review": review}
                )
                st.success("Merci pour votre avis !")

            # Afficher les avis
            if input_title in st.session_state:
                st.markdown("### 📋 Avis des utilisateurs")
                for rev in st.session_state[input_title]:
                    st.write(f"**Note :** {rev['rating']}/10")
                    st.write(f"**Avis :** {rev['review']}")
                    st.markdown("---")

            # Favoris et liste d'envies
            # Vérifiez si un utilisateur est connecté
            if current_username:
                current_user_data = st.session_state["users"].get(current_username, {})

                st.subheader("🎆 **Actions**")
                if st.button("🌟 Ajouter aux Favoris"):
                    if "favorites" not in current_user_data:
                        current_user_data["favorites"] = []
                    if (
                        df_complet_060125.loc[input_index]["titre_fr"]
                        not in current_user_data["favorites"]
                    ):
                        current_user_data["favorites"].append(
                            df_complet_060125.loc[input_index]["titre_fr"]
                        )
                        st.success(
                            f"'{df_complet_060125.loc[input_index]['titre_fr']}' ajouté à vos Favoris !"
                        )
                    else:
                        st.warning("Ce film est déjà dans vos Favoris.")

                if st.button("🌈 Ajouter à la Liste d'envies"):
                    if "watchlist" not in current_user_data:
                        current_user_data["watchlist"] = []
                    if (
                        df_complet_060125.loc[input_index]["titre_fr"]
                        not in current_user_data["watchlist"]
                    ):
                        current_user_data["watchlist"].append(
                            df_complet_060125.loc[input_index]["titre_fr"]
                        )
                        st.success(
                            f"'{df_complet_060125.loc[input_index]['titre_fr']}' ajouté à votre Liste d'envies !"
                        )
                    else:
                        st.warning("Ce film est déjà dans votre Liste d'envies.")
            else:
                st.warning(
                    "Veuillez vous connecter pour ajouter ce film à vos Favoris ou à votre Liste d'envies."
                )
        else:
            close_matches = get_close_matches(input_title, all_titles, n=5, cutoff=0.5)
            if close_matches:
                st.warning(
                    f"Le film ' {input_title}' n'existe pas dans la base de données. Peut-être vouliez-vous dire :"
                )
                for match in close_matches:
                    st.write(f"- {match}")
            else:
                st.error(
                    f"Le film '{input_title}' n'existe pas dans la base de données, et aucune suggestion n'est disponible."
                )


# PAGE AFFICHAGE DES FILMS À L'AFFICHE DANS LA CREUSE
if current_username and selected_page == "À l'affiche dans la Creuse":
    st.title("🎫 Films à l'affiche en Creuse")

    def get_movies_in_theaters():
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=fr&page=1&region=FR"
        try:
            response = requests.get(url).json()
            return response.get("results", [])
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la récupération des films à l'affiche : {e}")
            return []

    movies = get_movies_in_theaters()

    if movies:
        for movie in movies:
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; background-color: #f0f0f0; border-radius: 10px; padding: 15px; margin-bottom: 20px;'>
                    <div style='flex: 1; text-align: center;'>
                        <img src="https://image.tmdb.org/t/p/w300{movie['poster_path']}" style='border-radius: 10px; max-width: 200px; height: auto;'>
                    </div>
                    <div style='flex: 2; padding-left: 20px;'>
                        <h2 style='color: #FF5733; margin-bottom: 10px;'>{movie['title']} ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})</h2>
                        <p style='margin: 5px 0;'><b>Note :</b> {movie['vote_average']} / 10</p>
                        <p style='margin: 5px 0;'><b>Résumé :</b> {movie['overview']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("Aucun film à l'affiche pour le moment.")

    # Ajout d'un bouton pour consulter les horaires dans les cinémas locaux
    st.markdown(
        """
        <div style='text-align: center; margin-top: 20px;'>
            <a href='https://www.allocine.fr/salle/cinema/departement-83144/' target='_blank' style='text-decoration: none;'>
                <button style='background-color: #FF5733; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px;'>
                    Consulter les horaires dans les cinémas de la Creuse
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# PAGE QUIZZ DE RECOMMANDATION
if current_username and selected_page == "Quizz de Recommandation":
    st.title("🎯 Quizz de Recommandation")

    # Questions du quizz
    genre = st.selectbox(
        "Quel genre de film préférez-vous ?",
        ["Action", "Comédie", "Drame", "Horreur", "Science-Fiction"],
    )
    start_year, end_year = st.slider(
        "Choisissez une plage d'années pour les films (Année de sortie) :",
        1950,
        2023,
        (1990, 2020),
    )
    duration = st.radio("Quelle durée de film cherchez-vous ?", [90, 120, 180], index=1)
    popularity = st.slider(
        "Quel niveau de popularité recherchez-vous ? (Note moyenne minimum)", 0, 10, 7
    )

    # Lancer la recherche
    if st.button("Trouver des films"):
        genre_map = {
            "Action": 28,
            "Comédie": 35,
            "Drame": 18,
            "Horreur": 27,
            "Science-Fiction": 878,
        }
        genre_id = genre_map.get(genre, None)
        if genre_id:
            results = get_recommendations_by_quiz(
                genre_id, start_year, end_year, duration, popularity
            )

            # Vérification et affichage des résultats
            if results:
                st.write(
                    f"🔍 {len(results)} films trouvés correspondant à vos critères :"
                )
                for movie in results[:10]:  # Limite à 10 films
                    st.markdown(
                        f"- **{movie['title']}** ({movie['release_date'][:4]}) - Note : {movie['vote_average']}/10"
                    )
            else:
                st.write("Aucun film trouvé correspondant à vos critères.")

# Footer
st.markdown(
    """
<div class="footer">
    🖋️ Projet développé par l'équipe "Les Gadjos" <br>
</div>
""",
    unsafe_allow_html=True,
)
