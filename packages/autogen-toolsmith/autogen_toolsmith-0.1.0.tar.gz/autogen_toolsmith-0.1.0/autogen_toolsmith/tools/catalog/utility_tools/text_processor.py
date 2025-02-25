"""
Text processing utility tool.
"""

from typing import Dict, List, Optional
from autogen_toolsmith.tools.base.tool_base import BaseTool


class TextProcessorTool(BaseTool):
    """
    A utility tool for performing common text processing operations.
    
    This tool provides functionality for text transformation, extraction,
    and analysis operations like word count, character statistics, case conversion,
    and text summarization.
    
    Example:
        >>> tool = TextProcessorTool()
        >>> result = tool.run("This is a test", operation="word_count")
        >>> print(result)
        {'word_count': 4, 'char_count': 14, 'char_count_no_spaces': 11}
    """
    
    def __init__(self):
        """
        Initialize the text processor tool.
        """
        super().__init__(
            name="text_processor",
            description="A utility tool for text processing operations",
            version="0.1.0",
            author="AutoGen Toolsmith",
            dependencies=[],
            tags=["text", "nlp", "utility"],
            category="utility_tools"
        )
    
    def run(self, text: str, operation: str = "word_count") -> Dict:
        """
        Execute a text processing operation on the provided text.
        
        Args:
            text: The input text to process.
            operation: The operation to perform. Available operations:
                - word_count: Count words, characters, and characters without spaces
                - case_convert: Convert case (to upper, lower, title, etc.)
                - extract_words: Extract words matching a pattern
                - summarize: Generate a simple summary
                
        Returns:
            Dict: A dictionary containing the results of the operation.
            
        Raises:
            ValueError: If an invalid operation is specified.
        """
        if not text:
            return {"error": "Empty text provided"}
            
        if operation == "word_count":
            return self._count_statistics(text)
        elif operation.startswith("case_"):
            case_type = operation.split("_")[1] if len(operation.split("_")) > 1 else "lower"
            return self._convert_case(text, case_type)
        elif operation == "extract_words":
            return self._extract_words(text)
        elif operation == "summarize":
            return self._summarize(text)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def _count_statistics(self, text: str) -> Dict:
        """Count various statistics about the text."""
        words = text.split()
        return {
            "word_count": len(words),
            "char_count": len(text),
            "char_count_no_spaces": len(text.replace(" ", "")),
            "sentence_count": text.count(".") + text.count("!") + text.count("?"),
            "paragraph_count": text.count("\n\n") + 1 if "\n\n" in text else 1
        }
    
    def _convert_case(self, text: str, case_type: str) -> Dict:
        """Convert the case of the text."""
        if case_type == "upper":
            result = text.upper()
        elif case_type == "lower":
            result = text.lower()
        elif case_type == "title":
            result = text.title()
        elif case_type == "capitalize":
            result = text.capitalize()
        elif case_type == "swap":
            result = text.swapcase()
        else:
            result = text
            
        return {
            "original": text,
            "converted": result,
            "case_type": case_type
        }
    
    def _extract_words(self, text: str) -> Dict:
        """Extract words from the text."""
        import re
        words = re.findall(r'\b\w+\b', text)
        return {
            "words": words,
            "unique_words": list(set(words)),
            "word_count": len(words),
            "unique_word_count": len(set(words))
        }
    
    def _summarize(self, text: str) -> Dict:
        """Generate a simple extractive summary of the text."""
        # This is a very basic implementation
        import re
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) <= 2:
            return {"summary": text, "reduction": 0}
        
        # For a very simple summary, take the first and last sentences
        summary = f"{sentences[0]} {sentences[-1]}"
        
        reduction = 1 - (len(summary) / len(text))
        
        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "reduction": round(reduction, 2)
        } 