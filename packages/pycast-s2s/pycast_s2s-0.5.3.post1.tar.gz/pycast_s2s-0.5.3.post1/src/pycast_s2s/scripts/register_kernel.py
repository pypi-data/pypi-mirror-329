import os

def main():
    print("📢 Registering Jupyter kernel...")
    os.system("python -m ipykernel install --user --name=pycast-s2s --display-name 'Python (pycast-s2s)'")
    print("✅ Kernel 'Python (pycast-s2s)' registered successfully!")

if __name__ == "__main__":
    main()
