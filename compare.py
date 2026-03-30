import json
import sys

EXPECTED_JSON = "expected.json"
ACTUAL_JSON = "actual.json"


# ---------------- LOAD JSON ----------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        sys.exit(1)


# ---------------- TOGGLE VALIDATION ----------------
def validate_toggles(expected, actual):

    print("\n🔎 Validating TOGGLES section...\n")

    expected_toggles = expected.get("toggles", {})
    actual_toggles = actual.get("toggles", {})

    all_pass = True

    # 1️⃣ Check Missing Toggles
    for key in expected_toggles:
        if key not in actual_toggles:
            print(f"❌ Missing toggle in actual: {key}")
            all_pass = False

    # 2️⃣ Check Extra Toggles
    for key in actual_toggles:
        if key not in expected_toggles:
            print(f"⚠ Extra toggle found in actual: {key}")

    # 3️⃣ Check Value Differences
    for key in expected_toggles:
        if key in actual_toggles:
            if expected_toggles[key] != actual_toggles[key]:
                print(
                    f"❌ Toggle mismatch → {key}: "
                    f"expected={expected_toggles[key]} "
                    f"actual={actual_toggles[key]}"
                )
                all_pass = False
            else:
                print(f"✅ {key} = {expected_toggles[key]}")

    print("\n====================================")

    if all_pass:
        print("✅ TOGGLE VALIDATION PASSED")
    else:
        print("❌ TOGGLE VALIDATION FAILED")

    return all_pass


# ---------------- MAIN ----------------
def main():

    expected = load_json(EXPECTED_JSON)
    actual = load_json(ACTUAL_JSON)

    result = validate_toggles(expected, actual)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
