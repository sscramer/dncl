import pytest
import http.server
import socketserver
import threading
import os
from playwright.sync_api import Page, expect, Dialog

# --- HTTP Server Fixture ---
@pytest.fixture(scope="session", autouse=True)
def http_server():
    PORT = 8001  # Use a different port to avoid conflict with the other test file

    # SimpleHTTPRequestHandler serves files from the current directory
    Handler = http.server.SimpleHTTPRequestHandler

    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print(f"Serving at port {PORT}")

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield f"http://localhost:{PORT}"

    print("\nShutting down http server...")
    httpd.shutdown()
    httpd.server_close()
    server_thread.join()

# --- Test Function ---
def test_input_after_output(page: Page, http_server: str):
    """
    Tests that output is rendered before an input prompt appears.
    """
    xml_file_path = os.path.join(os.getcwd(), "test-programs", "input_after_output.xml")

    # Set up a handler for the prompt dialog
    def handle_dialog(dialog: Dialog):
        assert dialog.message == "外部からの入力"
        dialog.accept("Jules")

    page.on("dialog", handle_dialog)

    page.goto(f"{http_server}/index.html")

    # Load the XML file
    page.locator("#importFile").set_input_files(xml_file_path)

    # Click the run button
    page.locator("#runButton").click()

    # Wait for the program to finish
    status_div = page.locator("#runStatusDiv")
    expect(status_div).to_have_text("プログラム終了", timeout=15000)

    # Check the final output
    output_div = page.locator("#outputDiv")
    expected_text = "What is your name?Hello, Jules"
    expect(output_div).to_contain_text(expected_text, timeout=1000)
