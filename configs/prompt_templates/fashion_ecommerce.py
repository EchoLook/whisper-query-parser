"""
Prompt templates for fashion e-commerce query generation.

This module contains specialized prompts for processing transcribed text 
related to fashion products and generating structured queries.
"""

# Base fashion e-commerce prompt template
FASHION_ECOMMERCE_TEMPLATE = """
Transform the following transcribed speech into a structured query for a fashion e-commerce API.
The result should be a simple JSON object that captures the key product requirements.

Guidelines:
1. For clothing items, extract: product type, color, price range, size, and any other relevant attributes.
2. If the user mentions modifications to items shown in the image, make those changes explicit in the query.
3. If the user mentions relative pricing (e.g., "cheap", "affordable", "expensive"), convert to approximate price ranges.
4. Capture style descriptions (e.g., "casual", "formal", "vintage") as attributes.
5. If multiple items are mentioned, include them as separate entries in an "items" array.
6. Focus only on actionable shopping criteria and ignore conversational elements.

Transcribed text: {transcript}

Return ONLY a valid JSON object with no additional explanation or text.
"""

# Product-specific templates
CLOTHING_TEMPLATE = """
Transform the following transcribed speech about clothing into a structured query for a fashion e-commerce API.
The result should be a simple JSON object that captures the key clothing requirements.

For clothing items, extract and structure the following information if mentioned:
- product_type: The specific type of clothing (e.g., "shirt", "dress", "jeans")
- color: Preferred color(s)
- price_range: Convert mentions like "cheap" to {"min": 0, "max": 30}
- size: Any size specifications
- material: Fabric preferences (e.g., "cotton", "silk")
- style: Style descriptions (e.g., "casual", "formal")
- fit: Fit preferences (e.g., "slim", "loose", "regular")
- brand: Any mentioned brands
- occasion: What the item is for (e.g., "work", "party")

If the user mentions modifications to items shown in the image, prioritize those changes in the query.
If multiple items are mentioned, include them as separate entries in an "items" array.

Transcribed text: {transcript}

Return ONLY a valid JSON object with no additional explanation or text.
"""

# Sample expected output format
SAMPLE_OUTPUT = {
    "items": [
        {
            "product_type": "shirt",
            "color": "blue",
            "price_range": {
                "min": 0,
                "max": 30
            },
            "size": "medium",
            "material": "cotton",
            "style": "casual"
        }
    ],
    "preferences": {
        "sort_by": "price_low_to_high",
        "show_only_available": True
    }
} 