import pytest
from src.markgdoc.markgdoc import (
    remove_emojis,
    is_bullet_char,
    is_paragraph,
    preprocess_nested_styles
)


class TestEnhancedFeatures:
    
    def test_remove_emojis(self):
        """Test emoji removal functionality"""
        # Test with various emojis
        text_with_emojis = "Hello 😀 World 🌍! Testing 🚀 emojis."
        expected = "Hello  World ! Testing  emojis."
        assert remove_emojis(text_with_emojis) == expected
        
        # Test with no emojis
        text_no_emojis = "Hello World! No emojis here."
        assert remove_emojis(text_no_emojis) == text_no_emojis
        
        # Test with empty string
        assert remove_emojis("") == ""

    def test_is_bullet_char(self):
        """Test bullet character detection"""
        # Test standard bullet characters
        assert is_bullet_char('-') == True
        assert is_bullet_char('•') == True
        assert is_bullet_char('–') == True  # en dash
        assert is_bullet_char('—') == True  # em dash
        assert is_bullet_char('‐') == True  # hyphen
        assert is_bullet_char('‑') == True  # non-breaking hyphen
        assert is_bullet_char('◦') == True  # white bullet
        assert is_bullet_char('▪') == True  # black small square
        assert is_bullet_char('▫') == True  # white small square
        assert is_bullet_char('‣') == True  # triangular bullet
        assert is_bullet_char('⁃') == True  # hyphen bullet
        
        # Test non-bullet characters
        assert is_bullet_char('a') == False
        assert is_bullet_char('1') == False
        assert is_bullet_char(' ') == False
        assert is_bullet_char('#') == False

    def test_is_paragraph_enhanced_bullets(self):
        """Test paragraph detection with enhanced bullet support"""
        # Test standard bullet points
        assert is_paragraph("- This is a bullet point") == False
        assert is_paragraph("• This is a bullet point") == False
        assert is_paragraph("– This is a bullet point") == False
        assert is_paragraph("— This is a bullet point") == False
        
        # Test regular paragraphs
        assert is_paragraph("This is a regular paragraph") == True
        assert is_paragraph("Just some text without special formatting") == True
        
        # Test other markdown syntax
        assert is_paragraph("# Header") == False
        assert is_paragraph("## Header 2") == False
        assert is_paragraph("1. Ordered list") == False
        assert is_paragraph("|Table|Row|") == False
        assert is_paragraph("---") == False

    def test_preprocess_nested_styles_enhanced_patterns(self):
        """Test enhanced bold/italic pattern recognition"""
        # Test bold patterns with asterisks
        style_requests, cleaned = preprocess_nested_styles("**bold text**", 0, True)
        assert "bold text" in cleaned
        assert len(style_requests) > 0
        
        # Test bold patterns with underscores
        style_requests, cleaned = preprocess_nested_styles("__bold text__", 0, True)
        assert "bold text" in cleaned
        assert len(style_requests) > 0
        
        # Test italic patterns with asterisks
        style_requests, cleaned = preprocess_nested_styles("*italic text*", 0, True)
        assert "italic text" in cleaned
        assert len(style_requests) > 0
        
        # Test italic patterns with underscores
        style_requests, cleaned = preprocess_nested_styles("_italic text_", 0, True)
        assert "italic text" in cleaned
        assert len(style_requests) > 0
        
        # Test bold-italic combinations
        style_requests, cleaned = preprocess_nested_styles("***bold italic***", 0, True)
        assert "bold italic" in cleaned
        assert len(style_requests) > 0
        
        style_requests, cleaned = preprocess_nested_styles("**_bold italic_**", 0, True)
        assert "bold italic" in cleaned
        assert len(style_requests) > 0
        
        style_requests, cleaned = preprocess_nested_styles("_**bold italic**_", 0, True)
        assert "bold italic" in cleaned
        assert len(style_requests) > 0
        
        style_requests, cleaned = preprocess_nested_styles("___bold italic___", 0, True)
        assert "bold italic" in cleaned
        assert len(style_requests) > 0

    def test_preprocess_nested_styles_emoji_removal(self):
        """Test that emojis are removed during style preprocessing"""
        text_with_emoji = "**bold 😀 text**"
        style_requests, cleaned = preprocess_nested_styles(text_with_emoji, 0, True)
        
        # Emoji should be removed
        assert "😀" not in cleaned
        assert "bold  text" in cleaned  # Note the double space where emoji was
        assert len(style_requests) > 0

    def test_preprocess_nested_styles_hyperlinks(self):
        """Test hyperlink processing"""
        text_with_link = "[Google](https://www.google.com)"
        style_requests, cleaned = preprocess_nested_styles(text_with_link, 0, True)
        
        assert "Google" in cleaned
        assert "https://www.google.com" not in cleaned
        assert len(style_requests) > 0

    def test_preprocess_nested_styles_strikethrough(self):
        """Test strikethrough processing"""
        text_with_strike = "~strikethrough text~"
        style_requests, cleaned = preprocess_nested_styles(text_with_strike, 0, True)
        
        assert "strikethrough text" in cleaned
        assert len(style_requests) > 0
