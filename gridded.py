import os
import zipfile
from docx import Document # type: ignore

# -------- CONFIG --------
DOCX_PATH = "/Users/vanshlatiyan/Downloads/Vansh/d folder/Automation/Gridded Report_latestProject_Flat_Layout_Report_20260225_221124.docx"
KEYWORD = "4 States Image"   # Change this dynamically

# -------- STEP 1: CHECK FILE EXISTS --------
if not os.path.exists(DOCX_PATH):
    print("❌ Report file not found.")
    exit()

print("📄 Opening Report...")

# -------- STEP 2: READ TEXT --------
doc = Document(DOCX_PATH)
full_text = "\n".join([p.text for p in doc.paragraphs])

keyword_found = KEYWORD.lower() in full_text.lower()

# -------- STEP 3: CHECK IMAGES --------
image_count = 0

with zipfile.ZipFile(DOCX_PATH, 'r') as docx_zip:
    for file in docx_zip.namelist():
        if file.startswith("word/media/"):
            image_count += 1

print(f"🖼 Total Images Found in Report: {image_count}")

# -------- STEP 4: VALIDATION --------
print("\n🔍 VALIDATION RESULT\n")

if keyword_found:
    print(f"✅ Keyword '{KEYWORD}' FOUND in report")

    if image_count > 0:
        print("✅ Image exists in report")
        print("🎉 TEST CASE PASSED")
    else:
        print("❌ No images found in report")
        print("❌ TEST CASE FAILED")
else:
    print(f"❌ Keyword '{KEYWORD}' NOT found in report")
    print("❌ TEST CASE FAILED")