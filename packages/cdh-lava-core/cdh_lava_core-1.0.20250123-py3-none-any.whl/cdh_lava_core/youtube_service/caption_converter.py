import re
from webvtt import WebVTT
import os
import nltk
from nltk.tokenize import sent_tokenize
import ssl
from datetime import datetime


class CaptionConverter:
    # Class variable to track if NLTK data is downloaded
    _nltk_downloaded = False
    PAUSE_THRESHOLD = 1.5  # seconds that indicate a natural break
    
    @classmethod
    def ensure_nltk_downloaded(cls):
        """Ensure NLTK data is downloaded"""
        if not cls._nltk_downloaded:
            try:
                # Create SSL context for downloading
                try:
                    _create_unverified_https_context = ssl._create_unverified_context
                except AttributeError:
                    pass
                else:
                    ssl._create_default_https_context = _create_unverified_https_context
                
                # Set NLTK data path to user's home directory
                home = os.path.expanduser("~")
                nltk_data_dir = os.path.join(home, 'nltk_data')
                os.makedirs(nltk_data_dir, exist_ok=True)
                nltk.data.path.append(nltk_data_dir)
                
                # Download punkt data
                nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
                nltk.download('punkt_tab', download_dir=nltk_data_dir, quiet=True)
                
                cls._nltk_downloaded = True
                
            except Exception as e:
                print(f"Warning: NLTK download failed: {str(e)}")
                print("Falling back to basic sentence tokenization")
                cls._nltk_downloaded = False
                
 

    @staticmethod
    def format_text(text: str) -> str:
        """Format text with proper capitalization and punctuation"""
        # Add period if sentence doesn't end with punctuation
        sentences = text.split('. ')
        formatted_sentences = []
        
        for sentence in sentences:
            # Clean up the sentence
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Capitalize first letter
            sentence = sentence[0].upper() + sentence[1:] if sentence else ''
            
            # Add period if not ending with punctuation
            if not sentence[-1] in '.!?':
                sentence += '.'
                
            formatted_sentences.append(sentence)
        
        return ' '.join(formatted_sentences)

    @staticmethod
    def create_paragraphs(sentences: list, sentences_per_paragraph: int = 3) -> list:
        """Group sentences into paragraphs"""
        paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            current_paragraph.append(sentence)
            
            # Start new paragraph after sentences_per_paragraph
            if len(current_paragraph) >= sentences_per_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Add any remaining sentences
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
            
        return paragraphs

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean caption text by removing markup and special characters"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove timestamps
        text = re.sub(r'\[\d+:\d+\.\d+\]', '', text)
        text = re.sub(r'<\d+:\d+\.\d+>', '', text)
        # Remove multiple spaces and newlines
        text = ' '.join(text.split())
        return text.strip()

    @staticmethod
    def remove_duplicates(text_segments):
        """Remove overlapping text segments"""
        if not text_segments:
            return []

        result = []
        current_text = text_segments[0]
        
        for next_text in text_segments[1:]:
            # Skip if texts are identical
            if current_text == next_text:
                continue
                
            # Check if next_text is fully contained in current_text
            if next_text in current_text:
                continue
                
            # Check if current_text is contained in next_text
            if current_text in next_text:
                current_text = next_text
                continue
                
            # Find the longest overlapping suffix/prefix
            overlap_found = False
            for i in range(min(len(current_text), len(next_text)), 2, -1):
                if current_text.endswith(next_text[:i]):
                    current_text = current_text + next_text[i:]
                    overlap_found = True
                    break
            
            if not overlap_found:
                result.append(current_text)
                current_text = next_text
        
        result.append(current_text)
        return result

    @staticmethod
    def detect_sentences(text: str) -> list:
        """Split text into sentences using multiple heuristics"""
        # Common sentence endings
        endings = r'[.!?]'
        # Common conjunctions and transition words that often start new sentences
        transitions = r'(?:but|however|therefore|moreover|furthermore|in addition|also|then|next|finally|lastly)'
        
        # Split on multiple criteria
        potential_sentences = []
        
        # First split on clear sentence endings
        parts = re.split(f'({endings}\\s+)', text)
        current_sentence = []
        
        for part in parts:
            if part.strip():
                current_sentence.append(part)
                if re.search(endings, part):
                    potential_sentences.append(''.join(current_sentence).strip())
                    current_sentence = []
        
        if current_sentence:
            # If no clear sentence endings, try splitting on transitions
            final_part = ''.join(current_sentence)
            transition_splits = re.split(f'\\s+(?={transitions}\\s+)', final_part, flags=re.IGNORECASE)
            potential_sentences.extend(transition_splits)
        
        # Clean up sentences
        cleaned_sentences = []
        for sentence in potential_sentences:
            sentence = sentence.strip()
            if sentence:
                # Add period if no ending punctuation
                if not re.search(endings, sentence[-1]):
                    sentence += '.'
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences

    @staticmethod
    def format_sentences(sentences):
        """Format and group sentences into paragraphs"""
        formatted = []
        for sentence in sentences:
            # Capitalize first letter
            if sentence:
                sentence = sentence.strip()
                sentence = sentence[0].upper() + sentence[1:]
                formatted.append(sentence)
        
        # Group into paragraphs (3 sentences per paragraph)
        paragraphs = []
        for i in range(0, len(formatted), 3):
            paragraph = ' '.join(formatted[i:i+3])
            if paragraph:
                paragraphs.append(paragraph)
        
        return paragraphs

    @classmethod
    def vtt_to_text(cls, vtt_file: str, output_file: str = None) -> str:
        """Convert VTT file to clean readable text"""
        if not os.path.exists(vtt_file):
            raise FileNotFoundError(f"VTT file not found: {vtt_file}")
        
        try:
            text_segments = []
            vtt = WebVTT().read(vtt_file)
            
            # First pass: collect and clean text
            for caption in vtt:
                clean_caption = cls.clean_text(caption.text)
                if not clean_caption or clean_caption.lower() == '[music]':
                    continue
                text_segments.append(clean_caption)
            
            # Remove duplicates
            deduped_text = cls.remove_duplicates(text_segments)
            
            # Detect sentences in the deduplicated text
            all_sentences = []
            for text in deduped_text:
                sentences = cls.detect_sentences(text)
                all_sentences.extend(sentences)
            
            # Format sentences and create paragraphs
            formatted_sentences = []
            for sentence in all_sentences:
                if sentence.strip():
                    # Capitalize first letter
                    sentence = sentence[0].upper() + sentence[1:]
                    formatted_sentences.append(sentence)
            
            # Group into paragraphs
            paragraphs = []
            for i in range(0, len(formatted_sentences), 3):
                paragraph = ' '.join(formatted_sentences[i:i+3])
                paragraphs.append(paragraph)
            
            # Join paragraphs with double newlines
            final_text = '\n\n'.join(paragraphs)
            
            # Save to file if output_file is specified
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(final_text)
            
            return final_text
            
        except Exception as e:
            error_msg = f"Error processing VTT file {vtt_file}: {str(e)}"
            print(error_msg)
            raise ValueError(error_msg) from e

    @staticmethod
    def convert_directory(input_dir: str, output_dir: str = None):
        """
        Convert all VTT files in a directory to text files
        
        Args:
            input_dir: Directory containing VTT files
            output_dir: Directory for output text files (defaults to input_dir)
        """
        if output_dir is None:
            output_dir = input_dir
        
        os.makedirs(output_dir, exist_ok=True)
        
        vtt_files = [f for f in os.listdir(input_dir) if f.endswith('.vtt')]
        converted = []
        failed = []
        
        for vtt_file in vtt_files:
            try:
                input_path = os.path.join(input_dir, vtt_file)
                output_path = os.path.join(output_dir, vtt_file.rsplit('.', 1)[0] + '.txt')
                
                CaptionConverter.vtt_to_text(input_path, output_path)
                converted.append(vtt_file)
                print(f"Converted: {vtt_file}")
                
            except Exception as e:
                failed.append((vtt_file, str(e)))
                print(f"Failed to convert {vtt_file}: {str(e)}")
        
        print(f"\nConversion Summary:")
        print(f"Successfully converted: {len(converted)}")
        print(f"Failed conversions: {len(failed)}")
        
        return converted, failed

# Example usage
if __name__ == "__main__":
    # Convert single file
    text = CaptionConverter.vtt_to_text(
        "input.vtt",
        "output.txt"
    )
    
    # Convert entire directory
    converted, failed = CaptionConverter.convert_directory(
        "captions_directory",
        "text_output_directory"
    )