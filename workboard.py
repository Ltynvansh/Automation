import streamlit as st
import json
import zipfile
import re
import os
from datetime import datetime

# ---------------- YOUR FIXED PATHS ----------------
EXPECTED_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/report_settings.json"

ACTUAL_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report_settings.json"

REPORT_DATA = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report.data.json"

# Output files
RESULT_FILE = "validation_result.txt"
XML_FILE = "output.xml"

# ---------------- SAFE FILE CHECK ----------------
def check_file(path):
    if not os.path.exists(path):
        
        st.error(f"❌ File not found:\n{path}")
        return False
    return True

# ---------------- DOCX ----------------
def extract_docx(file):
    with zipfile.ZipFile(file) as docx:
        xml_bytes = docx.read("word/document.xml")

    with open(XML_FILE, "wb") as f:
        f.write(xml_bytes)

    xml = xml_bytes.decode()
    text = re.sub("<.*?>", " ", xml).lower()

    return text, xml

# ---------------- IMAGE CHECK ----------------
def check_image(xml, keyword):
    pos = xml.lower().find(keyword.lower())

    if pos == -1:
        return False

    chunk = xml[pos:pos+8000]

    return "<w:drawing" in chunk or "<a:blip" in chunk

# ---------------- UI ----------------
st.title("Vastu Detailed Report Validator")

st.info("📂 Using Fixed Local Paths")

uploaded_file = st.file_uploader("Upload DOCX", type=["docx"])

if uploaded_file:

    # Check files first
    if not (check_file(EXPECTED_JSON) and check_file(ACTUAL_JSON) and check_file(REPORT_DATA)):
        st.stop()

    st.success("DOCX Uploaded")

    # Load JSON
    with open(EXPECTED_JSON) as f:
        expected = json.load(f)

    with open(ACTUAL_JSON) as f:
        actual = json.load(f)

    with open(REPORT_DATA) as f:
        report_data = json.load(f)

    toggles = actual.get("report_settings_toggles", {})

    # Extract DOCX
    text, xml = extract_docx(uploaded_file)

    st.header("📊 Toggle Validation")

    pass_count = 0
    fail_count = 0

    for toggle, data in toggles.items():

        if data.get("is_required", False):

            keyword = toggle.lower()

            found_text = keyword in text
            found_image = check_image(xml, keyword)

            if found_text and found_image:
                st.success(f"✅ PASS: {toggle}")
                pass_count += 1

            elif found_text:
                st.warning(f"⚠ PARTIAL: {toggle} (No Image)")
                fail_count += 1

            else:
                st.error(f"❌ FAIL: {toggle}")
                st.warning("Reason: Not found in DOCX")
                fail_count += 1

    # ---------------- SECTION CHECK ----------------
    st.header("🧩 Section Validation")

    def validate(name, items):
        st.subheader(name)

        selected = [k for k, v in items.items() if v]

        found = sum(1 for i in selected if i.replace("_"," ").lower() in text)

        st.write(f"Found: {found}")
        st.write(f"Missing: {len(selected)-found}")

    validate("3D Remedies", report_data.get("selected_3d_items", {}))
    validate("Devta", report_data.get("selected_devta_items", {}))
    validate("Feng Shui", report_data.get("selected_fengshui_items", {}))

    # ---------------- SUMMARY ----------------
    st.header("📈 Summary")

    st.success(f"PASS: {pass_count}")
    st.error(f"FAIL: {fail_count}")