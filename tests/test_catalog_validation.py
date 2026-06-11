"""
Test XTF catalog reference validation.

This test suite validates that the XTF validator properly handles external
catalog files and validates references to catalog items.
"""

import pytest
from pathlib import Path
from model.xtf_validator import validate_xtf
from model.xtf_parser import XTFParser


def test_catalog_file_detection():
    """Test that catalog files are detected and loaded."""
    result = validate_xtf(
        "input/RoadTrafficCensus_V1_1_20240603.xtf",
        "input/RoadTrafficCensus_V1_1.ili"
    )
    
    # Check that catalog files were loaded
    found_catalog_msg = any("Found" in str(msg) and "catalog file" in str(msg) 
                           for msg in result.info)
    assert found_catalog_msg, "Should detect catalog files"
    
    # Check that catalog items were loaded
    loaded_msg = any("Loaded" in str(msg) and "catalog items" in str(msg) 
                    for msg in result.info)
    assert loaded_msg, "Should load catalog items"


def test_catalog_items_parsed():
    """Test that catalog items are correctly parsed."""
    parser = XTFParser()
    catalog_items = parser.parse_catalog_file("input/RoadTrafficCensus_Catalogue_V1_1.xml")
    
    # Should parse catalog items
    assert len(catalog_items) > 0, "Should parse catalog items"
    
    # Check specific known catalog items
    assert "ch.astra.roadtrafficcensus.100" in catalog_items
    assert "ch.astra.roadtrafficcensus.402" in catalog_items
    assert "ch.astra.roadtrafficcensus.501" in catalog_items
    
    # Verify structure of a catalog item
    item = catalog_items["ch.astra.roadtrafficcensus.100"]
    assert item.tid == "ch.astra.roadtrafficcensus.100"
    assert "Classification" in item.class_name
    assert "ItemId" in item.attributes


def test_valid_catalog_references():
    """Test that valid catalog references pass validation."""
    result = validate_xtf(
        "input/RoadTrafficCensus_V1_1_20240603.xtf",
        "input/RoadTrafficCensus_V1_1.ili"
    )
    
    # Should pass validation
    assert result.is_valid, f"Validation should pass: {result.errors}"
    
    # Should not have errors about missing catalog references
    catalog_ref_errors = [e for e in result.errors 
                         if "ch.astra.roadtrafficcensus" in str(e)]
    assert len(catalog_ref_errors) == 0, "Should not have catalog reference errors"


def test_invalid_catalog_reference():
    """Test that invalid catalog references are detected."""
    # Create a temporary XTF with invalid catalog reference
    import tempfile
    import xml.etree.ElementTree as ET
    
    # Parse the valid XTF
    tree = ET.parse("input/RoadTrafficCensus_V1_1_20240603.xtf")
    root = tree.getroot()
    
    # Find first MLocStatus reference and change it to invalid value
    ns = {'ili': 'http://www.interlis.ch/INTERLIS2.3'}
    datasection = root.find('.//ili:DATASECTION', ns) or root.find('.//*[local-name()="DATASECTION"]')
    
    if datasection:
        for basket in datasection:
            for obj in basket:
                for child in obj:
                    if 'MLocStatus' in child.tag:
                        # Find the Reference element
                        for grandchild in child:
                            for ggchild in grandchild:
                                if 'Reference' in ggchild.tag:
                                    # Change to invalid reference
                                    ggchild.set('REF', 'invalid.catalog.reference.999')
                                    break
                            break
                        break
                break
            break
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xtf', delete=False) as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
        temp_path = f.name
    
    try:
        # Validate the modified XTF
        result = validate_xtf(temp_path, "input/RoadTrafficCensus_V1_1.ili")
        
        # Should have an error about the invalid reference
        invalid_ref_errors = [e for e in result.errors 
                             if "invalid.catalog.reference.999" in str(e)]
        assert len(invalid_ref_errors) > 0, "Should detect invalid catalog reference"
    finally:
        # Clean up
        Path(temp_path).unlink(missing_ok=True)


def test_multiple_catalog_files():
    """Test that multiple catalog files are loaded."""
    result = validate_xtf(
        "input/RoadTrafficCensus_V1_1_20240603.xtf",
        "input/RoadTrafficCensus_V1_1.ili"
    )
    
    # Should load multiple catalog files
    catalog_count = sum(1 for msg in result.info 
                       if "Loaded" in str(msg) and "catalog items from" in str(msg))
    assert catalog_count > 1, f"Should load multiple catalog files, found {catalog_count}"
    
    # Total catalog items should be significant
    # The info messages show individual counts per file
    total_items = 0
    for msg in result.info:
        msg_str = str(msg)
        if "Loaded" in msg_str and "catalog items from" in msg_str:
            # Extract number from "Loaded X catalog items from..."
            parts = msg_str.split()
            for i, part in enumerate(parts):
                if part.isdigit():
                    total_items += int(part)
                    break
    
    assert total_items >= 16, f"Should load at least 16 catalog items, got {total_items}"


if __name__ == "__main__":
    # Run tests
    print("Testing catalog file detection...")
    test_catalog_file_detection()
    print(" Passed\n")
    
    print("Testing catalog items parsing...")
    test_catalog_items_parsed()
    print(" Passed\n")
    
    print("Testing valid catalog references...")
    test_valid_catalog_references()
    print(" Passed\n")
    
    print("Testing multiple catalog files...")
    test_multiple_catalog_files()
    print(" Passed\n")
    
    print("Testing invalid catalog reference...")
    test_invalid_catalog_reference()
    print(" Passed\n")
    
    print(" All catalog validation tests passed!")
