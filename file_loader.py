import pandas as pd

def load_dataset(file):
    filename = file.name.lower()

    # =========================
    # 📊 EXCEL FILES
    # =========================
    if filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(file, engine="openpyxl")

    # =========================
    # 📄 CSV FILES
    # =========================
    elif filename.endswith(".csv"):

        # Try standard UTF-8
        try:
            return pd.read_csv(file, encoding="utf-8")

        except Exception:
            pass

        # Try latin1 (very common fix)
        try:
            file.seek(0)
            return pd.read_csv(file, encoding="latin1")

        except Exception:
            pass

        # 🔥 BEST: auto-detect separator
        try:
            file.seek(0)
            return pd.read_csv(file, sep=None, engine="python")

        except Exception:
            pass

        # Try semicolon CSV
        try:
            file.seek(0)
            return pd.read_csv(file, sep=";", encoding="latin1")

        except Exception:
            pass

        # Try tab-separated
        try:
            file.seek(0)
            return pd.read_csv(file, sep="\t", encoding="latin1")

        except Exception:
            pass

        # ❌ Final fail
        raise ValueError("❌ Could not read CSV file. Try re-saving as CSV UTF-8.")

    # =========================
    # ❌ UNKNOWN FORMAT
    # =========================
    else:
        raise ValueError("Unsupported file format")