from pytest_bdd import given, when, then, parsers
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.entities import Screenshot

client = TestClient(app)

@given("the system is ready to capture a screenshot")
def system_ready():
    pass

@when("I send a request to capture a screenshot")
def send_capture_request():
    response = client.post("/capture")
    assert response.status_code == 200
    return response.json()

@then("I should receive a success response")
def check_success_response(send_capture_request):
    assert send_capture_request["status"] == "success"

@then(parsers.parse("the response should contain a screenshot with a timestamp, text, embedding, and image path"))
def check_screenshot_response(send_capture_request):
    screenshot = send_capture_request["screenshot"]
    assert "timestamp" in screenshot
    assert "text" in screenshot
    assert "embedding" in screenshot
    assert "image_path" in screenshot

@given("the system has captured screenshots")
def system_has_screenshots():
    # Simulate capturing a screenshot
    client.post("/capture")

@when("I send a request to retrieve the timeline")
def send_timeline_request():
    response = client.get("/timeline")
    assert response.status_code == 200
    return response.json()

@then("I should receive a list of screenshots")
def check_timeline_response(send_timeline_request):
    assert isinstance(send_timeline_request["screenshots"], list)

@then(parsers.parse("each screenshot should have a timestamp, text, embedding, and image path"))
def check_each_screenshot(send_timeline_request):
    for screenshot in send_timeline_request["screenshots"]:
        assert "timestamp" in screenshot
        assert "text" in screenshot
        assert "embedding" in screenshot
        assert "image_path" in screenshot
