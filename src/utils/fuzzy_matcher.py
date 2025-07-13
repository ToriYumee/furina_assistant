from typing import List, Tuple, Optional
import re

class FuzzyMatcher:
    """Simple fuzzy string matching without external dependencies"""
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return FuzzyMatcher.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def similarity_ratio(s1: str, s2: str) -> float:
        """Calculate similarity ratio between two strings (0-100)"""
        s1_clean = FuzzyMatcher._clean_string(s1)
        s2_clean = FuzzyMatcher._clean_string(s2)
        
        if not s1_clean or not s2_clean:
            return 0.0
        
        max_len = max(len(s1_clean), len(s2_clean))
        if max_len == 0:
            return 100.0
        
        distance = FuzzyMatcher.levenshtein_distance(s1_clean, s2_clean)
        ratio = ((max_len - distance) / max_len) * 100
        return ratio
    
    @staticmethod
    def _clean_string(s: str) -> str:
        """Clean and normalize string for comparison"""
        # Convert to lowercase
        s = s.lower()
        # Remove extra whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        # Remove common stop words in Spanish and English
        stop_words = ['el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 'y', 'o',
                     'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for']
        words = s.split()
        words = [w for w in words if w not in stop_words]
        return ' '.join(words)
    
    @staticmethod
    def find_best_match(text: str, candidates: List[str], threshold: float = 60.0) -> Optional[Tuple[str, float]]:
        """Find the best matching candidate string"""
        if not text or not candidates:
            return None
        
        best_match = None
        best_score = 0.0
        
        for candidate in candidates:
            score = FuzzyMatcher.similarity_ratio(text, candidate)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = candidate
        
        return (best_match, best_score) if best_match else None
    
    @staticmethod
    def partial_match(text: str, target: str, threshold: float = 70.0) -> bool:
        """Check if text partially matches target"""
        text_clean = FuzzyMatcher._clean_string(text)
        target_clean = FuzzyMatcher._clean_string(target)
        
        # Direct substring match
        if target_clean in text_clean or text_clean in target_clean:
            return True
        
        # Fuzzy match
        score = FuzzyMatcher.similarity_ratio(text_clean, target_clean)
        return score >= threshold
    
    @staticmethod
    def extract_keywords(text: str, keyword_list: List[str], threshold: float = 60.0) -> List[Tuple[str, float]]:
        """Extract keywords from text that match the keyword list"""
        matches = []
        text_words = FuzzyMatcher._clean_string(text).split()
        
        for keyword in keyword_list:
            keyword_clean = FuzzyMatcher._clean_string(keyword)
            keyword_words = keyword_clean.split()
            
            # Check for exact word matches first
            if any(word in text_words for word in keyword_words):
                matches.append((keyword, 100.0))
                continue
            
            # Check fuzzy match
            best_score = 0.0
            for text_word in text_words:
                for keyword_word in keyword_words:
                    score = FuzzyMatcher.similarity_ratio(text_word, keyword_word)
                    if score > best_score:
                        best_score = score
            
            if best_score >= threshold:
                matches.append((keyword, best_score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

class SmartCommandMatcher:
    """Enhanced command matching with fuzzy logic"""
    
    def __init__(self, threshold: float = 60.0):
        self.threshold = threshold
        self.fuzzy = FuzzyMatcher()
    
    def find_command_match(self, text: str, commands: List[object]) -> Optional[Tuple[object, float, str]]:
        """
        Find the best matching command for the given text
        Returns: (command_object, confidence_score, matched_keyword)
        """
        best_command = None
        best_score = 0.0
        best_keyword = ""
        
        for command in commands:
            if not hasattr(command, 'keywords'):
                continue
            
            # Try exact matches first
            for keyword in command.keywords:
                if self.fuzzy.partial_match(text, keyword, threshold=90.0):
                    return (command, 100.0, keyword)
            
            # Try fuzzy matches
            keyword_matches = self.fuzzy.extract_keywords(text, command.keywords, self.threshold)
            
            if keyword_matches:
                top_match = keyword_matches[0]
                if top_match[1] > best_score:
                    best_score = top_match[1]
                    best_command = command
                    best_keyword = top_match[0]
        
        return (best_command, best_score, best_keyword) if best_command else None
    
    def suggest_corrections(self, text: str, commands: List[object], max_suggestions: int = 3) -> List[str]:
        """Suggest command corrections based on fuzzy matching"""
        all_keywords = []
        for command in commands:
            if hasattr(command, 'keywords'):
                all_keywords.extend(command.keywords)
        
        matches = self.fuzzy.extract_keywords(text, all_keywords, threshold=30.0)
        suggestions = [match[0] for match in matches[:max_suggestions]]
        return suggestions