"""
Tests for the query generation module.
"""
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from utils.query_generation import QueryGenerator


class TestQueryGenerator:
    """Test class for the QueryGenerator implementation."""
    
    @pytest.fixture
    def mock_env_api_key(self):
        """Fixture to set a mock API key in environment variables."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake_api_key"}):
            yield
    
    @pytest.fixture
    def mock_genai(self):
        """Fixture to mock the Google GenerativeAI library responses."""
        with patch("google.generativeai.configure") as mock_configure:
            with patch("google.generativeai.GenerativeModel") as mock_model_class:
                mock_model = MagicMock()
                mock_model_class.return_value = mock_model
                
                # Set up response for the mock model
                mock_response = MagicMock()
                mock_response.text = json.dumps({
                    "items": [
                        {
                            "product_type": "shirt",
                            "color": "blue",
                            "price_range": {"min": 0, "max": 20}
                        }
                    ]
                })
                mock_model.generate_content.return_value = mock_response
                
                yield mock_model
    
    def test_initialization_with_env_key(self, mock_env_api_key, mock_genai):
        """Test initialization with environment API key."""
        generator = QueryGenerator()
        assert generator.api_key == "fake_api_key"
    
    def test_initialization_with_provided_key(self, mock_genai):
        """Test initialization with provided API key."""
        generator = QueryGenerator(api_key="provided_key")
        assert generator.api_key == "provided_key"
    
    def test_initialization_no_key(self):
        """Test initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                QueryGenerator()
            assert "Google API key not found" in str(exc_info.value)
    
    def test_generate_query_successful(self, mock_env_api_key, mock_genai):
        """Test successful query generation from transcript."""
        generator = QueryGenerator()
        transcript = "me gusta el conjunto pero quiero una camiseta azul en vez de rosa y me gustaria que fuera barata"
        
        result = generator.generate_query(transcript)
        
        # Verify the mock was called correctly
        mock_genai.generate_content.assert_called_once()
        
        # Check that the result is a dictionary with expected structure
        assert isinstance(result, dict)
        assert "items" in result
        assert len(result["items"]) == 1
        assert result["items"][0]["product_type"] == "shirt"
        assert result["items"][0]["color"] == "blue"
    
    def test_generate_query_with_image(self, mock_env_api_key, mock_genai):
        """Test query generation with image input."""
        generator = QueryGenerator()
        transcript = "el vestido es chulo pero no me convence, vamos a probar con unos vaqueros y una camiseta del mismo color"
        
        # Create a mock image path
        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = True
            with patch("PIL.Image.open") as mock_open:
                mock_img = MagicMock()
                mock_open.return_value = mock_img
                
                result = generator.generate_query(transcript, "mock_image.jpg")
                
                # Verify the mock was called with both text and image
                assert mock_genai.generate_content.call_count == 1
                args = mock_genai.generate_content.call_args[0][0]
                assert len(args) == 2  # Should have text and image
    
    def test_generate_query_error_handling(self, mock_env_api_key, mock_genai):
        """Test error handling during query generation."""
        generator = QueryGenerator()
        transcript = "test transcript"
        
        # Make the mock raise an exception
        mock_genai.generate_content.side_effect = Exception("API error")
        
        result = generator.generate_query(transcript)
        
        # Verify that we get an error result
        assert "error" in result
        assert "Failed to generate query" in result["error"]
        assert result["transcript"] == transcript 