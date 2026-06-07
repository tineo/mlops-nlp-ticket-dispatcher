import re
import nltk
from nltk.corpus import stopwords

# Asegurar que se descarguen las stopwords si es necesario
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Para la PoC usaremos stopwords en español
stop_words = set(stopwords.words('spanish'))

def clean_text(text: str) -> str:
    """
    Limpia el texto de entrada: minúsculas, remueve puntuación, 
    números y palabras vacías (stopwords).
    """
    if not isinstance(text, str):
        return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Remover puntuación y números
    text = re.sub(r'[^a-záéíóúñ\s]', '', text)
    
    # Remover espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remover stop words
    words = text.split()
    words = [w for w in words if w not in stop_words]
    
    return " ".join(words)
