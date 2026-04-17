import csv
from pathlib import Path

DATA_DIR = Path("data")
INPUT_FILES = [
    DATA_DIR / "daily_sales_data_0.csv",
    DATA_DIR / "daily_sales_data_1.csv",
    DATA_DIR / "daily_sales_data_2.csv",
]
OUTPUT_FILE = DATA_DIR / "pink_morsels_sales.csv"


def to_float(value: str) -> float:
    value = value.strip()
    if value.startswith("$"):
        value = value[1:]
    return float(value)


def main() -> None:
    rows_out = []

    for file_path in INPUT_FILES:
        with file_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                product = row["product"].strip().lower()

                # Your data uses "pink morsel"
                if product not in {"pink morsel", "pink morsels"}:
                    continue

                quantity = int(row["quantity"])
                price = to_float(row["price"])
                sales = quantity * price

                rows_out.append(
                    {
                        "Sales": f"{sales:.2f}",
                        "Date": row["date"].strip(),
                        "Region": row["region"].strip(),
                    }
                )

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Sales", "Date", "Region"])
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()