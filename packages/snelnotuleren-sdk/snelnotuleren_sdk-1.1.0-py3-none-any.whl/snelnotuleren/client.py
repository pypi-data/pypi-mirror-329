# snelnotuleren/client.py
import requests
import os

class SnelNotulerenClient:
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.snelnotuleren.nl/api/v1"
        self._access_token = None

    def create_client_credentials(self, label, description):
        """
        Maak nieuwe API credentials aan.
        
        Args:
            label (str): Label voor de credentials
            description (str): Beschrijving voor de credentials
            
        Returns:
            dict: Dictionary met client_id, client_secret en webhook_secret
        """
        response = requests.post(
            f"{self.base_url}/create-client-credentials",
            json={
                "label": label,
                "description": description
            }
        )
        response.raise_for_status()
        return response.json()

    def create_order(self, file_path, email, context, webhook_url=None, **kwargs):
        """
        Maak een nieuwe order aan voor notulen verwerking.
        
        Args:
            file_path (str): Pad naar het audio bestand
            email (str): Email adres voor notificaties
            context (str): Context/naam van de vergadering
            webhook_url (str, optional): URL waar webhook notificaties naartoe gestuurd worden
            **kwargs: Extra parameters zoals:
                - report_type: Type rapport ('transcriptie', 'korte_notulen', etc.)
                - model_type: Type model ('standard')
                - speaker_diarization: Of sprekerherkenning gebruikt moet worden (bool)
                - speaker_count: Verwacht aantal sprekers (int)
                
        Returns:
            str: Order ID
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get access token
        if not self._access_token:
            self._access_token = self._get_access_token()

        # Prepare order data
        order_data = {
            "fileName": os.path.basename(file_path),
            "email": email,
            "context": context,
            "modelType": kwargs.get("model_type", "standard"),
            "reportType": kwargs.get("report_type", "transcriptie"),
            "useSpeakerDiarization": kwargs.get("speaker_diarization", False),
            "speakerCount": kwargs.get("speaker_count", 1)
        }

        # Add webhook URL if provided
        if webhook_url:
            order_data["webhook_url"] = webhook_url

        # Create order
        response = requests.post(
            f"{self.base_url}/create-order",
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "X-API-Key": self.client_id
            },
            json=order_data
        )
        response.raise_for_status()
        result = response.json()

        # Upload file
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                result["uploadUrl"],
                data=f.read(),
                headers={"Content-Type": "audio/mpeg"}
            )
            upload_response.raise_for_status()

        return result["orderId"]

    def _get_access_token(self):
        """Get access token using client credentials"""
        response = requests.post(
            f"{self.base_url}/auth/token",
            headers={
                "X-Client-ID": self.client_id,
                "X-Client-Secret": self.client_secret
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]