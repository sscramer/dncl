import os
from playwright.sync_api import sync_playwright, expect

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to index.html
        file_path = os.path.abspath('index.html')
        page.goto(f'file://{file_path}')

        # XML for a simple program with only a function definition
        xml_string = """
        <xml xmlns="https://developers.google.com/blockly/xml">
          <block type="procedures_defnoreturn" id="g`_K7L_~r;a#*@Vz{/DB" x="213" y="113">
            <field name="NAME">my_function</field>
            <statement name="STACK">
              <block type="simple_display" id="=z+1kS2@8)zS@C3+;!A*">
                <field name="NEWLINE">TRUE</field>
                <value name="VALUE">
                  <block type="string_literal" id="5!^Y|Vb+sL%L52w(R3p*">
                    <field name="TEXT">Hello from function</field>
                  </block>
                </value>
              </block>
            </statement>
          </block>
        </xml>
        """

        # Use page.evaluate to load the XML into the Blockly workspace
        page.evaluate("""
          (xmlString) => {
            const xml = Blockly.utils.xml.textToDom(xmlString);
            workspace.clear();
            Blockly.Xml.domToWorkspace(xml, workspace);
          }
        """, xml_string)

        # Select Python from the dropdown
        page.locator("#languageSelector").select_option("Python")

        # Click the "Show Code" button
        page.locator("#showCodeButton").click()

        # Wait for the modal to be visible
        modal_body = page.locator("#jsCodeDiv")
        expect(modal_body).to_be_visible()

        # Check if the generated code contains Python syntax for the function definition
        expect(modal_body).to_contain_text("def my_function():")
        expect(modal_body).to_contain_text("print('Hello from function')")

        # Take a screenshot of the modal
        page.locator("#codeModal .modal-content").screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run_test()
