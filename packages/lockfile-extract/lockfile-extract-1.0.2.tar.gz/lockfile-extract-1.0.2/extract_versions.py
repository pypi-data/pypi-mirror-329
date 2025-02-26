import json
import sys
import csv

def extract_versions(lockfile_path):
    """Extracts package names and versions from package-lock.json"""
    try:
        with open(lockfile_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            packages = data.get("dependencies", {})

        return [{"name": name, "version": pkg.get("version", "Unknown")} for name, pkg in packages.items()]
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    """CLI entry point for lockfile-extract"""
    if len(sys.argv) < 2:
        print("Usage: lockfile-extract <path-to-package-lock.json> [--format=csv|json]")
        sys.exit(1)

    lockfile_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else None

    versions = extract_versions(lockfile_path)

    if not versions:
        print("No packages found.")
        sys.exit(1)

    # ✅ Default: Print to CLI
    for package in versions:
        print(f"{package['name']} {package['version']}")

    # ✅ If format is provided, save to a file
    if output_format == "--format=json":
        json_filename = "output.json"
        with open(json_filename, "w", encoding="utf-8") as jsonfile:
            json.dump(versions, jsonfile, indent=2)
        print(f"\n🔹 JSON output saved to {json_filename}")

    elif output_format == "--format=csv":
        csv_filename = "output.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "version"])
            writer.writeheader()
            writer.writerows(versions)
        print(f"\n🔹 CSV output saved to {csv_filename}")

    elif output_format:
        print("\n❌ Invalid format. Use --format=json or --format=csv")
        sys.exit(1)

if __name__ == "__main__":
    main()
