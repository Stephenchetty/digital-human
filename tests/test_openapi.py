import json
from pathlib import Path

def test_openapi_structure():
    openapi_path = Path(__file__).resolve().parents[1] / 'api' / 'openapi.json'
    with open(openapi_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    assert 'paths' in spec, "'paths' key missing in openapi spec"
    assert '/generate' in spec.get('paths', {}), "'/generate' path missing"
