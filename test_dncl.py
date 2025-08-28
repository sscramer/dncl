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

# --- Main Test Function ---
@pytest.mark.parametrize("program_name, expected_output", TEST_CASES)
def test_dncl_program(program_name: str, expected_output: str, page: Page, http_server: str):
    """
    Tests a DNCL program by loading its XML, running it, and checking the output.
    """
    xml_file_path = os.path.join(os.getcwd(), "sampleprograms", f"{program_name}.xml")

    page.goto(f"{http_server}/index.html")

    import_input = page.locator("#importFile")

    import_input.set_input_files(xml_file_path)

    page.locator("#runButton").click()

    status_div = page.locator("#runStatusDiv")
    expect(status_div).to_have_text("プログラム終了", timeout=15000)

    output_div = page.locator("#outputDiv")
    expect(output_div).to_have_text(expected_output + "\n", timeout=1000)
