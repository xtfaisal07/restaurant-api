from contract import load_spec

def validate_openapi():
    try:
        load_spec()
        print("PASS: OpenAPI specification is valid")
    except Exception as e:
        print("FAIL:", e)
        raise

if __name__ == "__main__":
    validate_openapi()