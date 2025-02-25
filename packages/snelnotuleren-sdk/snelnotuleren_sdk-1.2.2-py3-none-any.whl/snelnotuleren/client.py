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
        meeting_date: str,
        smart_detection: bool,
        webhook_url: str,
        report_type: str = "transcriptie",
        unstructured_agenda: Optional[str] = None,
        # Experimental features
        speaker_diarization: bool = False,
        speaker_count: Optional[int] = None,
        speaker_names: Optional[list] = None,
        verbose: bool = True
    ) -> dict:
        """
        Create a new order and upload an audio file.
        
        Required Args:
            file_path (str): Path to the audio file
            email (str): Email address for notifications
            context (str): Meeting name/context
            meeting_date (str): Meeting date in YYYY-MM-DD format
            smart_detection (bool): Whether to use smart agenda detection.
                If False, unstructured_agenda is required.
            webhook_url (str, optional): URL for webhook notifications
            
        Optional Args:
            report_type (str, optional): Type of report. Defaults to "transcriptie".
                Options: transcriptie, korte_notulen, middel_notulen, lange_notulen
            unstructured_agenda (str, optional): Unstructured agenda text.
                Required if smart_detection is False.
                
        Experimental Features:
            These features are in beta and may change:
            speaker_diarization (bool, optional): Use speaker diarization
            speaker_count (int, optional): Expected number of speakers (1-10)
            speaker_names (list, optional): List of speaker names
        
        Returns:
            dict: Full response data including order ID and payment information if needed
        
        Raises:
            ValueError: If validation fails for any of the parameters
        """
        # Validate smart_detection and unstructured_agenda combination
        if not smart_detection and not unstructured_agenda:
            raise ValueError(
                "Either smart_detection must be True or unstructured_agenda must be provided"
            )
        
        if not self.access_token:
            self.get_token()
            
        if verbose:
            print("1. Creating order...")
            
        # Validate meeting_date format
        try:
            from datetime import datetime
            datetime.strptime(meeting_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("meeting_date must be in YYYY-MM-DD format")
            
        # Validate speaker_count if provided
        if speaker_count is not None:
            if not isinstance(speaker_count, int) or not (1 <= speaker_count <= 10):
                raise ValueError("speaker_count must be an integer between 1 and 10")
                
        # Validate speaker_names if provided
        if speaker_names is not None and not isinstance(speaker_names, list):
            raise ValueError("speaker_names must be a list of strings")
            
        # Prepare order data
        order_data = {
            'fileName': file_path.split('/')[-1],
            'email': email,
            'reportType': report_type,
            'context': context,
            'meeting_date': meeting_date,
            'smart_detection': smart_detection,
            'modelType': 'standard',  # Only model for now
        }
        
        # Add unstructured_agenda if provided
        if unstructured_agenda:
            order_data['unstructured_agenda'] = unstructured_agenda
        
        # Add optional fields
        if webhook_url:
            order_data['webhook_url'] = webhook_url
            
        # Add experimental features if enabled
        if speaker_diarization:
            order_data['useSpeakerDiarization'] = True
            if speaker_count:
                order_data['speakerCount'] = speaker_count
            if speaker_names:
                order_data['speakerNames'] = speaker_names
        
        # Create order
        order_response = self.session.post(
            f"{self.base_url}/api/v1/create-order",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'X-API-Key': self.client_id
            },
            json=order_data
        )
        
        # Accept both 200 and 202 as success
        if order_response.status_code not in [200, 202]:
            raise Exception(f"Order creation failed: Status {order_response.status_code}")
            
        order_data = order_response.json()
        
        # Controleer of betaling vereist is
        payment_required = order_data.get('status') == 'payment_required' or order_data.get('paymentRequired', False)
        
        if verbose:
            print(f"\nOrder created successfully:")
            print(f"Order ID: {order_data['orderId']}")
            print(f"Status: {order_data.get('status', 'processing')}")
            print(f"Upload URL: {order_data.get('uploadUrl')}")
            print(f"Payment Required: {payment_required}")
            
            if payment_required:
                if order_data.get('paymentUrl'):
                    print(f"Payment URL: {order_data['paymentUrl']}")
                else:
                    print("Payment required. Use the pay_for_order method to process payment.")
                    
            if webhook_url:
                print(f"Webhook URL: {webhook_url}")
            print(f"Smart Detection: {'enabled' if smart_detection else 'disabled'}")
            if unstructured_agenda:
                print("Using provided unstructured agenda")
            
            # Log experimental features if used
            if speaker_diarization:
                print("\nExperimental features enabled:")
                print(f"- Speaker diarization: enabled")
                if speaker_count:
                    print(f"- Expected speakers: {speaker_count}")
                if speaker_names:
                    print(f"- Speaker names: {', '.join(speaker_names)}")
        
        # Als betaling vereist is, moeten we niet doorgaan met uploaden
        if payment_required:
            return order_data
        
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
                print(f"Meeting date: {meeting_date}")
                print(f"Smart agenda detection: {'enabled' if smart_detection else 'disabled'}")
            
            # Return full order data instead of just the ID
            return order_data
            
        except Exception as e:
            print(f"Final upload attempt failed: {str(e)}")
            print("\nDebug information:")
            print(f"File size: {len(file_data)} bytes")
            print(f"Order ID: {order_data['orderId']}")
            raise
            
    def upload_file(self, file_path: str, upload_url: str) -> requests.Response:
        """
        Upload a file to the given URL.
        
        Args:
            file_path (str): Path to the file to upload
            upload_url (str): The URL to upload to (from the order response)
            
        Returns:
            requests.Response: The response from the upload
        """
        with open(file_path, 'rb') as f:
            file_data = f.read()
            
        return self._upload_with_retry(upload_url, file_data)
    
    def pay_for_order(self, order_id: str, confirm: bool = True) -> dict:
        """
        Mark an order as paid via the API.
        This is only needed when the order requires payment.
        
        Args:
            order_id (str): The order ID to pay for
            confirm (bool): Explicitly confirm payment (required)
            
        Returns:
            dict: The updated order data
            
        Raises:
            Exception: If payment fails
        """
        if not self.access_token:
            self.get_token()
            
        # Controleer eerst de huidige status
        status = self.check_payment_status(order_id)
        if status.get('status') != 'payment_required':
            return status
            
        # Bevestig de betaling
        payment_response = self.session.post(
            f"{self.base_url}/api/v1/orders/{order_id}/payment",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'X-API-Key': self.client_id
            },
            json={
                'confirm_payment': confirm
            }
        )
        
        if payment_response.status_code not in [200, 202]:
            raise Exception(f"Payment failed: Status {payment_response.status_code}, {payment_response.text}")
            
        return payment_response.json()
        
    def check_payment_status(self, order_id: str) -> dict:
        """
        Check the payment status of an order.
        
        Args:
            order_id (str): The order ID to check
            
        Returns:
            dict: Payment status information
            
        Raises:
            Exception: If the request fails
        """
        if not self.access_token:
            self.get_token()
            
        status_response = self.session.get(
            f"{self.base_url}/api/v1/orders/{order_id}/payment",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'X-API-Key': self.client_id
            }
        )
        
        if status_response.status_code != 200:
            raise Exception(f"Status check failed: Status {status_response.status_code}")
            
        return status_response.json()
        
    def process_order_with_payment(
        self, 
        file_path: str, 
        email: str, 
        context: str,
        meeting_date: str,
        smart_detection: bool,
        webhook_url: str,
        report_type: str = "transcriptie",
        unstructured_agenda: Optional[str] = None,
        speaker_diarization: bool = False,
        speaker_count: Optional[int] = None,
        speaker_names: Optional[list] = None,
        verbose: bool = True,
        auto_pay: bool = True  # Automatically pay if required
    ) -> dict:
        """
        Complete workflow to create an order, handle payment if needed, and upload the file.
        
        Args:
            Same as create_order with the addition of:
            auto_pay (bool): Whether to automatically pay for the order if required
            
        Returns:
            dict: Complete order information
        """
        # Create order and get response
        order_data = self.create_order(
            file_path=file_path,
            email=email,
            context=context,
            meeting_date=meeting_date,
            smart_detection=smart_detection,
            webhook_url=webhook_url,
            report_type=report_type,
            unstructured_agenda=unstructured_agenda,
            speaker_diarization=speaker_diarization,
            speaker_count=speaker_count,
            speaker_names=speaker_names,
            verbose=verbose
        )
        
        # Check if payment is required
        payment_required = order_data.get('status') == 'payment_required' or order_data.get('paymentRequired', False)
        
        if payment_required:
            if not auto_pay:
                print("Payment is required for this order. Call pay_for_order() to proceed.")
                return order_data
                
            # Auto-pay if enabled
            if verbose:
                print("Payment required. Processing automatic payment...")
                
            payment_result = self.pay_for_order(order_data['orderId'])
            
            if verbose:
                print(f"Payment processed: {payment_result.get('message', 'Success')}")
                
            # Now upload the file
            if verbose:
                print("\nUploading file...")
                
            with open(file_path, 'rb') as f:
                file_data = f.read()
                
            upload_response = self._upload_with_retry(
                order_data['uploadUrl'],
                file_data
            )
            
            if verbose:
                print(f"Upload successful! Response code: {upload_response.status_code}")
                print(f"\nComplete! Order ID: {order_data['orderId']}")
                
            # Get updated order status
            order_status = self.check_order_status(order_data['orderId'])
            return order_status
            
        return order_data
        
    def check_order_status(self, order_id: str) -> dict:
        """
        Check the status of an order.
        
        Args:
            order_id (str): The order ID to check
            
        Returns:
            dict: Order status information
        """
        if not self.access_token:
            self.get_token()
            
        status_response = self.session.get(
            f"{self.base_url}/api/v1/orders/{order_id}/status",
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'X-API-Key': self.client_id
            }
        )
        
        if status_response.status_code != 200:
            raise Exception(f"Status check failed: Status {status_response.status_code}")
            
        return status_response.json()