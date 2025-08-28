import pytest
import http.server
import socketserver
import threading
import os
from playwright.sync_api import Page, expect

# --- Test Data ---
TEST_CASES = [
    ("01_sum", "150"),
    ("02_factorial", "3628800"),
    ("03_fibonacci", "610"),
    ("04_gcd", "6"),
    ("05_prime", "Prime"),
    ("06_linear_search", "2"),
    ("07_binary_search", "2"),
    ("08_bubble_sort", "25,45,72,87,100"),
    ("09_string_reversal", "o,l,l,e,h"),
    ("10_change_making", "8"),
]

# --- HTTP Server Fixture ---
@pytest.fixture(scope="session", autouse=True)
def http_server():
    PORT = 8000

    # SimpleHTTPRequestHandler serves files from the current directory
    Handler = http.server.SimpleHTTPRequestHandler

    # The server needs to be created in a way that allows port reuse
    # This prevents "address already in use" errors on subsequent test runs
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), Handler)

    print(f"Serving at port {PORT}")

    # Run the server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True  # Allows main thread to exit even if server is running
    server_thread.start()

    # Yield the URL to the tests
    yield f"http://localhost:{PORT}"

    # Teardown: stop the server
    print("\nShutting down http server...")
    httpd.shutdown()
    httpd.server_close()
    server_thread.join()

# --- Main Test Function ---
@pytest.mark.parametrize("program_name, expected_output", TEST_CASES)
def test_dncl_program(program_name: str, expected_output: str, page: Page, http_server: str):
    """
    Tests a DNCL program by loading its XML, running it, and checking the output.
    """
    # Construct the full path to the XML file
    xml_file_path = os.path.join(os.getcwd(), "programs", f"{program_name}.xml")

    # Navigate to the simulator page
    page.goto(f"{http_server}/index.html")

    # Locate the hidden file input element
    import_input = page.locator("#importFile")

    # Upload the XML file
    import_input.set_input_files(xml_file_path)

    # Click the "Run" button
    page.locator("#runButton").click()

    # Wait for the status to indicate completion
    status_div = page.locator("#runStatusDiv")
    # Wait for either success, error, or timeout, with a generous timeout
    expect(status_div).to_have_text("プログラム終了", timeout=15000)

    # Get the output and normalize it
    output_div = page.locator("#outputDiv")
    # The output div might have trailing newlines, so we strip them
    expect(output_div).to_have_text(expected_output + "\n", timeout=1000)

    # An alternative check that is more robust to whitespace:
    # actual_text = output_div.inner_text().strip()
    # assert actual_text == expected_output
