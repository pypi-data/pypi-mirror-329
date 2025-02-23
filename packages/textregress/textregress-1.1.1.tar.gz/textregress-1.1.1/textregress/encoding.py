from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import AutoTokenizer, AutoModel
import warnings

def get_encoder(model_identifier, **kwargs):
    """
    Factory function to obtain an encoder based on the model identifier.
    
    Args:
        model_identifier (str): Identifier for the encoding model.
        **kwargs: Additional keyword arguments.
                  For example, if model_identifier indicates TFIDF, these are passed
                  to the TfidfVectorizer.
        
    Returns:
        An encoder object with an `encode` method.
    """
    model_identifier_lower = model_identifier.lower() if isinstance(model_identifier, str) else ""
    if "tfidf" in model_identifier_lower:
        return TfidfEncoder(**kwargs)
    elif "sentence-transformers" in model_identifier_lower:
        return SentenceTransformerEncoder(model_identifier)
    else:
        # Use a generic HuggingFace encoder for any other model identifier.
        return HuggingFaceEncoder(model_identifier)

class SentenceTransformerEncoder:
    """
    Encoder using the SentenceTransformer library.
    """
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    
    def encode(self, text):
        """
        Encode text (or a text chunk) into a vector representation.
        
        Args:
            text (str): The text to encode.
            
        Returns:
            vector (torch.Tensor): Encoded vector.
        """
        return self.model.encode(text, convert_to_tensor=True)

class TfidfEncoder:
    """
    Encoder using TFIDF Vectorizer.
    
    Note:
        The TFIDF encoder must be fitted on the full text corpus before encoding chunks.
        This version allows customization by accepting additional keyword arguments
        that are passed to the underlying TfidfVectorizer.
    """
    def __init__(self, **kwargs):
        self.vectorizer = TfidfVectorizer(**kwargs)
        self.fitted = False
        self.output_dim = None
    
    def fit(self, texts):
        """
        Fit the TFIDF vectorizer on a list of texts.
        
        Args:
            texts (list): List of text documents.
        """
        self.vectorizer.fit(texts)
        self.fitted = True
        self.output_dim = len(self.vectorizer.get_feature_names_out())
    
    def encode(self, text):
        """
        Encode text using the fitted TFIDF vectorizer.
        
        Args:
            text (str): The text to encode.
            
        Returns:
            vector (torch.Tensor): Encoded vector representation.
        """
        if not self.fitted:
            warnings.warn("TFIDF encoder has not been fitted yet. Fitting on the provided text as fallback.")
            self.fit([text])
        encoded = self.vectorizer.transform([text]).toarray()[0]
        return torch.tensor(encoded, dtype=torch.float32)

class HuggingFaceEncoder:
    """
    Encoder using HuggingFace transformers.
    
    This encoder loads a pre-trained model and tokenizer from HuggingFace and uses
    mean pooling over the token embeddings (from the last hidden state) as the sentence embedding.
    """
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
    
    def encode(self, text):
        """
        Encode text (or a text chunk) into a vector representation using a HuggingFace model.
        
        Args:
            text (str): The text to encode.
            
        Returns:
            vector (torch.Tensor): Encoded vector.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling: average the token embeddings along the sequence dimension.
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze(0)
        return embeddings
