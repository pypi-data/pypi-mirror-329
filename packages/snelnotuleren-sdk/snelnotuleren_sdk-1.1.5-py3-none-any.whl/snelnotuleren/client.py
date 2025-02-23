import requests
from typing import Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

class SnelNotulerenClient:
    """
    Official Python client for the Snelnotuleren API.
    
    Args:
        client_id (str): Your client ID
        client_secret (str): Your client secret
        base_url (str, optional): API base URL. Defaults to production API.
    """
    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.snelnotuleren.nl"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.access_token = None
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retries = Retry(
            total=5,  # Total number of retries
            backoff_factor=0.5,  # Wait 0.5, 1, 2, 4, 8 seconds between retries
            status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
            allowed_methods=["GET", "POST", "PUT"]  # Allow retries on these methods
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
    def get_token(self) -> str:
        """
        Get an access token using client credentials.
        
        Returns:
            str: The access token
            
        Raises:
            Exception: If token request fails
        """
        response = requests.post(
            f"{self.base_url}/api/v1/auth/token",
            headers={
                'X-Client-ID': self.client_id,
                'X-Client-Secret': self.client_secret
            }
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        else:
            raise Exception(f"Token request failed: {response.text}")
        
    def _upload_with_retry(self, url: str, file_data: bytes, max_attempts: int = 3) -> requests.Response:
        """Upload with retry logic for SSL errors"""
        attempt = 0
        last_error = None
        
        while attempt < max_attempts:
            try:
                response = self.session.put(
                    url,
                    data=file_data,
                    headers={'Content-Type': 'application/octet-stream'}
                )
                
                # Log response details for debugging
                print(f"Upload attempt {attempt + 1} status: {response.status_code}")
                if response.status_code != 200:
                    print(f"Response text: {response.text}")
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.SSLError as e:
                last_error = e
                attempt += 1
                if attempt < max_attempts:
                    wait_time = 2 ** attempt
                    print(f"SSL error on attempt {attempt}, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"SSL error on final attempt: {str(e)}")
                    raise
                    
            except requests.exceptions.RequestException as e:
                print(f"Upload error: {str(e)}")
                if hasattr(e.response, 'text'):
                    print(f"Error response: {e.response.text}")
                raise

    def create_order(
        self, 
        file_path: str, 
        email: str, 
        context: str, 
        webhook_url: Optional[str] = None,
        report_type: str = "transcriptie",
        verbose: bool = True
    ) -> str:
        """
        Create a new order and upload an audio file.
        
        Args:
            file_path (str): Path to the audio file
            email (str): Email address for notifications
            context (str): Meeting context/name
            webhook_url (str, optional): URL for webhook notifications
            report_type (str, optional): Type of report. Defaults to "transcriptie".
                Options: transcriptie, korte_notulen, middel_notulen, lange_notulen
            verbose (bool, optional): Whether to print progress. Defaults to True.
            
        Returns:
            str: The order ID
            
        Raises:
            Exception: If order creation or file upload fails
        """
        if not self.access_token:
            self.get_token()
            
        if verbose:
            print("1. Creating order...")
            
        # Prepare order data
        order_data = {
            'fileName': file_path.split('/')[-1],
            'email': email,
            'modelType': 'standard',
            'reportType': report_type,
            'context': context
        }
        
        if webhook_url:
            order_data['webhook_url'] = webhook_url
            
        # Create order
        order_response = self.session.post(
            f"{self.base_url}/api/v1/create-order",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'X-API-Key': self.client_id
            },
            json=order_data
        )
        
        if order_response.status_code != 200:
            raise Exception(f"Order creation failed: {order_response.text}")
            
        order_data = order_response.json()
        
        if verbose:
            print(f"\nOrder created successfully:")
            print(f"Order ID: {order_data['orderId']}")
            print(f"Payment Required: {order_data.get('paymentRequired', False)}")
            if order_data.get('paymentUrl'):
                print(f"Payment URL: {order_data['paymentUrl']}")
            if webhook_url:
                print(f"Webhook URL: {webhook_url}")
        
        if verbose:
            print("\n2. Uploading file...")
            
        # Read file once to avoid multiple reads on retry
        with open(file_path, 'rb') as f:
            file_data = f.read()
            
        # Upload with retry
        try:
            upload_response = self._upload_with_retry(
                order_data['uploadUrl'],
                file_data
            )
            
            if verbose:
                print(f"Upload successful! Response code: {upload_response.status_code}")
                print(f"\nComplete! Order ID: {order_data['orderId']}")
                if webhook_url:
                    print(f"You will receive updates at: {webhook_url}")
            
            return order_data['orderId']
            
        except Exception as e:
            print(f"Final upload attempt failed: {str(e)}")
            print("\nDebug information:")
            print(f"File size: {len(file_data)} bytes")
            print(f"Order ID: {order_data['orderId']}")
            raise