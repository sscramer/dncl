import re
from pathlib import Path
from playwright.sync_api import Page, expect
import pytest

# Helper function to load and run a Blockly program and return the output text.
def run_blockly_program(page: Page, xml_content: str):
    """
    Injects and runs a Blockly XML program on the page.
    Returns the text content of the output div.
    """
    # Go to the page, wait for it to load and for the workspace to be ready
    page.goto(f"file://{Path(__file__).parent.absolute()}/index.html", wait_until="load")
    page.wait_for_function("() => window.workspace")

    # Sanitize XML for injection into a JavaScript template literal
    # Removed .replace("\\", "\\\\") which caused a JS SyntaxError
    js_safe_xml_content = xml_content.replace("`", "\\`").replace("\n", "")

    # Clear workspace and load new XML
    page.evaluate(f'''
        window.workspace.clear();
        const xml = Blockly.utils.xml.textToDom(`{js_safe_xml_content}`);
        Blockly.Xml.domToWorkspace(xml, window.workspace);
    ''')

    # Run the code
    page.locator("button#runButton").click()

    # Wait for the output to appear and return its text
    output_div = page.locator("#outputDiv")
    output_div.wait_for(state="attached", timeout=5000)
    return output_div.inner_text()

# Helper to generate XML for a simple assignment and display
def create_test_xml(math_input: str, var_name: str = "x") -> str:
    """Creates XML to assign the result of a math expression to a variable and display it."""
    return f"""
    <xml xmlns="https://developers.google.com/blockly/xml">
      <block type="assignment" x="110" y="90">
        <field name="VAR">{var_name}</field>
        <value name="VALUE">
          <block type="math_free_input">
            <field name="MATH_INPUT">{math_input}</field>
          </block>
        </value>
        <next>
          <block type="simple_display">
            <field name="NEWLINE">TRUE</field>
            <value name="VALUE">
              <block type="variable_access">
                <field name="VAR">{var_name}</field>
              </block>
            </value>
          </block>
        </next>
      </block>
    </xml>
    """

# Original test case, refactored
def test_original_math_free_input_block(page: Page):
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
    output = run_blockly_program(page, xml_content)
    assert output.strip() == "3"

# Parameterized test for various mathematical expressions
@pytest.mark.parametrize("expression, expected", [
    ("3*2-1", "5"),
    ("(3+2)*5", "25"),
    ("10 / (2.5 * 2)", "2"),
    ("1.5 * 3 - 0.5", "4"),
    ("Math.sqrt(16)", "4"),
    ("Math.pow(2, 3)", "8"),
    ("Math.round(2.6)", "3"),
])
def test_advanced_math_expressions(page: Page, expression: str, expected: str):
    xml = create_test_xml(expression)
    output = run_blockly_program(page, xml)
    assert output.strip() == expected

# Test for 1D array access with calculations in the index
def test_1d_array_access(page: Page):
    xml_content = """
    <xml xmlns="https://developers.google.com/blockly/xml">
      <block type="assignment" x="110" y="90">
        <field name="VAR">i</field>
        <value name="VALUE"><block type="number_literal"><field name="NUM">1</field></block></value>
        <next>
          <block type="assignment">
            <field name="VAR">A</field>
            <value name="VALUE">
              <block type="lists_create_with">
                <mutation items="3"></mutation>
                <value name="ADD0"><block type="number_literal"><field name="NUM">10</field></block></value>
                <value name="ADD1"><block type="number_literal"><field name="NUM">20</field></block></value>
                <value name="ADD2"><block type="number_literal"><field name="NUM">30</field></block></value>
              </block>
            </value>
            <next>
              <block type="assignment">
                <field name="VAR">x</field>
                <value name="VALUE">
                  <block type="math_free_input"><field name="MATH_INPUT">A[i+1] * 2</field></block>
                </value>
                <next>
                  <block type="simple_display">
                    <field name="NEWLINE">TRUE</field>
                    <value name="VALUE"><block type="variable_access"><field name="VAR">x</field></block></value>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </next>
      </block>
    </xml>
    """
    output = run_blockly_program(page, xml_content)
    assert output.strip() == "60" # A[1+1] -> A[2] which is 30. 30 * 2 = 60.

# Test for 2D array access with calculations in indices
def test_2d_array_access(page: Page):
    xml_content = """
    <xml xmlns="https://developers.google.com/blockly/xml">
      <block type="assignment" x="110" y="90">
        <field name="VAR">i</field><value name="VALUE"><block type="number_literal"><field name="NUM">0</field></block></value>
        <next>
          <block type="assignment">
            <field name="VAR">j</field><value name="VALUE"><block type="number_literal"><field name="NUM">2</field></block></value>
            <next>
              <block type="assignment">
                <field name="VAR">M</field>
                <value name="VALUE">
                  <block type="lists_create_with">
                    <mutation items="2"></mutation>
                    <value name="ADD0">
                      <block type="lists_create_with">
                        <mutation items="3"></mutation>
                        <value name="ADD0"><block type="number_literal"><field name="NUM">1</field></block></value>
                        <value name="ADD1"><block type="number_literal"><field name="NUM">2</field></block></value>
                        <value name="ADD2"><block type="number_literal"><field name="NUM">3</field></block></value>
                      </block>
                    </value>
                    <value name="ADD1">
                      <block type="lists_create_with">
                        <mutation items="3"></mutation>
                        <value name="ADD0"><block type="number_literal"><field name="NUM">4</field></block></value>
                        <value name="ADD1"><block type="number_literal"><field name="NUM">5</field></block></value>
                        <value name="ADD2"><block type="number_literal"><field name="NUM">6</field></block></value>
                      </block>
                    </value>
                  </block>
                </value>
                <next>
                  <block type="assignment">
                    <field name="VAR">x</field>
                    <value name="VALUE">
                      <block type="math_free_input"><field name="MATH_INPUT">M[i+1, j-1] + 5</field></block>
                    </value>
                    <next>
                      <block type="simple_display">
                        <field name="NEWLINE">TRUE</field>
                        <value name="VALUE"><block type="variable_access"><field name="VAR">x</field></block></value>
                      </block>
                    </next>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </next>
      </block>
    </xml>
    """
    output = run_blockly_program(page, xml_content)
    assert output.strip() == "10" # M[0+1, 2-1] -> M[1, 1] which is 5. 5 + 5 = 10.

# Test for error handling of invalid expressions
# Updated error messages to match actual Japanese output from the application
@pytest.mark.parametrize("expression, error_message", [
    ("y * 2", "実行エラー: y is not defined"), # y is not defined
    ("3 +* 2", "コード生成エラー"),    # Invalid syntax
    ("A[99]", "配列の範囲外アクセス"), # Array index out of bounds
])
def test_error_handling(page: Page, expression: str, error_message: str):
    # This test needs an array 'A' to be defined for the out-of-bounds check
    xml_content = f"""
    <xml xmlns="https://developers.google.com/blockly/xml">
        <block type="assignment" x="110" y="90">
            <field name="VAR">A</field>
            <value name="VALUE">
              <block type="lists_create_with">
                <mutation items="1"></mutation>
                <value name="ADD0"><block type="number_literal"><field name="NUM">10</field></block></value>
              </block>
            </value>
            <next>
              <block type="assignment">
                <field name="VAR">x</field>
                <value name="VALUE">
                  <block type="math_free_input">
                    <field name="MATH_INPUT">{expression}</field>
                  </block>
                </value>
                <next>
                  <block type="simple_display">
                    <field name="NEWLINE">TRUE</field>
                    <value name="VALUE">
                      <block type="variable_access"><field name="VAR">x</field></block>
                    </value>
                  </block>
                </next>
              </block>
            </next>
        </block>
    </xml>
    """
    output = run_blockly_program(page, xml_content)
    assert error_message in output
