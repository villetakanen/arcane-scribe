"""PDF ingestion and processing module."""

import pathlib
from typing import List, Dict, Any, Optional
import logging

import pypdf
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF text extraction, chunking, and vector storage."""
    
    def __init__(self, db_dir: pathlib.Path, embedding_model: str = "BAAI/bge-small-en-v1.5"):
        """Initialize the PDF processor.
        
        Args:
            db_dir: Directory for ChromaDB persistence
            embedding_model: Sentence transformer model name
        """
        self.db_dir = db_dir
        self.db_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=str(db_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedder = SentenceTransformer(embedding_model)
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="rpg_rules",
            metadata={"description": "RPG rulebook text chunks"}
        )
    
    def extract_text_from_pdf(self, pdf_path: pathlib.Path) -> List[Dict[str, Any]]:
        """Extract text from a PDF file with page-level metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries with text and metadata for each page
        """
        pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():  # Only include pages with text
                        pages.append({
                            'text': text,
                            'source_file': pdf_path.name,
                            'page_number': page_num,
                            'total_pages': len(pdf_reader.pages)
                        })
                        
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            raise
            
        return pages
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Target size for each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start + chunk_size - 100, start)
                for i in range(end - 1, search_start - 1, -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
                
        return chunks
    
    def process_pdf(self, pdf_path: pathlib.Path) -> int:
        """Process a single PDF file and store in ChromaDB.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of chunks created
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Extract text from PDF
        pages = self.extract_text_from_pdf(pdf_path)
        
        # Process each page
        all_chunks = []
        all_embeddings = []
        all_metadatas = []
        all_ids = []
        
        chunk_count = 0
        
        for page in pages:
            # Chunk the page text
            chunks = self.chunk_text(page['text'])
            
            for i, chunk in enumerate(chunks):
                # Create unique ID
                chunk_id = f"{pdf_path.stem}_p{page['page_number']}_c{i}"
                
                # Generate embedding
                embedding = self.embedder.encode(chunk).tolist()
                
                # Prepare metadata
                metadata = {
                    'source_file': page['source_file'],
                    'page_number': page['page_number'],
                    'total_pages': page['total_pages'],
                    'chunk_index': i,
                    'chunk_text': chunk[:100] + "..." if len(chunk) > 100 else chunk  # Preview
                }
                
                all_chunks.append(chunk)
                all_embeddings.append(embedding)
                all_metadatas.append(metadata)
                all_ids.append(chunk_id)
                chunk_count += 1
        
        # Store in ChromaDB
        if all_chunks:
            self.collection.add(
                documents=all_chunks,
                embeddings=all_embeddings,
                metadatas=all_metadatas,
                ids=all_ids
            )
            logger.info(f"Stored {chunk_count} chunks from {pdf_path}")
        
        return chunk_count
    
    def process_directory(self, pdf_dir: pathlib.Path, reset: bool = False) -> int:
        """Process all PDF files in a directory.
        
        Args:
            pdf_dir: Directory containing PDF files
            reset: Whether to reset the database before processing
            
        Returns:
            Total number of chunks created
        """
        if reset:
            logger.info("Resetting database...")
            self.chroma_client.delete_collection("rpg_rules")
            self.collection = self.chroma_client.create_collection(
                name="rpg_rules",
                metadata={"description": "RPG rulebook text chunks"}
            )
        
        # Find all PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return 0
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        total_chunks = 0
        
        # Process each PDF
        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            try:
                chunks = self.process_pdf(pdf_file)
                total_chunks += chunks
            except Exception as e:
                logger.error(f"Failed to process {pdf_file}: {e}")
                continue
        
        logger.info(f"Processing complete. Total chunks created: {total_chunks}")
        return total_chunks
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        
        # Get sample metadata to understand structure
        sample = self.collection.get(limit=1, include=['metadatas'])
        
        return {
            'total_chunks': count,
            'collection_name': self.collection.name,
            'sample_metadata': sample['metadatas'][0] if sample['metadatas'] else None
        }
