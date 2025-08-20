import os
from playwright.sync_api import sync_playwright, expect

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get the absolute path to index.html
        file_path = os.path.abspath('index.html')
        page.goto(f'file://{file_path}')

        # XML for a for loop
        xml_string = """
        <xml xmlns="https://developers.google.com/blockly/xml">
          <block type="for_loop" id="f(Sg|B@jB*h6l6]B]P@," x="163" y="113">
            <field name="VAR">i</field>
            <value name="FROM">
              <shadow type="number_literal" id="~+f},i^C65I#pI=qYk~D">
                <field name="NUM">1</field>
              </shadow>
            </value>
            <value name="TO">
              <shadow type="number_literal" id="5S~2s#B!p5]4k;!zYkE/">
                <field name="NUM">10</field>
              </shadow>
            </value>
            <value name="STEP">
              <shadow type="number_literal" id="V-y167E-C+D@#5M3=z#q">
                <field name="NUM">1</field>
              </shadow>
            </value>
            <statement name="DO">
              <block type="simple_display" id="=z+1kS2@8)zS@C3+;!A*">
                <field name="NEWLINE">TRUE</field>
                <value name="VALUE">
                  <block type="variable_access" id="tEa-`y?+p_L%L52w(R3p*">
                    <field name="VAR">i</field>
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

        # Check if the generated code contains the correct Python for loop
        expect(modal_body).to_contain_text("for i in range(int(1), int(10) + (1 if int(1) > 0 else -1), int(1)):")
        expect(modal_body).to_contain_text("print(i)")

        # Take a screenshot of the modal
        page.locator("#codeModal .modal-content").screenshot(path="jules-scratch/verification/verification.png")

        browser.close()

if __name__ == "__main__":
    run_test()
