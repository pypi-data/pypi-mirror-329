import json
import sys

def extract_versions(lockfile_path):
    """Extracts package names and versions from package-lock.json"""
    try:
        with open(lockfile_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            packages = data.get("dependencies", {})

        return [f"{name} {pkg.get('version', 'Unknown')}" for name, pkg in packages.items()]
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def main():
    """CLI entry point for lockfile-extract"""
    if len(sys.argv) < 2:
        print("Usage: lockfile-extract <path-to-package-lock.json>")
        sys.exit(1)

    lockfile_path = sys.argv[1]
    versions = extract_versions(lockfile_path)
    
    if versions:
        print(", ".join(versions))
    else:
        print("No packages found.")

if __name__ == "__main__":
    main()
