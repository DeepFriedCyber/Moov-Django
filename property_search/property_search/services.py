# property_search/services.py

import json
import openai
from django.conf import settings

class OpenAIService:
    """Service for interacting with OpenAI API for natural language property search."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def extract_search_parameters(self, query_text):
        """
        Extract search parameters from natural language query using OpenAI.
        
        Args:
            query_text (str): The user's natural language search query
            
        Returns:
            dict: Extracted search parameters
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4", # You can change this to "gpt-3.5-turbo" for lower cost
                messages=[
                    {
                        "role": "system",
                        "content": """You are a property search assistant. Extract search parameters from the user's query.
                        Return a JSON object with the following fields if mentioned:
                        - location: The city or area name
                        - property_type: Type of property (flat, house, bungalow, etc.)
                        - min_bedrooms: Minimum number of bedrooms
                        - max_bedrooms: Maximum number of bedrooms
                        - min_price: Minimum price in GBP
                        - max_price: Maximum price in GBP
                        - has_garden: Boolean indicating if garden is required
                        - has_parking: Boolean indicating if parking is required
                        - keyword: Any specific feature mentioned (e.g., "modern", "renovated")
                        
                        Only include fields that are explicitly or implicitly mentioned in the query.
                        If a range is given (e.g., "2-3 bedrooms"), set both min and max.
                        If only a single value is given (e.g., "3 bedrooms"), set only the min value.
                        Return valid JSON only, no explanation text."""
                    },
                    {
                        "role": "user",
                        "content": query_text
                    }
                ],
                temperature=0.1,
            )
            
            # Extract and parse the JSON from the response
            content = response.choices[0].message.content.strip()
            
            # Handle case where response might have markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].strip()
                
            return json.loads(content)
            
        except Exception as e:
            # Log error and return empty dict if parsing fails
            print(f"Error extracting search parameters: {str(e)}")
            return {}
    
    def generate_search_summary(self, query_text, properties, extracted_params):
        """
        Generate a natural language summary of search results.
        
        Args:
            query_text (str): The original search query
            properties (list): List of property objects that matched
            extracted_params (dict): The parameters extracted from the query
            
        Returns:
            str: Natural language summary of the search results
        """
        try:
            property_count = len(properties)
            
            if property_count == 0:
                prompt = f"""User query: "{query_text}"
                Parameters extracted: {json.dumps(extracted_params)}
                No properties match these criteria.
                Please provide a helpful response explaining that no properties were found and suggest
                how they might broaden their search."""
            else:
                # Create a summary of the properties found
                property_summaries = []
                for i, prop in enumerate(properties[:5]):  # Limit to first 5 for API efficiency
                    property_summaries.append(
                        f"Property {i+1}: {prop.title}, {prop.bedrooms} bed, "
                        f"£{prop.price}, {prop.location.name}, {prop.property_type.name}"
                    )
                
                properties_text = "\n".join(property_summaries)
                
                prompt = f"""User query: "{query_text}"
                Parameters extracted: {json.dumps(extracted_params)}
                {property_count} properties found. Here are some examples:
                {properties_text}
                
                Please provide a helpful summary of the search results in 2-3 sentences.
                Don't list all properties, just mention the number found and highlight key similarities."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Using cheaper model for summaries
                messages=[
                    {"role": "system", "content": "You are a helpful property assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Log error and return basic message if generation fails
            print(f"Error generating search summary: {str(e)}")
            return f"Found {len(properties)} properties matching your search criteria."