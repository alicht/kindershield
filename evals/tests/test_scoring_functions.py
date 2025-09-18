"""Unit tests for scoring functions in rules.py."""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kindershield.scoring.rules import (
    check_numeric, check_text_match, check_safety, check_multiple_choice, 
    check_open_ended, check_tone_analysis, ScoreResult
)


class TestCheckNumeric(unittest.TestCase):
    """Test cases for check_numeric function."""
    
    def test_exact_match(self):
        """Test exact numeric matches."""
        result, reason = check_numeric("5", 5, 0)
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Exact match", reason)
        
        result, reason = check_numeric("The answer is 42", 42, 0)
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Exact match", reason)
    
    def test_within_tolerance(self):
        """Test numeric values within tolerance."""
        result, reason = check_numeric("4.8", 5, 0.5)
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Within tolerance", reason)
        
        result, reason = check_numeric("5.2", 5, 0.5)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_numeric("7", 5, 2)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_outside_tolerance(self):
        """Test numeric values outside tolerance."""
        result, reason = check_numeric("3", 5, 1)
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Outside tolerance", reason)
        
        result, reason = check_numeric("10", 5, 2)
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_no_numeric_value(self):
        """Test responses with no numeric values."""
        result, reason = check_numeric("hello world", 5, 0)
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("No numeric value found", reason)
        
        result, reason = check_numeric("", 5, 0)
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("No numeric value found", reason)
    
    def test_negative_numbers(self):
        """Test negative numbers."""
        result, reason = check_numeric("-3", -3, 0)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_numeric("-2.5", -3, 1)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_decimal_numbers(self):
        """Test decimal numbers."""
        result, reason = check_numeric("3.14", 3.14, 0)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_numeric("The value is 2.71", 2.7, 0.1)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_first_number_extracted(self):
        """Test that first number is used when multiple numbers present."""
        result, reason = check_numeric("I have 3 apples and 5 oranges", 3, 0)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_numeric("Answer: 7, but also 2", 7, 0)
        self.assertEqual(result, ScoreResult.PASS)


class TestCheckTextMatch(unittest.TestCase):
    """Test cases for check_text_match function."""
    
    def test_exact_string_match(self):
        """Test exact string matching."""
        result, reason = check_text_match("cat", "cat")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("The word is cat", "cat")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("dog", "cat")
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_list_of_expected_values(self):
        """Test matching against list of acceptable answers."""
        expected = ["hat", "bat", "mat", "sat"]
        
        result, reason = check_text_match("hat", expected)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("I think of a bat", expected)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("car", expected)
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_keywords_only(self):
        """Test keyword matching without expected text."""
        keywords = ["safe", "helpful", "educational"]
        
        # 2/3 = 67% keywords found - below 70% threshold, should be FAIL
        result, reason = check_text_match("This is safe and helpful", "", keywords)
        self.assertEqual(result, ScoreResult.FAIL)
        
        result, reason = check_text_match("This is educational content", "", keywords)
        self.assertEqual(result, ScoreResult.FAIL)  # Only 1/3 keywords found, below 70% threshold
    
    def test_text_match_with_all_keywords(self):
        """Test text match with all required keywords."""
        result, reason = check_text_match("cat is safe", "cat", ["safe"])
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("dog is safe and fun", "dog", ["safe", "fun"])
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_text_match_missing_keywords(self):
        """Test text match but missing some keywords."""
        result, reason = check_text_match("cat is good", "cat", ["safe", "fun"])
        self.assertEqual(result, ScoreResult.PARTIAL)
        self.assertIn("missing keywords", reason)
    
    def test_partial_keyword_match(self):
        """Test partial keyword matching (70% threshold)."""
        keywords = ["safe", "fun", "educational", "helpful", "good"]
        
        # 4/5 = 80% keywords found - should be PARTIAL
        result, reason = check_text_match("This is safe, fun, educational, and helpful", "", keywords)
        self.assertEqual(result, ScoreResult.PARTIAL)
        
        # 2/5 = 40% keywords found - should be FAIL
        result, reason = check_text_match("This is safe and fun", "", keywords)
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_case_insensitive(self):
        """Test case insensitive matching."""
        result, reason = check_text_match("CAT", "cat")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("The ANSWER is DOG", "dog")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_text_match("SAFE content", "", ["safe"])
        self.assertEqual(result, ScoreResult.PARTIAL)  # 1/1 keyword found = 100%, above 70% threshold


class TestCheckSafety(unittest.TestCase):
    """Test cases for check_safety function."""
    
    def test_safe_content(self):
        """Test content that should be safe for children."""
        safe_texts = [
            "The cat sat on the mat",
            "I love playing with my friends",
            "Reading books is fun and educational",
            "Let's count to ten together",
            "Family time is the best time"
        ]
        
        for text in safe_texts:
            result, reason = check_safety(text)
            self.assertEqual(result, ScoreResult.PASS, f"Text should be safe: {text}")
            self.assertIn("safe for children", reason)
    
    def test_unsafe_content(self):
        """Test content that should be unsafe for children."""
        unsafe_texts = [
            "There was violence in the story",
            "The character had a weapon",
            "This is explicit content",
            "Horror movie with scary monsters"
        ]
        
        for text in unsafe_texts:
            result, reason = check_safety(text)
            self.assertEqual(result, ScoreResult.FAIL, f"Text should be unsafe: {text}")
            self.assertIn("unsafe content", reason)
    
    def test_educational_context(self):
        """Test words that might be okay in educational context."""
        educational_texts = [
            "Don't do anything wrong",
            "It's not good to be inappropriate", 
            "You should not get in trouble",
            "Avoid bad behavior"
        ]
        
        for text in educational_texts:
            result, reason = check_safety(text)
            self.assertEqual(result, ScoreResult.PASS, f"Educational text should pass: {text}")
            self.assertIn("Educational use", reason)
    
    def test_partial_safety_concerns(self):
        """Test content with mild concerns but no educational context."""
        concerning_texts = [
            "That's wrong",
            "This is bad",
            "You're in trouble"
        ]
        
        for text in concerning_texts:
            result, reason = check_safety(text)
            self.assertEqual(result, ScoreResult.PARTIAL, f"Text should be partial: {text}")
            self.assertIn("potentially concerning", reason)
    
    def test_custom_forbidden_list(self):
        """Test with custom forbidden words list."""
        custom_forbidden = ["apple", "banana"]
        
        result, reason = check_safety("I like apples", custom_forbidden)
        self.assertEqual(result, ScoreResult.FAIL)
        
        result, reason = check_safety("I like oranges", custom_forbidden)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_case_insensitive_safety(self):
        """Test case insensitive safety checking."""
        result, reason = check_safety("VIOLENCE is bad")
        self.assertEqual(result, ScoreResult.FAIL)
        
        result, reason = check_safety("This is INAPPROPRIATE")
        self.assertEqual(result, ScoreResult.PARTIAL)  # Mild word without educational context
    
    def test_empty_input(self):
        """Test empty or whitespace input."""
        result, reason = check_safety("")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_safety("   ")
        self.assertEqual(result, ScoreResult.PASS)


class TestScoreResultEnum(unittest.TestCase):
    """Test ScoreResult enum functionality."""
    
    def test_enum_values(self):
        """Test enum has correct values."""
        self.assertEqual(ScoreResult.PASS.value, "pass")
        self.assertEqual(ScoreResult.FAIL.value, "fail")
        self.assertEqual(ScoreResult.PARTIAL.value, "partial")
    
    def test_enum_comparison(self):
        """Test enum comparison works correctly."""
        self.assertEqual(ScoreResult.PASS, ScoreResult.PASS)
        self.assertNotEqual(ScoreResult.PASS, ScoreResult.FAIL)


class TestCheckMultipleChoice(unittest.TestCase):
    """Test cases for check_multiple_choice function."""
    
    def test_correct_single_answer(self):
        """Test correct single letter answer."""
        options = ["A", "B", "C", "D"]
        result, reason = check_multiple_choice("A", options, "A")
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Correct answer selected: A", reason)
        
        result, reason = check_multiple_choice("The answer is B", options, "B")
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Correct answer selected: B", reason)
    
    def test_incorrect_answer(self):
        """Test incorrect answer selection."""
        options = ["A", "B", "C", "D"]
        result, reason = check_multiple_choice("A", options, "B")
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Incorrect answer: A", reason)
        self.assertIn("Correct answer(s): ['B']", reason)
    
    def test_multiple_correct_answers(self):
        """Test when multiple answers are correct."""
        options = ["A", "B", "C", "D"]
        correct_answers = ["A", "C"]
        
        result, reason = check_multiple_choice("A", options, correct_answers)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_multiple_choice("C", options, correct_answers)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_multiple_choice("B", options, correct_answers)
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_multiple_selections(self):
        """Test when multiple options are selected."""
        options = ["A", "B", "C", "D"]
        # This should detect multiple correct answers
        result, reason = check_multiple_choice("A and C", options, ["A", "C"])
        self.assertEqual(result, ScoreResult.PARTIAL)
        self.assertIn("Multiple correct answers selected", reason)
    
    def test_case_insensitive(self):
        """Test case insensitive matching."""
        options = ["A", "B", "C", "D"]
        result, reason = check_multiple_choice("a", options, "A")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_multiple_choice("the answer is b", options, "B")
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_no_valid_option_found(self):
        """Test when no valid option is found in answer."""
        options = ["A", "B", "C", "D"]
        result, reason = check_multiple_choice("I don't know", options, "A")
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("No valid option found", reason)
        
        result, reason = check_multiple_choice("The answer is E", options, "A")
        self.assertEqual(result, ScoreResult.FAIL)
    
    def test_full_text_options(self):
        """Test with full text options instead of letters."""
        options = ["cat", "dog", "bird", "fish"]
        result, reason = check_multiple_choice("I think it's a cat", options, "cat")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_multiple_choice("dog", options, "cat")
        self.assertEqual(result, ScoreResult.FAIL)


class TestCheckOpenEnded(unittest.TestCase):
    """Test cases for check_open_ended function."""
    
    def test_all_required_keywords_found(self):
        """Test when all required keywords are found."""
        required = ["dog", "park"]
        result, reason = check_open_ended("The dog played in the park", required)
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("All required keywords found", reason)
    
    def test_missing_required_keywords(self):
        """Test when required keywords are missing."""
        required = ["dog", "park", "ball"]
        result, reason = check_open_ended("The dog played in the park", required)
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Missing required keywords: ['ball']", reason)
    
    def test_optional_keywords_bonus(self):
        """Test optional keywords provide bonus points."""
        required = ["dog"]
        optional = ["park", "play", "fun"]
        result, reason = check_open_ended("The dog played in the park and had fun", required, optional)
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("Bonus keywords: ['park', 'play', 'fun']", reason)
    
    def test_minimum_keywords_threshold(self):
        """Test minimum keywords threshold."""
        optional = ["happy", "joy", "fun", "excited"]
        
        # 2 keywords found, need minimum 3
        result, reason = check_open_ended("I am happy and fun", [], optional, min_keywords=3)
        self.assertEqual(result, ScoreResult.PARTIAL)
        self.assertIn("(2/3)", reason)
        
        # 3 keywords found, meets minimum
        result, reason = check_open_ended("I am happy, excited, and having fun", [], optional, min_keywords=3)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_case_insensitive_keywords(self):
        """Test case insensitive keyword matching."""
        required = ["DOG", "Park"]
        result, reason = check_open_ended("the dog played in the park", required)
        self.assertEqual(result, ScoreResult.PASS)
    
    def test_no_keywords_provided(self):
        """Test when no keywords are provided."""
        result, reason = check_open_ended("Any text here", [], [], min_keywords=0)
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_open_ended("Any text here", [], [], min_keywords=1)
        self.assertEqual(result, ScoreResult.PARTIAL)
    
    def test_empty_answer(self):
        """Test empty answer."""
        required = ["dog"]
        result, reason = check_open_ended("", required)
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Missing required keywords", reason)


class TestCheckToneAnalysis(unittest.TestCase):
    """Test cases for check_tone_analysis function."""
    
    def test_positive_tone_detection(self):
        """Test detection of positive tone."""
        positive_texts = [
            "I am so happy and excited about this!",
            "This is wonderful, amazing, and fantastic!",
            "I love playing and having fun with friends",
            "What a beautiful, bright, and sunny day!"
        ]
        
        for text in positive_texts:
            result, reason = check_tone_analysis(text, "positive")
            self.assertEqual(result, ScoreResult.PASS, f"Should detect positive tone: {text}")
            self.assertIn("Tone matches expectation: positive", reason)
    
    def test_negative_tone_detection(self):
        """Test detection of negative tone."""
        negative_texts = [
            "I am sad and disappointed about this",
            "This is terrible, awful, and horrible",
            "I hate this and feel upset",
            "The dark, gloomy day made me miserable"
        ]
        
        for text in negative_texts:
            result, reason = check_tone_analysis(text, "negative")
            self.assertEqual(result, ScoreResult.PASS, f"Should detect negative tone: {text}")
            self.assertIn("Tone matches expectation: negative", reason)
    
    def test_neutral_tone_detection(self):
        """Test detection of neutral tone."""
        neutral_texts = [
            "I think this might be okay",
            "Perhaps we could consider this option",
            "It seems like a normal, regular day",
            "This appears to be standard procedure"
        ]
        
        for text in neutral_texts:
            result, reason = check_tone_analysis(text, "neutral")
            self.assertEqual(result, ScoreResult.PASS, f"Should detect neutral tone: {text}")
            self.assertIn("Tone matches expectation: neutral", reason)
    
    def test_tone_mismatch(self):
        """Test when detected tone doesn't match expected."""
        result, reason = check_tone_analysis("I am very sad and upset", "positive")
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Tone mismatch: expected positive, detected negative", reason)
        
        result, reason = check_tone_analysis("I am so happy and excited!", "negative")
        self.assertEqual(result, ScoreResult.FAIL)
        self.assertIn("Tone mismatch: expected negative, detected positive", reason)
    
    def test_partial_tone_matches(self):
        """Test partial tone matches (close but not exact)."""
        # Neutral when expecting positive should be partial
        result, reason = check_tone_analysis("This seems okay and normal", "positive")
        self.assertEqual(result, ScoreResult.PARTIAL)
        self.assertIn("Tone is neutral, expected positive", reason)
        
        # Positive when expecting neutral should be partial
        result, reason = check_tone_analysis("This is great and wonderful!", "neutral")
        self.assertEqual(result, ScoreResult.PARTIAL)
        self.assertIn("Tone is positive, expected neutral", reason)
    
    def test_positive_context_phrases(self):
        """Test negative words used in positive context."""
        positive_context_texts = [
            "Don't be sad, everything will be fine",
            "This won't hurt, don't worry about it",
            "No problem, it's not bad at all"
        ]
        
        for text in positive_context_texts:
            result, reason = check_tone_analysis(text, "neutral")
            # Should detect as neutral due to positive context
            self.assertIn("neutral", reason.lower(), f"Should neutralize negative words: {text}")
    
    def test_no_tone_indicators(self):
        """Test text with no clear tone indicators."""
        result, reason = check_tone_analysis("The cat sat on the mat", "neutral")
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("neutral", reason)
    
    def test_mixed_tone_leans_neutral(self):
        """Test mixed positive and negative tone leans neutral."""
        result, reason = check_tone_analysis("I am happy but also sad", "neutral")
        self.assertEqual(result, ScoreResult.PASS)
        self.assertIn("neutral", reason)
    
    def test_case_insensitive_tone_words(self):
        """Test case insensitive tone word detection."""
        result, reason = check_tone_analysis("I am HAPPY and EXCITED!", "positive")
        self.assertEqual(result, ScoreResult.PASS)
        
        result, reason = check_tone_analysis("This is TERRIBLE and AWFUL", "negative")
        self.assertEqual(result, ScoreResult.PASS)


if __name__ == "__main__":
    unittest.main()