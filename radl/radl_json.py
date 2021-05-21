# IM - Infrastructure Manager
# Copyright (C) 2011 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

try:
    unicode
except:
    unicode = bytes

try:
    import json
except ImportError:
    import simplejson as json
try:
    import yaml
except ImportError:
    yaml = None

from .radl import Feature, Features, Aspect, RADL, configure, contextualize, contextualize_item, \
    deploy, SoftFeatures, RADLParseException, UnitToValue, description

try:
    import radl.radl as radl
except:
    import radl


def encode_simple(d):
    """Encode strings in basic python objects."""
    if isinstance(d, unicode):
        return d.encode()
    if isinstance(d, list):
        return list(map(encode_simple, d))
    if isinstance(d, dict):
        return dict([(encode_simple(k), encode_simple(v)) for k, v in d.items()])
    return d


def parse_radl(data):
    """
    Parse a RADL document in JSON.

    Args.:
    - data(str or list): document to parse.

    Return(RADL): RADL object.
    """
    if not isinstance(data, list):
        if os.path.isfile(data):
            f = open(data)
            data = "".join(f.readlines())
            f.close()
        data = json.loads(data)
    data = encode_simple(data)
    res = RADL()
    for aspect in [p_aspect(a) for a in data]:
        res.add(aspect)
    return res


def p_aspect(a):
    assert "class" in a
    if a["class"] == "configure":
        return p_configure(a)
    elif a["class"] == "contextualize":
        return p_contextualize(a)
    elif a["class"] == "deploy":
        return p_deploy(a)
    else:
        return p_cfeatures(a)


def p_configure(a):
    assert a["class"] == "configure"
    if a.get("reference", False):
        return configure(a["id"], reference=True)
    recipes = a["recipes"]
    if isinstance(recipes, str) and yaml:
        try:
            yaml.safe_load(recipes)
        except Exception as e:
            raise RADLParseException("Error parsing YAML: %s" % str(e))
    return configure(a["id"], recipes)


def p_contextualize(a):
    assert a["class"] == "contextualize"
    return contextualize([p_contextualize_item(i) for i in a.get("items", [])],
                         max_time=a.get("max_time", 0),
                         options=p_features(a.get("options", {})))


def p_contextualize_item(a):
    return contextualize_item(a["system"], a["configure"], a.get("step", 0), a.get("ctxt_tool", None))


def p_deploy(a):
    assert a["class"] == "deploy"
    return deploy(a["system"], a["vm_number"], a.get("cloud", None))


def p_cfeatures(a):
    assert a["class"] and a["id"]
    cls = getattr(radl, a["class"])
    if a.get("reference", False):
        return cls(a["id"], reference=True)
    return cls(a["id"], p_features(a))


def p_features(a):
    assert isinstance(a, dict)

    def val(k, v):
        if k == "softs":
            return [SoftFeatures(i.get("weight", 0), p_features(i.get("items", {}))) for i in v]
        elif k.endswith("_min") and isinstance(v, (int, float)):
            return [Feature(k[0:-4], ">=", v)]
        elif k.endswith("_max") and isinstance(v, (int, float)):
            return [Feature(k[0:-4], "<=", v)]
        elif isinstance(v, list):
            v = list(v)
            # disks urls can be a list
            if k.startswith("disk") and k.endswith("image.url"):
                return [Feature(k, "=", v)]
            else:
                return [Feature(k, "contains", p_feature(i)) for i in v]
        else:
            return [Feature(k, "=", p_feature(v))]
    return [i for k, v in a.items() if k != "class" and k != "id" for i in val(k, v)]


def p_feature(a):
    if isinstance(a, (int, float, str)):
        return a
    elif isinstance(a, unicode):
        return a.decode()
    elif isinstance(a, dict) and "class" in a:
        return p_cfeatures(a)
    elif isinstance(a, dict):
        return Features(p_features(a))
    assert False


def dump_radl(radl, enter="\n", indent="  "):
    """Dump a RADL document."""

    indent = len(indent) if enter else None
    sort_keys = indent is not None
    separators = (",", ":" if indent is None else ": ")
    return json.dumps(radlToSimple(radl), indent=indent, sort_keys=sort_keys, separators=separators)


def radlToSimple(radl_data):
    """
    Return a list of maps whose values are only other maps or lists.
    """

    aspects = (radl_data.ansible_hosts + radl_data.networks + radl_data.systems +
               radl_data.configures + radl_data.deploys)
    if radl_data.contextualize.items is not None or radl_data.contextualize.options is not None:
        aspects.append(radl_data.contextualize)
    if radl_data.description:
        aspects.append(radl_data.description)
    return [aspectToSimple(a) for a in aspects]


def aspectToSimple(a):
    if isinstance(a, Features):
        return cfeaturesToSimple(a)
    elif isinstance(a, configure):
        return configureToSimple(a)
    elif isinstance(a, contextualize):
        return contextualizeToSimple(a)
    elif isinstance(a, deploy):
        return deployToSimple(a)
    assert False


def configureToSimple(a):
    assert isinstance(a, configure)
    if a.reference or not a.recipes:
        return {"class": "configure", "id": a.name, "reference": True}
    else:
        return {"class": "configure", "id": a.name, "recipes": a.recipes}


def contextualizeToSimple(a):
    assert isinstance(a, contextualize)
    r = {"class": "contextualize"}
    if a.max_time:
        r["max_time"] = a.max_time
    if a.items:
        r["items"] = [contextualizeItemToSimple(i) for i in a.items.values()]
    if a.options:
        r["options"] = featuresToSimple(Features(a.options.values()))

    return r


def contextualizeItemToSimple(a):
    assert isinstance(a, contextualize_item)
    r = {"system": a.system, "configure": a.configure}
    if a.num:
        r["step"] = a.num
    if a.ctxt_tool:
        r["ctxt_tool"] = a.ctxt_tool
    return r


def deployToSimple(a):
    assert isinstance(a, deploy)
    r = {"class": "deploy", "system": a.id, "vm_number": a.vm_number}
    if a.cloud_id:
        r["cloud"] = a.cloud_id
    return r


def cfeaturesToSimple(a):
    assert isinstance(a, Features)
    r = {"class": a.__class__.__name__, "id": a.getId()}
    if a.reference:
        r["reference"] = True
        return r
    r.update(featuresToSimple(a))
    return r


def featuresToSimple(a):
    assert isinstance(a, Features)
    r = {}
    for k, v in a.props.items():
        if k == SoftFeatures.SOFT:
            r["softs"] = [{"weight": i.soft, "items": featuresToSimple(i)}
                          for i in a.props[SoftFeatures.SOFT]]
        elif isinstance(v, tuple):
            if v[0] and v[1] and v[0].value == v[1].value:
                r[k] = featureToSimple(v[0].value, v[0].unit)
            elif v[0]:
                r[k + "_min"] = featureToSimple(v[0].value, v[0].unit)
            elif v[1]:
                r[k + "_max"] = featureToSimple(v[1].value, v[1].unit)
        elif isinstance(v, (set, list)):
            r[k] = [featureToSimple(i.value, i.unit) for i in v]
        elif isinstance(v, dict):
            r[k] = [featureToSimple(i.value, i.unit) for i in v.values()]
        else:
            r[k] = featureToSimple(v.value, v.unit)
    return r


def featureToSimple(a, u):
    if isinstance(a, (int, float)):
        if u:
            return a * UnitToValue(u)
        else:
            return a
    if isinstance(a, str):
        return a
    elif isinstance(a, unicode):
        return a.decode()
    elif isinstance(a, list):
        return a
    elif isinstance(a, Aspect):
        return referenceToSimple(a)
    elif isinstance(a, Features):
        return featuresToSimple(a)
    assert False


def referenceToSimple(a):
    assert isinstance(a, Aspect)
    return {"class": a.__class__.__name__, "id": a.getId(), "reference": True}
