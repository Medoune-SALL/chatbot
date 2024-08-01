import nltk
import streamlit as st
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Télécharger les ressources NLTK une fois
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Charger le fichier texte et prétraiter les données
with open('DataScience.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Tokeniser le texte en phrases
sentences = sent_tokenize(data)


# Définir une fonction pour prétraiter chaque phrase
def preprocess(sentence):
    # Tokeniser la phrase en mots
    words = word_tokenize(sentence)
    # Retirer les stopwords et la ponctuation
    words = [word.lower() for word in words if
             word.lower() not in stopwords.words('english') and word not in string.punctuation]
    # Lemmatizer les mots
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words


# Prétraiter chaque phrase dans le texte
corpus = [preprocess(sentence) for sentence in sentences]


# Définir une fonction pour trouver la phrase la plus pertinente en fonction d'une requête
def get_most_relevant_sentence(query):
    # Prétraiter la requête
    query = preprocess(query)
    # Calculer la similarité entre la requête et chaque phrase dans le texte
    max_similarity = 0
    most_relevant_sentence = ""
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence


# Fonction du chatbot
def chatbot(question):
    try:
        # Trouver la phrase la plus pertinente
        most_relevant_sentence = get_most_relevant_sentence(question)
        if not most_relevant_sentence:
            return "Je suis désolé, je n'ai pas trouvé de réponse pertinente."
        # Retourner la réponse
        return most_relevant_sentence
    except Exception as e:
        return f"Une erreur est survenue: {e}"


# Créer une application Streamlit
def main():
    st.title("My First Chatbot")
    st.write("Bonjour ! Que voulez vous savoir sur la data science.")

    # Obtenir la question de l'utilisateur
    question = st.text_input("Vous:")

    # Créer un bouton pour soumettre la question
    if st.button("Envoyer"):
        # Appeler la fonction du chatbot avec la question et afficher la réponse
        response = chatbot(question)
        st.write("Chatbot: " + response)


if __name__ == "__main__":
    main()
