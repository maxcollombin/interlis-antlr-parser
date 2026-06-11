import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from model.xtf_validator import validate_xtf

def test_invalid_coord_axis_value():
    xtf_path = Path("input/xtf-validation/elektrische_anlagen_ueber_36kv/ail.xtf")
    ili_path = Path("input/xtf-validation/elektrische_anlagen_ueber_36kv/ElektrischeAnlagenNennspannungUeber36kV_V1.ili")
    result = validate_xtf(str(xtf_path), str(ili_path))
    # There should be at least one error about invalid COORD axis value (e.g., 'c' in <C1>c</C1>)
    errors = [e for e in result.errors if "Invalid numeric value for COORD axis" in str(e)]
    assert errors, f"Expected COORD axis numeric error, got: {[str(e) for e in result.errors]}"
