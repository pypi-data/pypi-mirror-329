from qubicon import QubiconCore

# Mock client with necessary attributes
class MockClient:
    def __init__(self):
        self.base_url = "https://master.qub-lab.io"
        self.token = None

mock_client = MockClient()
core = QubiconCore(client=mock_client)

print("\n--- Testing login_user ---")
try:
    token = core.login_user(username="qubiconClient", password="qubiconClient1!")
    print("Token:", token)
except Exception as e:
    print(f"login_user failed: {e}")

