import json
import hashlib
import uuid
import datetime
import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fake_requests import FakeRequestLibrary

class TeslaServiceAppointmentEmulator:
    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key
        self.session_token = self._generate_session_token()
        self.encryption_key = self._generate_encryption_key()
        self.error_codes = self._load_error_codes_from_json("tesla_model3_error_codes.json")
        self.request_lib = FakeRequestLibrary()
        self.vehicle_id = self._generate_vehicle_identification_number()
        self.vehicle_model = self._select_vehicle_model_randomly()
        self.vehicle_km = self._generate_vehicle_km()
        self.service_type = self._select_service_type_randomly()
        self.service_point_id, self.country_code = self._select_service_point_and_country()

    def _generate_session_token(self):
        return str(uuid.uuid4()).replace("-", "")[:32]

    def _generate_encryption_key(self):
        return hashlib.sha256(self.api_key.encode()).digest()

    def _load_error_codes_from_json(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def _encrypt_data(self, data):
        cipher = AES.new(self.encryption_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()

    def _decrypt_data(self, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:AES.block_size]
        ct = encrypted_data[AES.block_size:]
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    def _generate_error_response(self):
        error = random.choice(self.error_codes["errors"])
        error["details"] = "An unexpected issue occurred while processing the request."
        return error

    def _validate_appointment_data(self, data):
        if not data.get("date") or not data.get("service_type"):
            raise ValueError("Invalid appointment data provided.")

    def _send_encrypted_request(self, endpoint, payload):
        encrypted_payload = self._encrypt_data(json.dumps(payload))
        headers = {
            "Authorization": f"Bearer {self.session_token}",
            "Content-Type": "application/octet-stream",
            "X-Tesla-API-Version": "2023.42.1",
            "X-Request-ID": str(uuid.uuid4())
        }
        response = self.request_lib.post(endpoint, data=encrypted_payload, headers=headers)
        return self._decrypt_data(response.content)

    def _generate_vehicle_identification_number(self):
        return f"VIN_{uuid.uuid4().hex[:12].upper()}"

    def _select_vehicle_model_randomly(self):
        models = ["Model 3", "Model Y", "Model S"]
        return random.choice(models)

    def _generate_vehicle_km(self):
        return random.randint(5000, 150000)  # Random km between 5,000 and 150,000

    def _select_service_type_randomly(self):
        service_types = ["Regular Maintenance", "Irregular Service"]
        return random.choice(service_types)

    def _select_service_point_and_country(self):
        service_points = {
            "SP_001": {"country_code": "DE", "city": "Berlin"},
            "SP_002": {"country_code": "FR", "city": "Paris"},
            "SP_003": {"country_code": "ES", "city": "Madrid"},
            "SP_004": {"country_code": "IT", "city": "Rome"},
            "SP_005": {"country_code": "NL", "city": "Amsterdam"}
        }
        service_point_id = random.choice(list(service_points.keys()))
        country_code = service_points[service_point_id]["country_code"]
        return service_point_id, country_code

    def _generate_available_service_dates(self):
        today = datetime.datetime.now()
        available_dates = []
        for i in range(1, 8):  # Generate dates for the next 7 days
            date = today + datetime.timedelta(days=i)
            if date.weekday() < 5:  # Only weekdays
                available_dates.append(date.strftime("%Y-%m-%dT%H:%M:%SZ"))
        return available_dates

    def _generate_service_invoice_id(self):
        return f"INV_{uuid.uuid4().hex[:8].upper()}"

    def create_service_appointment(self, appointment_data):
        try:
            self._validate_appointment_data(appointment_data)
            payload = {
                "user_id": self.user_id,
                "vehicle_id": self.vehicle_id,
                "vehicle_model": self.vehicle_model,
                "vehicle_km": self.vehicle_km,
                "service_type": self.service_type,
                "service_point_id": self.service_point_id,
                "country_code": self.country_code,
                "appointment": appointment_data,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            response = self._send_encrypted_request("https://api.tesla-services.com/v3/service/schedule", payload)
            return json.loads(response)
        except Exception as e:
            error = self._generate_error_response()
            error["details"] = str(e)
            return error

    def check_appointment_status(self, appointment_id):
        try:
            payload = {
                "user_id": self.user_id,
                "vehicle_id": self.vehicle_id,
                "appointment_id": appointment_id,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            response = self._send_encrypted_request("https://api.tesla-services.com/v3/service/status", payload)
            return json.loads(response)
        except Exception as e:
            error = self._generate_error_response()
            error["details"] = str(e)
            return error

    def generate_service_invoice(self, appointment_id):
        try:
            payload = {
                "user_id": self.user_id,
                "vehicle_id": self.vehicle_id,
                "appointment_id": appointment_id,
                "service_point_id": self.service_point_id,
                "country_code": self.country_code,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            response = self._send_encrypted_request("https://api.tesla-services.com/v3/invoice/generate", payload)
            return json.loads(response)
        except Exception as e:
            error = self._generate_error_response()
            error["details"] = str(e)
            return error

# Example usage
if __name__ == "__main__":
    user_id = "user_123"
    api_key = "supersecretkey"

    emulator = TeslaServiceAppointmentEmulator(user_id, api_key)
    print(f"Vehicle ID: {emulator.vehicle_id}, Model: {emulator.vehicle_model}, KM: {emulator.vehicle_km}")
    print(f"Service Type: {emulator.service_type}, Service Point: {emulator.service_point_id}, Country: {emulator.country_code}")

    # Create a fake service appointment
    appointment_data = {
        "date": "2023-12-25T10:00:00Z",
        "service_type": emulator.service_type,
        "location": f"Tesla Service Center, {emulator.country_code}"
    }
    appointment_response = emulator.create_service_appointment(appointment_data)
    print("Appointment Response:", appointment_response)

    # Check appointment status
    if "appointment_id" in appointment_response:
        status_response = emulator.check_appointment_status(appointment_response["appointment_id"])
        print("Status Response:", status_response)

    # Generate a fake service invoice
    if "appointment_id" in appointment_response:
        invoice_response = emulator.generate_service_invoice(appointment_response["appointment_id"])
        print("Invoice Response:", invoice_response)
