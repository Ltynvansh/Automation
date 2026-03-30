import zipfile
from lxml import etree # type: ignore
 # type: ignore # Your registry file
 # ---------------- LAYERS REGISTRY ----------------

LAYERS = [

    # Core Zones
    {"selection_key": "8_Zone_Image", "title_key": "8 Vastu Zone Analysis", "toggle_key": "8 Zones Analysis"},
    {"selection_key": "16_Zone_Image", "title_key": "16 Vastu Zone Analysis", "toggle_key": "16 Zones Analysis"},
    {"selection_key": "16_Zone_Image_Directions", "title_key": "16 Vastu Zone Directions", "toggle_key": "16 Zones Directions"},
    {"selection_key": "16_Zone_Image_Numbers", "title_key": "16 Vastu Zone Numbers", "toggle_key": "16 Zones Numbers"},
    {"selection_key": "24_Zone_Image", "title_key": "24 Vastu Zone Analysis", "toggle_key": "24 Zones Analysis"},
    {"selection_key": "32_Zone_Image(Moderne vastu)", "title_key": "32 Zones Analysis (Moderne vastu)", "toggle_key": "32 Zone Moderne vastu"},
    {"selection_key": "32 Zones(Vedic)", "title_key": "32 Zones Analysis (Vedic)", "toggle_key": "32 Zone Vedic Vastu"},

    # Colored / Elemental / Dosha / Guna
    {"selection_key": "Colored_Zone_Analysis", "title_key": "Colored Zone Analysis", "toggle_key": "color image"},
    {"selection_key": "Colored_Zone_Colored", "title_key": "Colored Zone (Colored)", "toggle_key": "Colored Image"},
    {"selection_key": "Colored_Zone_Labeled", "title_key": "Colored Zone (Labeled)", "toggle_key": "Labeled Image"},
    {"selection_key": "ElementalZone(Moderne vastu)", "title_key": "Elemental Zone (Moderne vastu)", "toggle_key": "Elemental Zone"},
    {"selection_key": "ElementalZone(Vedic)", "title_key": "Elemental Zone (Vedic)", "toggle_key": "Vedic Elemental Zone"},
    {"selection_key": "Tri_Dosha(Moderne vastu)", "title_key": "TriDosha (Moderne vastu)", "toggle_key": "Tridosha Moderne vastu"},
    {"selection_key": "Tri_Dosha_Vedic", "title_key": "TriDosha (Vedic)", "toggle_key": "Tridosha Vedic Vastu"},
    {"selection_key": "TriGuna", "title_key": "TriGuna (Moderne vastu)", "toggle_key": "Triguna"},
    {"selection_key": "Tri_Guna_Vedic", "title_key": "TriGuna (Vedic)", "toggle_key": "Triguna Vedic Vastu"},

    # Gridded / Planet / Source
    {"selection_key": "64_Gridded_Image", "title_key": "64 Vastu Gridded Image", "toggle_key": "64 Zones Analysis"},
    {"selection_key": "Vedic_Planet_Zoning", "title_key": "Vedic Planet Zoning", "toggle_key": "Vedic Planet Zoning"},
    {"selection_key": "8 Zone(Source Sink)", "title_key": "8 Zone (Source Sink)", "toggle_key": "Sourcesink"},

    # Padvinyash / Body / Special
    {"selection_key": "64_Padvinyash_Analysis", "title_key": "64 Padvinyash Analysis", "toggle_key": "64 padvinyash"},
    {"selection_key": "81_Padvinyash_Analysis", "title_key": "81 Padvinyash Analysis", "toggle_key": "81 padvinyash"},
    {"selection_key": "bodyPart", "title_key": "Body Part Analysis", "toggle_key": "Body part"},
    {"selection_key": "Marmsthan_Image", "title_key": "Marmsthan Image", "toggle_key": "Marma sthan"},
    {"selection_key": "Surya_Chandra_Bhag", "title_key": "Surya Chandra Bhag", "toggle_key": "Surya Chandra Bhag"},
    {"selection_key": "4_States_Image", "title_key": "4 States Image", "toggle_key": "4 States Image"},
    {"selection_key": "Mandal_Image", "title_key": "Mandal Image", "toggle_key": "8 Mandal Image"},
    {"selection_key": "Astha_Disha_Griha_Vastu", "title_key": "Astha Disha Griha Vastu", "toggle_key": "Astha Disha Griha Vastu"},
    {"selection_key": "16_Directional_Domestic_Vastu", "title_key": "16 Directional Domestic Vastu", "toggle_key": "16 Direction Domestic Vastu"},

    # Direction / Fengshui
    {"selection_key": "Direction_and_Their_Influence", "title_key": "Direction and Their Influence", "toggle_key": "Direction and Their Influence"},
    {"selection_key": "Five_Elements_of_Fengshui", "title_key": "Five Elements of Fengshui", "toggle_key": "Five Elements of Fengshui"},

    # Industrial / Commercial
    {"selection_key": "Commercial_Vastu", "title_key": "Commercial Vastu", "toggle_key": "Commercial Vastu"},
    {"selection_key": "Industrial_Vastu", "title_key": "Industrial Vastu", "toggle_key": "Industrial Vastu"},
    {"selection_key": "Hospital_Vastu", "title_key": "Hospital Vastu", "toggle_key": "Hospital Vastu"},
    {"selection_key": "Gender_vastu", "title_key": "Gender Vastu", "toggle_key": "Gender Vastu"},
    {"selection_key": "Academic_Vastu", "title_key": "Academic Vastu", "toggle_key": "Academic Vastu"},
    {"selection_key": "Office_Vastu", "title_key": "Office Vastu", "toggle_key": "Office Vastu"},
    {"selection_key": "Grocery_Store_Vastu", "title_key": "Grocery Store Vastu", "toggle_key": "Grocery Store Vastu"},

    # Guidelines
    {"selection_key": "16_Zone_Guidelines", "title_key": "16 Zone Guidelines", "toggle_key": "16 Zone Guidelines"},
    {"selection_key": "16_Zone_Guidelines_Directions", "title_key": "16 Zone Guidelines (Directions)", "toggle_key": "16 Zone Guidelines"},
    {"selection_key": "16_Zone_Guidelines_Numbers", "title_key": "16 Zone Guidelines (Numbers)", "toggle_key": "16 Zone Guidelines"},
    {"selection_key": "32_Zone_Guidelines", "title_key": "32 Zone Guidelines", "toggle_key": "32 Zone Guidelines"},
    {"selection_key": "64_Zone_Guidelines", "title_key": "64 Zone Guidelines", "toggle_key": "64 Zone Guidelines"},
    {"selection_key": "4_States_Guidelines", "title_key": "4 States Guidelines", "toggle_key": "4 States Guidelines"},
    {"selection_key": "Padvinyash_Guidelines_64", "title_key": "Padvinyash Guidelines (64)", "toggle_key": "Padvinyash Guidelines 64"},
    {"selection_key": "Padvinyash_Guidelines_81", "title_key": "Padvinyash Guidelines (81)", "toggle_key": "Padvinyash Guidelines 81"},

    # Moderne Names / Numbers
    {"selection_key": "Moderne_vastu_Names_81", "title_key": "Moderne vastu Names (81 Padvinyash)", "toggle_key": "Moderne vastu Names 81"},
    {"selection_key": "Moderne_vastu_Names_64", "title_key": "Moderne vastu Names (64 Padvinyash)", "toggle_key": "Moderne vastu Names 64"},
    {"selection_key": "Moderne_vastu_Numbers_81", "title_key": "Moderne vastu Numbers (81 Padvinyash)", "toggle_key": "Moderne vastu Numbers 81"},
    {"selection_key": "Moderne_vastu_Numbers_64", "title_key": "Moderne vastu Numbers (64 Padvinyash)", "toggle_key": "Moderne vastu Numbers 64"},

    # Vedic Names / Numbers
    {"selection_key": "Vedic_Names_81", "title_key": "Vedic Names (81 Padvinyash)", "toggle_key": "Vedic Names 81"},
    {"selection_key": "Vedic_Names_64", "title_key": "Vedic Names (64 Padvinyash)", "toggle_key": "Vedic Names 64"},
    {"selection_key": "Vedic_Numbers_81", "title_key": "Vedic Numbers (81 Padvinyash)", "toggle_key": "Vedic Numbers 81"},
    {"selection_key": "Vedic_Numbers_64", "title_key": "Vedic Numbers (64 Padvinyash)", "toggle_key": "Vedic Numbers 64"},

    # Special
    {"selection_key": "Ratna_Sthapna", "title_key": "Ratna Sthapna", "toggle_key": "Ratna Sthapna"},
    {"selection_key": "Nakshatra_Vastu", "title_key": "Nakshatra Vastu", "toggle_key": "Nakshatra Vastu"},
    {"selection_key": "Nakshatra_Vastu_Name", "title_key": "Nakshatra Vastu Names", "toggle_key": "Nakshatra Vastu Name"},
    {"selection_key": "Nakshatra_Vastu_Number", "title_key": "Nakshatra Vastu Numbers", "toggle_key": "Nakshatra Vastu Number"},
    {"selection_key": "Zodiac_Vastu", "title_key": "Zodiac Vastu", "toggle_key": "Zodiac Vastu"},
    {"selection_key": "Ancient_81_pad_Devta", "title_key": "Ancient 81 pad Devta", "toggle_key": "Ancient 81 pad Devta"},
    {"selection_key": "Ancient_81_pad_Number", "title_key": "Ancient 81 pad Number", "toggle_key": "Ancient 81 pad Number"},

]

DOCX_PATH = "/Users/vanshlatiyan/Downloads/Vansh/d folder/Automation/Gridded Report_latestProject_Flat_Layout_Report_20260225_221124.docx"

# -------- EXTRACT KEYWORDS --------
keywords = [
    layer["title_key"]
    for layer in LAYERS
    if layer.get("title_key")
]

# -------- OPEN DOCX --------
with zipfile.ZipFile(DOCX_PATH) as docx:
    xml_content = docx.read("word/document.xml")

root = etree.XML(xml_content)

# Extract text from XML
all_text = []
for node in root.iter():
    if node.tag.endswith("}t"):
        all_text.append(node.text)

document_text = " ".join(filter(None, all_text)).lower()

# -------- SEARCH KEYWORDS --------
print("\n🔍 Searching Sections in DOCX\n")

for keyword in keywords:
    if keyword.lower() in document_text:
        print(f"✅ FOUND → {keyword}")
    else:
        print(f"❌ MISSING → {keyword}")