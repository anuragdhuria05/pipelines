#!/usr/bin/env python3
"""
Sample Python code demonstrating various API call patterns.
This module shows how to make HTTP requests to different types of APIs.
"""

import json
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
import urllib.request
import urllib.error


class APIClient:
    """Generic API client with common functionality for making HTTP requests."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session_headers = {
            'User-Agent': 'Python-API-Client/1.0',
            'Content-Type': 'application/json'
        }
        
        if api_key:
            self.session_headers['Authorization'] = f'Bearer {api_key}'
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make HTTP request with error handling and retries."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if params:
            url += '?' + urlencode(params)
        
        request_headers = self.session_headers.copy()
        if headers:
            request_headers.update(headers)
        
        request_data = None
        if data:
            request_data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(
            url=url,
            data=request_data,
            headers=request_headers,
            method=method.upper()
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data) if response_data else {}
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            raise APIException(f"HTTP {e.code}: {e.reason}. Body: {error_body}")
        
        except urllib.error.URLError as e:
            raise APIException(f"URL Error: {e.reason}")
        
        except json.JSONDecodeError as e:
            raise APIException(f"Invalid JSON response: {e}")
        
        except Exception as e:
            raise APIException(f"Request failed: {str(e)}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make GET request."""
        return self._make_request('GET', endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make POST request."""
        return self._make_request('POST', endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Make PUT request."""
        return self._make_request('PUT', endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict:
        """Make DELETE request."""
        return self._make_request('DELETE', endpoint, headers=headers)


class APIException(Exception):
    """Custom exception for API errors."""
    pass


class JSONPlaceholderAPI:
    """Sample client for JSONPlaceholder API (public testing API)."""
    
    def __init__(self):
        self.client = APIClient('https://jsonplaceholder.typicode.com')
    
    def get_posts(self, user_id: Optional[int] = None) -> List[Dict]:
        """Get all posts or posts by specific user."""
        params = {'userId': user_id} if user_id else None
        response = self.client.get('/posts', params=params)
        return response if isinstance(response, list) else [response]
    
    def get_post(self, post_id: int) -> Dict:
        """Get specific post by ID."""
        return self.client.get(f'/posts/{post_id}')
    
    def create_post(self, title: str, body: str, user_id: int) -> Dict:
        """Create new post."""
        data = {
            'title': title,
            'body': body,
            'userId': user_id
        }
        return self.client.post('/posts', data=data)
    
    def update_post(self, post_id: int, title: str, body: str, user_id: int) -> Dict:
        """Update existing post."""
        data = {
            'id': post_id,
            'title': title,
            'body': body,
            'userId': user_id
        }
        return self.client.put(f'/posts/{post_id}', data=data)
    
    def delete_post(self, post_id: int) -> Dict:
        """Delete post."""
        return self.client.delete(f'/posts/{post_id}')
    
    def get_users(self) -> List[Dict]:
        """Get all users."""
        response = self.client.get('/users')
        return response if isinstance(response, list) else [response]


class WeatherAPI:
    """Sample client for OpenWeatherMap API (requires API key)."""
    
    def __init__(self, api_key: str):
        self.client = APIClient('https://api.openweathermap.org/data/2.5')
        self.api_key = api_key
    
    def get_current_weather(self, city: str, units: str = 'metric') -> Dict:
        """Get current weather for a city."""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }
        return self.client.get('/weather', params=params)
    
    def get_forecast(self, city: str, days: int = 5, units: str = 'metric') -> Dict:
        """Get weather forecast for a city."""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units,
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        return self.client.get('/forecast', params=params)


def demo_jsonplaceholder_api():
    """Demonstrate JSONPlaceholder API usage."""
    print("=== JSONPlaceholder API Demo ===")
    
    api = JSONPlaceholderAPI()
    
    try:
        # Get all posts
        print("1. Getting first 5 posts...")
        posts = api.get_posts()[:5]
        for post in posts:
            print(f"  Post {post['id']}: {post['title'][:50]}...")
        
        # Get specific post
        print("\n2. Getting post #1...")
        post = api.get_post(1)
        print(f"  Title: {post['title']}")
        print(f"  Body: {post['body'][:100]}...")
        
        # Create new post
        print("\n3. Creating new post...")
        new_post = api.create_post(
            title="Sample API Test Post",
            body="This post was created using the API client sample code.",
            user_id=1
        )
        print(f"  Created post with ID: {new_post['id']}")
        
        # Get users
        print("\n4. Getting users...")
        users = api.get_users()[:3]
        for user in users:
            print(f"  User {user['id']}: {user['name']} ({user['email']})")
    
    except APIException as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def demo_weather_api():
    """Demonstrate Weather API usage (requires API key)."""
    print("\n=== Weather API Demo ===")
    print("Note: This demo requires an API key from OpenWeatherMap")
    
    # Replace with actual API key for testing
    api_key = "YOUR_API_KEY_HERE"
    
    if api_key == "YOUR_API_KEY_HERE":
        print("Skipping weather API demo - no API key provided")
        return
    
    weather_api = WeatherAPI(api_key)
    
    try:
        # Get current weather
        print("1. Getting current weather for London...")
        weather = weather_api.get_current_weather("London")
        print(f"  Temperature: {weather['main']['temp']}°C")
        print(f"  Description: {weather['weather'][0]['description']}")
        print(f"  Humidity: {weather['main']['humidity']}%")
        
        # Get forecast
        print("\n2. Getting 3-day forecast for New York...")
        forecast = weather_api.get_forecast("New York", days=3)
        print(f"  Forecast entries: {len(forecast['list'])}")
        
    except APIException as e:
        print(f"Weather API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def demo_rate_limiting():
    """Demonstrate handling rate-limited APIs."""
    print("\n=== Rate Limiting Demo ===")
    
    api = JSONPlaceholderAPI()
    
    print("Making multiple rapid requests...")
    for i in range(1, 6):
        try:
            post = api.get_post(i)
            print(f"  Request {i}: Got post '{post['title'][:30]}...'")
            time.sleep(0.1)  # Small delay to be respectful
        except APIException as e:
            print(f"  Request {i}: Failed - {e}")


def demo_error_handling():
    """Demonstrate error handling patterns."""
    print("\n=== Error Handling Demo ===")
    
    api = JSONPlaceholderAPI()
    
    # Test with invalid endpoint
    try:
        api.client.get('/nonexistent-endpoint')
    except APIException as e:
        print(f"Expected error for invalid endpoint: {e}")
    
    # Test with invalid post ID
    try:
        api.get_post(99999)  # Very high ID that likely doesn't exist
        print("Post retrieved successfully (or API returns empty response)")
    except APIException as e:
        print(f"Error retrieving non-existent post: {e}")


if __name__ == "__main__":
    """Run all demonstrations."""
    print("API Client Sample Code")
    print("=" * 50)
    
    # Run demonstrations
    demo_jsonplaceholder_api()
    demo_weather_api()
    demo_rate_limiting()
    demo_error_handling()
    
    print("\n" + "=" * 50)
    print("Sample completed successfully!")
    print("\nTo use this code:")
    print("1. Install required packages: pip install urllib3 (built-in)")
    print("2. For weather API: Get API key from https://openweathermap.org/api")
    print("3. Replace 'YOUR_API_KEY_HERE' with your actual API key")
    print("4. Run: python api_client_sample.py")