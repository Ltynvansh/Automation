import streamlit as st
import json
import zipfile
import re
import os
from datetime import datetime

# ---------------- BASE PATH ----------------
appdata_local = os.path.join(
    os.path.expanduser("~/Library/Application Support"),
    "VastuApp"
)

projects_dir = os.path.join(appdata_local, "MapAnalysis_Projects")

# ---------------- GET LATEST PROJECT ----------------
def get_latest_project_path():
    try:
        projects = [
            os.path.join(projects_dir, d)
            for d in os.listdir(projects_dir)
            if os.path.isdir(os.path.join(projects_dir, d))
        ]

        valid_projects = []

        for project in projects:
            report_file = os.path.join(project, "report.data.json")

            if os.path.exists(report_file):
                valid_projects.append(project)

        if not valid_projects:
            raise Exception("No valid project with report.data.json found")

        latest_project = max(valid_projects, key=os.path.getmtime)

        return latest_project

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

# Output files
RESULT_FILE = "validation_result.txt"
XML_FILE = "output.xml"

# ---------------- TOGGLE → KEYWORDS ----------------
TOGGLE_KEYWORDS = {
    "8 Zones Analysis": ["8 Vastu Zone Analysis"],
    "16 Zones Analysis": ["16 Vastu Zone Analysis"],
    "24 Zones Analysis": ["24 Vastu Zone Analysis"],
    "64 Zones Analysis": ["64 Vastu Gridded Image"],
    "32 Zone Moderne vastu": ["32 Zones Analysis (Moderne vastu)"],
    "32 Zone Vedic Vastu": ["32 Zones Analysis (Vedic)"],
    "Marma sthan": ["Marmsthan Image"],
    "Body part": ["Body Part Analysis"],
}

# ---------------- DOCX READER ----------------
def extract_docx_data(file):
    with zipfile.ZipFile(file) as docx:
        xml_bytes = docx.read("word/document.xml")

    # Save XML
    with open(XML_FILE, "wb") as f:
        f.write(xml_bytes)

    xml = xml_bytes.decode()

    # remove XML tags
    text = re.sub("<.*?>", " ", xml).lower()

    return text, xml


# ---------------- IMAGE CHECK ----------------
def check_image_after_keyword(xml, keyword):

    keyword = keyword.lower()
    pos = xml.lower().find(keyword)

    if pos == -1:
        return False

    # check next part of xml
    forward_chunk = xml[pos: pos + 8000]

    if "<w:drawing" in forward_chunk or "<a:blip" in forward_chunk:
        return True

    return False


# ---------------- RESULT LOGGER ----------------
def write_result(msg):
    with open(RESULT_FILE, "a") as f:
        f.write(msg + "\n")


# ---------------- FAIL REASON ----------------
def get_fail_reason(toggle):
    t = toggle.lower()

    if "3d" in t:
        return "3D content is graphical (images), not plain text"
    elif "devta" in t:
        return "Devta section may be charts/images, not text"
    elif "feng" in t:
        return "Feng Shui items may be visual elements"
    else:
        return "Section heading not found (keyword mismatch)"


# ---------------- UI ----------------
st.title("Vastu Detailed Report Validator")

st.info(f"📂 Using Project: {latest_project_path}")

uploaded_file = st.file_uploader("Upload Detailed Report (.docx)", type=["docx"])

if uploaded_file:

    # clear old results
    open(RESULT_FILE, "w").close()

    st.success("DOCX Uploaded Successfully")

    # ---------------- LOAD JSON ----------------
    try:
        with open(EXPECTED_JSON) as f:
            expected = json.load(f)

        with open(ACTUAL_JSON) as f:
            actual = json.load(f)

        with open(REPORT_DATA) as f:
            report_data = json.load(f)

    except Exception as e:
        st.error(f"❌ Error loading JSON files: {e}")
        st.stop()

    actual_toggles = actual.get("toggles", {})

    # ---------------- DOCX EXTRACTION ----------------
    report_text, full_xml = extract_docx_data(uploaded_file)

    st.header("📊 Toggle Validation")

    write_result("===== VALIDATION REPORT =====")
    write_result(f"Time: {datetime.now()}\n")

    pass_count = 0
    fail_count = 0

    # ---------------- TOGGLE VALIDATION ----------------
    for toggle, value in actual_toggles.items():

        if value:  # only TRUE toggles

            keywords = TOGGLE_KEYWORDS.get(toggle, [toggle])

            found_text = False
            found_image = False

            for word in keywords:

                if word.lower() in report_text:
                    found_text = True

                    if check_image_after_keyword(full_xml, word):
                        found_image = True

                    break

            if found_text and found_image:
                st.success(f"✅ PASS: {toggle} (Text + Image)")
                write_result(f"PASS: {toggle}")
                pass_count += 1

            elif found_text and not found_image:
                st.warning(f"⚠ PARTIAL: {toggle}")
                st.warning("Reason: Text found but image missing")

                write_result(f"PARTIAL: {toggle} (No Image)")
                fail_count += 1

            else:
                reason = get_fail_reason(toggle)

                st.error(f"❌ FAIL: {toggle}")
                st.warning(f"Reason: {reason}")

                write_result(f"FAIL: {toggle}")
                write_result(f"Reason: {reason}\n")

                fail_count += 1

    # ---------------- SECTION VALIDATION ----------------
    st.header("🧩 Section-wise Validation")

    def validate_items(section_name, toggle_key, items_dict):

        st.subheader(f"🔷 {section_name}")

        if not actual_toggles.get(toggle_key, False):
            st.info(f"{section_name} Toggle OFF")
            return

        items = [k for k, v in items_dict.items() if v]

        st.write(f"Selected Items: {len(items)}")

        found = []
        missing = []

        for item in items:
            clean = item.replace("_", " ").lower()

            if clean in report_text:
                found.append(item)
            else:
                missing.append(item)

        st.success(f"Found: {len(found)}")
        st.error(f"Missing: {len(missing)}")

        write_result(f"\n[{section_name}]")
        write_result(f"Found: {len(found)} | Missing: {len(missing)}")

        for m in missing:
            write_result(f"Missing: {m}")

    validate_items(
        "3D Remedies",
        "3D remedies inside 16 zones",
        report_data.get("selected_3d_items", {})
    )

    validate_items(
        "Devta",
        "Devta",
        report_data.get("selected_devta_items", {})
    )

    validate_items(
        "Feng Shui",
        "Feng Shui Cards",
        report_data.get("selected_fengshui_items", {})
    )

    # ---------------- FINAL SUMMARY ----------------
    st.header("📈 Final Summary")

    st.success(f"✅ PASS: {pass_count}")
    st.error(f"❌ FAIL: {fail_count}")

    write_result("\n===== SUMMARY =====")
    write_result(f"PASS: {pass_count}")
    write_result(f"FAIL: {fail_count}")
   

    st.success("📄 validation_result.txt saved")
    st.success("🧾 output.xml saved")