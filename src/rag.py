import os
from typing import Optional
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever

# Rutas predeterminadas
DOCS_DIR = "data/docs"
INDEX_DIR = "data/faiss_index"

# Modelo de Embeddings local (HuggingFace - Ejecuta en CPU, 384 dimensiones)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_embeddings_instance: Optional[HuggingFaceEmbeddings] = None

def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Patrón Singleton: Carga el modelo de Embeddings en memoria una sola vez.
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    return _embeddings_instance

def build_vector_store() -> FAISS:
    """
    Lee todos los PDFs de 'data/docs', los divide en fragmentos (chunks),
    genera sus embeddings y construye un indice FAISS persistido en disco.
    """
    print(f"⏳ Cargando documentos PDF desde '{DOCS_DIR}'...")
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()

    if not documents:
        raise FileNotFoundError(
            f"❌ No se encontraron archivos PDF en la carpeta '{DOCS_DIR}'. "
            "Por favor, añade al menos un archivo PDF."
        )

    print(f"📄 Se cargaron {len(documents)} página(s) de PDF.")

    # Divisor de texto semántico con solapamiento
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Documentos divididos en {len(chunks)} fragmentos (chunks).")

    print("🧠 Generando embeddings e indexando en FAISS (esto puede tardar unos segundos)...")
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Persistir el índice en disco
    vector_store.save_local(INDEX_DIR)
    print(f"💾 Índice vectorial FAISS guardado exitosamente en '{INDEX_DIR}'.")
    
    return vector_store

def get_retriever(k: int = 3) -> VectorStoreRetriever:
    """
    Retorna un recuperador (Retriever) de FAISS.
    Si el índice no existe en disco, invoca build_vector_store() para construirlo.
    """
    embeddings = get_embeddings()

    if not os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        print("⚠️ No se encontró un índice FAISS existente. Generando uno nuevo...")
        vector_store = build_vector_store()
    else:
        # Cargar índice preexistente desde disco
        vector_store = FAISS.load_local(
            folder_path=INDEX_DIR,
            embeddings=embeddings,
            allow_dangerous_deserialization=True  # Requerido por LangChain para archivos local pkl de confianza
        )

    # Configurar el retriever para devolver los k fragmentos más similares
    return vector_store.as_retriever(search_kwargs={"k": k})