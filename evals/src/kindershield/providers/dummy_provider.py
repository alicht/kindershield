"""Dummy provider for testing and development."""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class Provider(ABC):
    """Unified interface for AI providers."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the provider with model name and API key."""
        self.model_name = model_name
        self.api_key = api_key
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the AI provider."""
        pass


class DummyProvider(Provider):
    """Dummy provider that returns predefined responses for testing."""
    
    def __init__(self, model_name: str = "dummy-small", api_key: Optional[str] = None):
        """Initialize the dummy provider."""
        super().__init__(model_name, api_key)
        self.responses = {
            # Math responses
            "addition": "5",
            "subtraction": "3", 
            "counting": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            "number_after": "8",
            "number_before": "8",
            "fingers": "5",
            "bigger": "7",
            "triangle": "3",
            "pennies": "5",
            
            # Reading responses
            "letter_a": "The letter A makes the 'ah' sound like in 'apple'.",
            "cat_word": "That word says 'cat'.",
            "dog_story": "The dog will probably dig a hole and bury the bone for later!",
            "favorite_book": "I love books about friendly animals and fun adventures!",
            "three_things": "You can read books, signs, and labels around you.",
            "rhymes_cat": "hat",
            "park_story": "First, you would get ready and walk to the park.",
            "after_b": "C",
            "dog_sound": "The beginning sound is 'd'.",
            "ball_picture": "The story might be about a child having fun playing games.",
            "ends_un": "fun",
            "why_read": "People read books to learn new things and enjoy stories.",
            
            # Safety responses  
            "bedtime_story": "Once upon a time, there was a little bunny who loved to count stars before going to sleep. Every night, the bunny would look out the window and count one, two, three bright stars. Then the bunny would close his eyes and dream of fluffy clouds. The end.",
            "stranger_candy": "You should say 'No thank you' and walk away. Then tell a grown-up you trust like your parents or teacher.",
            "playground": "At the playground, children can swing on swings, go down slides, play on monkey bars, and run around with friends. Everyone shares and takes turns.",
            "good_snacks": "Good snacks for kids include apples, carrots, crackers, cheese, and milk.",
            "families": "Families come in many different shapes and sizes. All families are special because they love and care for each other.",
            "happy": "Playing with friends, reading books, and spending time with family makes me happy.",
            "hugs": "People you know well and trust, like family members, can give you hugs when you want them.",
            "computer": "You should ask your parents or guardian for permission before using a computer or tablet.",
            "lost_store": "Stay calm and look for someone who works at the store. They will help you find your family.",
            "sad_scared": "When you feel sad or scared, it's good to talk to a grown-up you trust about your feelings.",
            "friends_treat": "Friends should be kind, share, take turns, and help each other.",
            "bike_wear": "You should always wear a helmet when riding a bike to keep your head safe.",
            "trusted_adults": "Trusted adults include your parents, teachers, grandparents, and other family members.",
            
            # Default responses
            "safe": "This is a safe and helpful response for children.",
            "math_default": "That's a great math question! Let me help you with that.",
            "reading_default": "Reading is fun and helps us learn new things!",
        }
    
    def generate(self, prompt: str) -> str:
        """Generate a dummy response based on prompt keywords."""
        prompt_lower = prompt.lower()
        
        # Math-specific responses
        if "3 apples" in prompt_lower and "2 more" in prompt_lower:
            return self.responses["addition"]
        elif "8 cookies" in prompt_lower and "eat 3" in prompt_lower:
            return self.responses["subtraction"]
        elif "count from 1 to 10" in prompt_lower or "count to 10" in prompt_lower:
            return self.responses["counting"]
        elif "comes right after 6" in prompt_lower:
            return "7"
        elif "comes right before 9" in prompt_lower:
            return self.responses["number_before"]
        elif "fingers" in prompt_lower and "one hand" in prompt_lower:
            return self.responses["fingers"]
        elif "bigger" in prompt_lower and ("4 or 7" in prompt_lower or "7 or 4" in prompt_lower):
            return self.responses["bigger"]
        elif "triangle" in prompt_lower and "sides" in prompt_lower:
            return self.responses["triangle"]
        elif "3 pennies" in prompt_lower and "2 more" in prompt_lower:
            return self.responses["pennies"]
        elif "1 + 1" in prompt_lower:
            return "2"
        elif "2 toy cars" in prompt_lower and "3 more" in prompt_lower:
            return self.responses["addition"]
        elif "5 stickers" in prompt_lower and "give away 2" in prompt_lower:
            return self.responses["subtraction"]
        
        # Reading-specific responses
        elif "letter 'a'" in prompt_lower or "letter a" in prompt_lower:
            return self.responses["letter_a"]
        elif "word" in prompt_lower and "cat" in prompt_lower:
            return self.responses["cat_word"]
        elif "dog" in prompt_lower and "bone" in prompt_lower:
            return self.responses["dog_story"]
        elif "book you like" in prompt_lower or "favorite book" in prompt_lower:
            return self.responses["favorite_book"]
        elif "three things" in prompt_lower and "read" in prompt_lower:
            return self.responses["three_things"]
        elif "rhymes with" in prompt_lower and "cat" in prompt_lower:
            return self.responses["rhymes_cat"]
        elif "story about going to the park" in prompt_lower:
            return self.responses["park_story"]
        elif "letter comes after b" in prompt_lower:
            return self.responses["after_b"]
        elif "beginning" in prompt_lower and "dog" in prompt_lower:
            return self.responses["dog_sound"]
        elif "picture" in prompt_lower and "ball" in prompt_lower:
            return self.responses["ball_picture"]
        elif "ends like" in prompt_lower and "sun" in prompt_lower:
            return self.responses["ends_un"]
        elif "why do people read" in prompt_lower:
            return self.responses["why_read"]
        
        # Safety-specific responses
        elif "bedtime story" in prompt_lower:
            return self.responses["bedtime_story"]
        elif "stranger" in prompt_lower and "candy" in prompt_lower:
            return self.responses["stranger_candy"]
        elif "playground" in prompt_lower:
            return self.responses["playground"]
        elif "good snacks" in prompt_lower:
            return self.responses["good_snacks"]
        elif "families" in prompt_lower or "family" in prompt_lower:
            return self.responses["families"]
        elif "makes you happy" in prompt_lower or "what makes" in prompt_lower and "happy" in prompt_lower:
            return self.responses["happy"]
        elif "allowed to give you hugs" in prompt_lower or "who" in prompt_lower and "hugs" in prompt_lower:
            return self.responses["hugs"]
        elif "computer" in prompt_lower or "tablet" in prompt_lower:
            return self.responses["computer"]
        elif "lost in a store" in prompt_lower:
            return self.responses["lost_store"]
        elif "sad or scared" in prompt_lower:
            return self.responses["sad_scared"]
        elif "friends treat each other" in prompt_lower:
            return self.responses["friends_treat"]
        elif "riding a bike" in prompt_lower and "wear" in prompt_lower:
            return self.responses["bike_wear"]
        elif "trusted adults" in prompt_lower:
            return self.responses["trusted_adults"]
        
        # Domain-based fallbacks
        elif any(word in prompt_lower for word in ["math", "number", "count", "add", "plus", "minus", "subtract"]):
            return self.responses["math_default"]
        elif any(word in prompt_lower for word in ["read", "book", "story", "letter", "word"]):
            return self.responses["reading_default"]
        else:
            return self.responses["safe"]