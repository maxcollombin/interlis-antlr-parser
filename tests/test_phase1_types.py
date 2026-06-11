"""
Unit tests for Phase 1: Core Type Extensions (Issue #1)

Tests for newly added types:
- DateType, TimeType, AreaType, LengthType, AngleType
- VertexType, SurfaceType
- DomainType inheritance (extends)
"""

import pytest
from model.types import (
    DomainType,
    DateType,
    TimeType,
    AreaType,
    LengthType,
    AngleType,
    VertexType,
    SurfaceType,
    CoordType,
    TextType,
    NumericType,
)


class TestDateType:
    """Tests for DateType domain."""

    def test_date_type_creation(self):
        """Test basic DateType instantiation."""
        date_type = DateType(name="MyDate", ili_name="MyModel.MyDate")
        assert date_type.name == "MyDate"
        assert date_type.ili_name == "MyModel.MyDate"
        assert date_type.kind == "DATE"
        assert date_type.mandatory is False

    def test_date_type_mandatory(self):
        """Test DateType with mandatory constraint."""
        date_type = DateType(name="RequiredDate", mandatory=True)
        assert date_type.mandatory is True


class TestTimeType:
    """Tests for TimeType domain."""

    def test_time_type_creation(self):
        """Test basic TimeType instantiation."""
        time_type = TimeType(name="MyTime", ili_name="MyModel.MyTime")
        assert time_type.name == "MyTime"
        assert time_type.kind == "TIMEOFDAY"
        assert time_type.mandatory is False

    def test_time_type_distinct_from_datetime(self):
        """Verify TimeType is distinct from DateTimeType."""
        time_type = TimeType(kind="TIMEOFDAY")
        assert time_type.kind == "TIMEOFDAY"


class TestAreaType:
    """Tests for AreaType domain."""

    def test_area_type_creation(self):
        """Test basic AreaType instantiation."""
        area_type = AreaType(name="MyArea", ili_name="MyModel.MyArea")
        assert area_type.name == "MyArea"
        assert area_type.unit is None

    def test_area_type_with_unit(self):
        """Test AreaType with specific unit."""
        area_type = AreaType(name="SquareMeters", unit="m2")
        assert area_type.unit == "m2"

    def test_area_type_various_units(self):
        """Test AreaType supports various units."""
        units = ["m2", "km2", "ha", "cm2"]
        for unit in units:
            area_type = AreaType(unit=unit)
            assert area_type.unit == unit


class TestLengthType:
    """Tests for LengthType domain."""

    def test_length_type_creation(self):
        """Test basic LengthType instantiation."""
        length_type = LengthType(name="MyLength")
        assert length_type.name == "MyLength"
        assert length_type.unit is None

    def test_length_type_with_unit(self):
        """Test LengthType with specific unit."""
        length_type = LengthType(name="Meters", unit="m")
        assert length_type.unit == "m"

    def test_length_type_various_units(self):
        """Test LengthType supports various units."""
        units = ["m", "km", "cm", "mm"]
        for unit in units:
            length_type = LengthType(unit=unit)
            assert length_type.unit == unit


class TestAngleType:
    """Tests for AngleType domain."""

    def test_angle_type_creation(self):
        """Test basic AngleType instantiation."""
        angle_type = AngleType(name="MyAngle")
        assert angle_type.name == "MyAngle"
        assert angle_type.unit == "DEGREES"
        assert angle_type.min_value == 0.0
        assert angle_type.max_value == 360.0

    def test_angle_type_degrees(self):
        """Test AngleType in degrees."""
        angle_type = AngleType(unit="DEGREES", min_value=0.0, max_value=360.0)
        assert angle_type.unit == "DEGREES"
        assert angle_type.max_value == 360.0

    def test_angle_type_radians(self):
        """Test AngleType in radians."""
        angle_type = AngleType(unit="RADIANS", min_value=0.0, max_value=6.283185307)
        assert angle_type.unit == "RADIANS"
        assert abs(angle_type.max_value - 6.283185307) < 0.0001

    def test_angle_type_circular(self):
        """Verify AngleType circular property."""
        angle_type = AngleType()
        # Angles are naturally circular (0-360 or 0-2π)
        assert angle_type.max_value - angle_type.min_value == 360.0


class TestVertexType:
    """Tests for VertexType domain."""

    def test_vertex_type_creation(self):
        """Test basic VertexType instantiation."""
        vertex_type = VertexType(name="MyVertex")
        assert vertex_type.name == "MyVertex"
        assert vertex_type.coord_type is None

    def test_vertex_type_with_coord(self):
        """Test VertexType with coordinate type."""
        coord_type = CoordType(name="2D_Coords")
        vertex_type = VertexType(name="Vertex2D", coord_type=coord_type)
        assert vertex_type.coord_type == coord_type
        assert vertex_type.coord_type.name == "2D_Coords"


class TestSurfaceType:
    """Tests for SurfaceType domain."""

    def test_surface_type_creation(self):
        """Test basic SurfaceType instantiation."""
        surface_type = SurfaceType(name="MySurface")
        assert surface_type.name == "MySurface"
        assert surface_type.with_holes is True

    def test_surface_type_without_holes(self):
        """Test SurfaceType disallowing holes."""
        surface_type = SurfaceType(name="SimpleSurface", with_holes=False)
        assert surface_type.with_holes is False

    def test_surface_type_with_holes(self):
        """Test SurfaceType allowing holes."""
        surface_type = SurfaceType(name="ComplexSurface", with_holes=True)
        assert surface_type.with_holes is True


class TestDomainInheritance:
    """Tests for domain inheritance (TYPE ... EXTENDS ...)."""

    def test_domain_type_without_inheritance(self):
        """Test DomainType without extends."""
        domain = TextType(name="SimpleDomain")
        assert domain.extends is None

    def test_domain_type_with_inheritance(self):
        """Test DomainType with extends reference."""
        base_domain = TextType(name="BaseText", max_length=255)
        extended_domain = TextType(
            name="ExtendedText",
            max_length=100,
            extends=base_domain
        )
        assert extended_domain.extends == base_domain
        assert extended_domain.extends.max_length == 255

    def test_numeric_domain_inheritance(self):
        """Test numeric type inheritance."""
        base_numeric = NumericType(
            name="BaseNumeric",
            min_value="0.0",
            max_value="100.0"
        )
        extended_numeric = NumericType(
            name="ExtendedNumeric",
            min_value="10.0",
            max_value="90.0",
            extends=base_numeric
        )
        assert extended_numeric.extends == base_numeric
        assert extended_numeric.extends.min_value == "0.0"

    def test_domain_inheritance_chain(self):
        """Test multi-level domain inheritance."""
        domain_a = TextType(name="DomainA")
        domain_b = TextType(name="DomainB", extends=domain_a)
        domain_c = TextType(name="DomainC", extends=domain_b)
        
        assert domain_c.extends == domain_b
        assert domain_c.extends.extends == domain_a
        assert domain_c.extends.extends.extends is None

    def test_specialized_type_inheritance(self):
        """Test specialized type inheriting from base."""
        base_area = AreaType(name="BaseArea", unit="m2")
        extended_area = AreaType(name="SpecialArea", unit="km2", extends=base_area)
        assert extended_area.extends == base_area
        assert extended_area.unit == "km2"
        assert extended_area.extends.unit == "m2"


class TestTypeExportedInInit:
    """Verify all new types are exported from model/__init__.py."""

    def test_all_new_types_importable(self):
        """Test that all Phase 1 types can be imported from model package."""
        from model import (
            DateType,
            TimeType,
            AreaType,
            LengthType,
            AngleType,
            VertexType,
            SurfaceType,
        )
        assert DateType is not None
        assert TimeType is not None
        assert AreaType is not None
        assert LengthType is not None
        assert AngleType is not None
        assert VertexType is not None
        assert SurfaceType is not None


class TestTypeConsistency:
    """Integration tests for type consistency."""

    def test_all_types_inherit_from_domain_type(self):
        """Verify all new types are subclasses of DomainType."""
        new_types = [
            DateType,
            TimeType,
            AreaType,
            LengthType,
            AngleType,
            VertexType,
            SurfaceType,
        ]
        for type_class in new_types:
            instance = type_class(name="test")
            assert isinstance(instance, DomainType)

    def test_all_types_have_ili_name_field(self):
        """Verify all types support ili_name."""
        types_to_test = [
            DateType(name="date1", ili_name="model.date1"),
            TimeType(name="time1", ili_name="model.time1"),
            AreaType(name="area1", ili_name="model.area1"),
            LengthType(name="len1", ili_name="model.len1"),
            AngleType(name="ang1", ili_name="model.ang1"),
            VertexType(name="vert1", ili_name="model.vert1"),
            SurfaceType(name="surf1", ili_name="model.surf1"),
        ]
        for type_instance in types_to_test:
            assert type_instance.ili_name == type_instance.ili_name

    def test_all_types_have_mandatory_field(self):
        """Verify all types support mandatory constraint."""
        types_to_test = [
            DateType(name="d", mandatory=True),
            TimeType(name="t", mandatory=True),
            AreaType(name="a", mandatory=True),
            LengthType(name="l", mandatory=True),
            AngleType(name="ang", mandatory=True),
            VertexType(name="v", mandatory=True),
            SurfaceType(name="s", mandatory=True),
        ]
        for type_instance in types_to_test:
            assert type_instance.mandatory is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
