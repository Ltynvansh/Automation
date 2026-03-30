import json
import zipfile
import re
import sys

# ---------------- PATHS ----------------

EXPECTED_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/report_settings.json"

ACTUAL_JSON = "/Users/vanshlatiyan/Library/Application Support/VastuApp/MapAnalysis_Projects/latestProject/report_settings.json"

DOCX_REPORT = "/Users/vanshlatiyan/Downloads/vansh_latestProject_Flat_Layout_Report_20260313_205605.docx"


# ---------------- TOGGLE → REPORT KEYWORDS ----------------

TOGGLE_KEYWORDS = {
    "8 Zones Analysis": ["8 Vastu Zone Analysis"],
    "16 Zones Analysis": ["16 Vastu Zone Analysis"],
    "24 Zones Analysis": ["24 Vastu Zone Analysis"],
    "64 Zones Analysis": ["64 Vastu Gridded Image"],
    "32 Zone Moderne vastu": ["32 Zones Analysis (Moderne vastu)"],
    "32 Zone Vedic Vastu": ["32 Zones Analysis (Vedic)"],
    "Marma sthan": ["Marmsthan Image"],
    "Body part": ["Body Part Analysis"],
    "64 padvinyash": ["64 Padvinyash Analysis"],
    "81 padvinyash": ["81 Padvinyash Analysis"],
    "Triguna": ["TriGuna"],
    "Triguna Vedic Vastu": ["TriGuna (Vedic)"],
    "Tridosha Moderne vastu": ["TriDosha"],
    "Tridosha Vedic Vastu": ["TriDosha (Vedic)"],
    "4 States Image": ["4 States Image"],
    "Surya Chandra Bhag": ["Surya Chandra Bhag"],
    "Vedic Planet Zoning": ["Vedic Planet Zoning"]
}


# ---------------- LOAD JSON ----------------

def load_json(path):

    try:
        with open(path, "r") as f:
            return json.load(f)

    except Exception as e:
        print("JSON loading error:", e)
        sys.exit(1)


# ---------------- EXTRACT TEXT FROM DOCX ----------------

def extract_docx_text(docx_path):

    try:

        with zipfile.ZipFile(docx_path) as docx:

            xml = docx.read("word/document.xml").decode()

        # remove XML tags
        text = re.sub("<.*?>", " ", xml)

        return text

    except Exception as e:

        print("DOCX read error:", e)
        sys.exit(1)


# ---------------- FIND ENABLED TOGGLES ----------------

def get_enabled_toggles(expected, actual):

    expected_toggles = expected.get("toggles", {})
    actual_toggles = actual.get("toggles", {})

    enabled = []

    print("\nChecking JSON Toggles\n")

    for toggle, value in expected_toggles.items():

        if toggle not in actual_toggles:

            print("Missing toggle:", toggle)

        elif value != actual_toggles[toggle]:

            print("Mismatch:", toggle)

        else:

            print("OK:", toggle)

            if value:
                enabled.append(toggle)

    return enabled


# ---------------- VALIDATE REPORT ----------------

def validate_report(enabled_toggles, report_text):

    print("\nChecking Detailed Report Sections\n")

    pass_count = 0
    fail_count = 0

    for toggle in enabled_toggles:

        keywords = TOGGLE_KEYWORDS.get(toggle, [toggle])

        found = False

        for word in keywords:

            if word.lower() in report_text.lower():

                print("PASS:", word)
                pass_count += 1
                found = True
                break

        if not found:

            print("FAIL:", toggle)
            fail_count += 1

    print("\n==============================")
    print("REPORT VALIDATION SUMMARY")
    print("==============================")

    print("Checked:", len(enabled_toggles))
    print("PASS:", pass_count)
    print("FAIL:", fail_count)

    return fail_count == 0


# ---------------- MAIN ----------------

if __name__ == "__main__":

    print("\nLoading JSON files...\n")

    expected_json = load_json(EXPECTED_JSON)
    actual_json = load_json(ACTUAL_JSON)

    enabled_toggles = get_enabled_toggles(expected_json, actual_json)

    print("\nReading Detailed Report...\n")

    report_text = extract_docx_text(DOCX_REPORT)

    result = validate_report(enabled_toggles, report_text)

    print("\n==============================")

    if result:
        print("🎉 VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")