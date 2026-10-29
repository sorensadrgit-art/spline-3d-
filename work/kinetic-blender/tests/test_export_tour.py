"""Unit tests for export_tour.py utilities (visible, group_for)."""
import sys
from pathlib import Path
import pytest

# Ensure work/kinetic-blender directory is on sys.path
blender_dir = Path(__file__).resolve().parent.parent
if str(blender_dir) not in sys.path:
    sys.path.insert(0, str(blender_dir))

from export_tour import visible, group_for


class MockCollection:
    def __init__(self, name: str, hide_render: bool = False):
        self.name = name
        self.hide_render = hide_render


class MockMatrixTranslation:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z


class MockMatrixWorld:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.translation = MockMatrixTranslation(x, y, z)


class MockObject:
    def __init__(
        self,
        name: str = "TestObject",
        hide_render: bool = False,
        collections: list = None,
        x: float = 0.0,
    ):
        self.name = name
        self.hide_render = hide_render
        self.users_collection = collections if collections is not None else []
        self.matrix_world = MockMatrixWorld(x=x)


# --- Tests for visible(ob) ---


def test_visible_returns_true_when_object_and_collection_visible():
    ob = MockObject(
        hide_render=False,
        collections=[MockCollection("Scene Collection", hide_render=False)]
    )
    assert visible(ob) is True


def test_visible_returns_false_when_object_is_hidden():
    ob = MockObject(
        hide_render=True,
        collections=[MockCollection("Scene Collection", hide_render=False)]
    )
    assert visible(ob) is False


def test_visible_returns_false_when_all_collections_hidden():
    ob = MockObject(
        hide_render=False,
        collections=[
            MockCollection("Col1", hide_render=True),
            MockCollection("Col2", hide_render=True),
        ]
    )
    assert visible(ob) is False


def test_visible_returns_false_when_no_collections():
    ob = MockObject(
        hide_render=False,
        collections=[]
    )
    assert visible(ob) is False


def test_visible_returns_true_when_at_least_one_collection_visible():
    ob = MockObject(
        hide_render=False,
        collections=[
            MockCollection("HiddenCol", hide_render=True),
            MockCollection("VisibleCol", hide_render=False),
        ]
    )
    assert visible(ob) is True


def test_visible_returns_false_when_both_object_and_collections_hidden():
    ob = MockObject(
        hide_render=True,
        collections=[MockCollection("HiddenCol", hide_render=True)]
    )
    assert visible(ob) is False


# --- Tests for group_for(ob) ---


def test_group_for_plants():
    ob = MockObject(collections=[MockCollection("08_PLANT_MONSTERA")])
    assert group_for(ob) == "plants"


def test_group_for_exterior():
    ob = MockObject(collections=[MockCollection("02_EXTERIOR_MOUNTAIN")])
    assert group_for(ob) == "exterior"


def test_group_for_lounge_by_lounge_keyword():
    ob = MockObject(collections=[MockCollection("07_LOUNGE_SEATING")])
    assert group_for(ob) == "lounge"


def test_group_for_lounge_by_furniture_keyword():
    ob = MockObject(collections=[MockCollection("FURNITURE_DESKS")])
    assert group_for(ob) == "lounge"


def test_group_for_workstation():
    ob = MockObject(collections=[MockCollection("01_WORKSTATION_MAIN")])
    assert group_for(ob) == "workstation"


def test_group_for_motion_zone():
    ob = MockObject(collections=[MockCollection("03_ZONE_01_MOTION_SYSTEMS")])
    assert group_for(ob) == "motion"


def test_group_for_clinical_zone():
    ob = MockObject(collections=[MockCollection("04_ZONE_02_CLINICAL_THINKING")])
    assert group_for(ob) == "clinical"


def test_group_for_engineering_zone():
    ob = MockObject(collections=[MockCollection("05_ZONE_03_CREATIVE_ENGINEERING")])
    assert group_for(ob) == "engineering"


def test_group_for_projects_zone():
    ob = MockObject(collections=[MockCollection("06_ZONE_04_PROJECTS")])
    assert group_for(ob) == "projects"


@pytest.mark.parametrize(
    "x,expected_group",
    [
        (-10.0, "motion"),
        (-6.1, "motion"),
        (-6.0, "clinical"),
        (-4.0, "clinical"),
        (-2.81, "clinical"),
        (-2.8, "engineering"),
        (0.0, "engineering"),
        (7.3, "engineering"),
        (7.31, "projects"),
        (15.0, "projects"),
    ],
)
def test_group_for_zone_details_branching(x, expected_group):
    ob = MockObject(
        collections=[MockCollection("ZONE_DETAILS_PROPS")],
        x=x,
    )
    assert group_for(ob) == expected_group


def test_group_for_priority_rules():
    # PLANT check is prioritized over ZONE_01
    ob_plant_zone = MockObject(collections=[MockCollection("PLANT_ZONE_01")])
    assert group_for(ob_plant_zone) == "plants"

    # EXTERIOR check is prioritized over FURNITURE
    ob_ext_furn = MockObject(collections=[MockCollection("EXTERIOR_FURNITURE")])
    assert group_for(ob_ext_furn) == "exterior"

    # LOUNGE is prioritized over WORKSTATION
    ob_lounge_work = MockObject(collections=[MockCollection("LOUNGE_WORKSTATION")])
    assert group_for(ob_lounge_work) == "lounge"

    # WORKSTATION is prioritized over ZONE_01
    ob_work_zone = MockObject(collections=[MockCollection("WORKSTATION_ZONE_01")])
    assert group_for(ob_work_zone) == "workstation"

    # ZONE_01 is prioritized over ZONE_DETAILS
    ob_zone_details = MockObject(collections=[MockCollection("ZONE_01_ZONE_DETAILS")])
    assert group_for(ob_zone_details) == "motion"


def test_group_for_multiple_collections_matches_first_valid():
    ob = MockObject(
        collections=[
            MockCollection("ARCHITECTURE_BASE"),
            MockCollection("04_ZONE_02_CLINICAL"),
        ]
    )
    assert group_for(ob) == "clinical"


def test_group_for_architecture_fallback_for_unmatched_collection():
    ob = MockObject(collections=[MockCollection("01_ARCHITECTURE")])
    assert group_for(ob) == "architecture"


def test_group_for_architecture_fallback_when_empty_collections():
    ob = MockObject(collections=[])
    assert group_for(ob) == "architecture"
