from abcli.tests.test_env import test_abcli_env
from blue_objects.tests.test_env import test_blue_objects_env

from roofai import env


def test_required_env():
    test_abcli_env()
    test_blue_objects_env()


def test_blue_plugin_env():
    assert env.GOOGLE_MAPS_API_KEY

    assert env.TEST_roofAI_ingest_AIRS_v1
    assert env.TEST_roofAI_ingest_AIRS_v2
    assert env.TEST_roofAI_ingest_CamVid_v1

    assert env.TEST_roofAI_semseg_model_AIRS_full_v1
    assert env.TEST_roofAI_semseg_model_AIRS_full_v2
    assert env.TEST_roofAI_semseg_model_CamVid_v1

    assert env.ROOFAI_AIRS_CACHE_OBJECT_NAME

    assert isinstance(env.ROOFAI_TEST_GOOGLE_MAPS_LAT, float)
    assert isinstance(env.ROOFAI_TEST_GOOGLE_MAPS_LON, float)

    assert isinstance(env.ROOFAI_TEST_GOOGLE_MAPS_HOUSE_LAT, float)
    assert isinstance(env.ROOFAI_TEST_GOOGLE_MAPS_HOUSE_LON, float)

    assert env.ROBOFLOW_API_KEY

    assert env.ROOFAI_DEFAULT_GOOGLE_MAPS_MODEL
