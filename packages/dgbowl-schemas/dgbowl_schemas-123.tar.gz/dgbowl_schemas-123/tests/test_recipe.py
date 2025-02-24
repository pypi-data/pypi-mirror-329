import pytest
import os
import yaml
import json
from dgbowl_schemas.dgpost import to_recipe
import ref_recipe


@pytest.mark.parametrize(
    "inpath, outdict",
    [
        ("le_1.yaml", ref_recipe.le_1),
        ("le_2.yaml", ref_recipe.le_2),
        ("lee_1.yaml", ref_recipe.lee_1),
        ("lee_2.yaml", ref_recipe.lee_2),
        ("les_1.yaml", ref_recipe.les_1),
        ("les_2.yaml", ref_recipe.les_2),
        ("les_3.yaml", ref_recipe.les_3),
        ("let_1.yaml", ref_recipe.let_1),
        ("let_2.yaml", ref_recipe.let_2),
        ("letp_1.yaml", ref_recipe.letp_1),
        ("lp_1.yaml", ref_recipe.lp_1),
        ("pivot_1.yaml", ref_recipe.pivot_1),
        ("pivot_2.yaml", ref_recipe.pivot_2),
    ],
)
def test_recipe_from_yml(inpath, outdict, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        indict = yaml.safe_load(infile)
    obj = to_recipe(**indict)
    if hasattr(obj, "model_dump"):
        ret = obj.model_dump(by_alias=True)
    else:
        ret = obj.dict(by_alias=True)
    assert outdict == ret


@pytest.mark.parametrize(
    "inpath, outdict",
    [("lets.json", ref_recipe.lets)],
)
def test_recipe_from_json(inpath, outdict, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        indict = json.load(infile)
    ret = to_recipe(**indict).dict(by_alias=True)
    assert outdict == ret


@pytest.mark.parametrize(
    "inpath",
    [
        ("le_1.yaml"),  # 1.0
        ("letp_1.yaml"),  # 1.0
    ],
)
def test_recipe_update_chain(inpath, datadir):
    os.chdir(datadir)
    with open(inpath, "r") as infile:
        jsdata = yaml.safe_load(infile)
    ret = to_recipe(**jsdata)
    while hasattr(ret, "update"):
        ret = ret.update()
    assert ret.version == "2.1"
