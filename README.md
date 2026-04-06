# 🏠 Vastu Report Automation & Validator

A powerful automation tool to validate **Vastu detailed reports (DOCX)** by extracting XML data and verifying content, structure, and images.

---

## 🚀 Features

* 📄 Extracts XML from DOCX reports
* 🔍 Validates **keywords based on toggles**
* 🖼️ Ensures **images exist when required**
* ⚙️ JSON-based configuration (Expected vs Actual)
* 📊 Section-wise validation:

  * 3D Remedies
  * Devta
  * Feng Shui
* 🧾 Generates:

  * `validation_result.txt`
  * `output.xml`
* 💻 Simple UI using Streamlit

---

## 🧠 Core Logic

* If a toggle is **enabled** → keyword must exist
* If keyword exists → **image must also exist in XML**
* Missing image = ❌ FAIL

---

## 📂 Project Structure

```
Automation/
│
├── automation.py              # Main validation logic
├── validator_gui.py           # Streamlit UI
├── expected.json              # Expected toggle configuration
├── actual.json                # Actual toggle values
├── report.data.json           # Section-wise data
│
├── output.xml                 # Extracted XML (auto-generated)
├── validation_result.txt      # Validation results (auto-generated)
│
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/Automation.git
cd Automation
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run validator_gui.py
```

---

## 📥 Usage

1. Upload a **DOCX Vastu Report**
2. Tool will:

   * Extract XML
   * Validate toggles
   * Check images
3. View results in UI + text file

---

## 📌 Example Validation Output

```
PASS: 8 Zones Analysis
FAIL: 16 Zones Analysis
Reason: Image missing after keyword
```

---

## 🛠 Tech Stack

* Python 🐍
* Streamlit 🌐
* XML Processing
* JSON-based validation

---

## ⚠️ Important Notes

* Do not upload:

  * `output.xml`
  * `validation_result.txt`
  * `venv/`
* These are auto-generated files

---

## 🔥 Future Improvements

* ✅ Advanced image mapping per section
* 📊 Dashboard analytics
* ☁️ Cloud deployment (Streamlit Cloud)
* 🤖 AI-based report validation

---

## 👨‍💻 Author

**Vansh Latiyan**
B.Tech CSE (AI)
GitHub: https://github.com/Ltynvansh

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
