from datetime import datetime, timedelta
import pytest
from hydroq_api import (
    HydroQuebec, 
    AUTHORIZE_URL,
    AUTH_URL,
    AUTH_URL_COMB,
    TOKEN_URL,
    RELATION_URL,
    CONTRACT_SUMMARY_URL,
    SESSION_URL,
    PORTRAIT_URL
)

@pytest.fixture
def hydro_client():
    return HydroQuebec("test@example.com", "password123")

@pytest.mark.parametrize("username,password,expected_status", [
    ("test@example.com", "validpass", True),
    ("invalid@example.com", "wrongpass", False),
    ("", "", False),
])
def test_login(username, password, expected_status, requests_mock):
    client = HydroQuebec(username, password)
    
    # Mock the exact endpoints used in the login flow
    requests_mock.get(AUTHORIZE_URL, text='{"csrf":"test_csrf","transId":"test_trans"}')
    requests_mock.post(AUTH_URL, json={"status": "success"})
    requests_mock.get(AUTH_URL_COMB, headers={"location": "callback?code=test_code"})
    requests_mock.post(TOKEN_URL, json={
        "id_token": "test_id_token",
        "access_token": "test_access_token",
        "refresh_token": "test_refresh",
        "expires_in": 3600,
        "refresh_token_expires_in": 7200
    })
    requests_mock.get(RELATION_URL, json=[{
        "noPartenaireDemandeur": "test_applicant",
        "noPartenaireTitulaire": "test_customer"
    }])
    
    client.login()
    assert client.access_token == "test_access_token"

def test_token_refresh(hydro_client, requests_mock):
    requests_mock.post(TOKEN_URL, json={
        "id_token": "new_test_token",
        "access_token": "new_access_token",
        "refresh_token": "new_refresh",
        "expires_in": 3600,
        "refresh_token_expires_in": 7200
    })
    
    hydro_client.refresh_token = "initial_refresh_token"
    result = hydro_client._refresh_token()
    
    assert result is True
    assert hydro_client.access_token == "new_access_token"
    assert hydro_client.refresh_token == "new_refresh"

def test_requires_web_session(hydro_client, requests_mock):
    # Mock the endpoints used in web session creation
    requests_mock.get(CONTRACT_SUMMARY_URL, json={
        "comptesContrats": [{
            "listeNoContrat": ["123456789"]
        }]
    })
    requests_mock.get(SESSION_URL, json={"status": "success"})
    requests_mock.get(PORTRAIT_URL, json={"status": "success"})
    requests_mock.post(TOKEN_URL, json={
        "id_token": "new_test_token",
        "access_token": "new_access_token",
        "refresh_token": "new_refresh",
        "expires_in": 3600,
        "refresh_token_expires_in": 7200
    })

    # Create a test method with the decorator
    @HydroQuebec.requires_web_session
    def test_method(self):
        return "success"
    
    # First call - should create new session
    hydro_client.access_token = "mock_access_token"
    hydro_client.applicant_id = "test_applicant"
    hydro_client.customer_id = "test_customer"
    result1 = test_method(hydro_client)
    first_session_time = hydro_client._session_created_at
    
    # Call within 5 minutes - should use same session
    result2 = test_method(hydro_client)
    assert first_session_time == hydro_client._session_created_at
    
    # Simulate time passing (5 minutes)
    hydro_client._session_created_at = datetime.now() - timedelta(minutes=6)
    
    # Call after 5 minutes - should create new session
    result3 = test_method(hydro_client)
    assert first_session_time != hydro_client._session_created_at
    assert result1 == result2 == result3 == "success"