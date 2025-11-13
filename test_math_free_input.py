import re
from pathlib import Path
from playwright.sync_api import Page, expect


def test_math_free_input_block(page: Page):
    # Navigate to the local index.html file
    page.goto(f"file://{Path(__file__).parent.absolute()}/index.html")

    # Define the Blockly XML for the test program
    xml_content = """
    <xml xmlns="https://developers.google.com/blockly/xml">
      <block type="assignment" id="N8-W]u6)u.]p0]p/h,aQ" x="110" y="90">
        <field name="VAR">i</field>
        <value name="VALUE">
          <block type="number_literal" id="E6`h%_8(Kj/J6f-0,Vz_">
            <field name="NUM">3</field>
          </block>
        </value>
        <next>
          <block type="assignment" id="v!@*w,k/mJ6_?J/8q{S,">
            <field name="VAR">x</field>
            <value name="VALUE">
              <block type="math_free_input" id="R;pG(S_V!Bq;!@;,*Kz@">
                <field name="MATH_INPUT">3*2-1*i</field>
              </block>
            </value>
            <next>
              <block type="simple_display" id="=zX_9[2a[L@b_?dE`*x,">
                <field name="NEWLINE">TRUE</field>
                <value name="VALUE">
                  <block type="variable_access" id="x:hY1(zB]V_E_k(5[}o,">
                    <field name="VAR">x</field>
                  </block>
                </value>
              </block>
            </next>
          </block>
        </next>
      </block>
    </xml>
    """

    # Sanitize the XML content for JavaScript
    js_safe_xml_content = xml_content.replace("`", "\\`").replace("\n", "")

    # Use JavaScript to load the XML into the Blockly workspace
    page.evaluate(f'''
        const xml = Blockly.utils.xml.textToDom(`{js_safe_xml_content}`);
        Blockly.Xml.domToWorkspace(xml, window.workspace);
    ''')

    # Click the run button
    page.locator("button#runButton").click()

    # Wait for the output to appear and assert its value
    output_div = page.locator("#outputDiv")
    expect(output_div).to_have_text("3")

    # Take a screenshot for verification
    page.screenshot(path="screenshot.png")
