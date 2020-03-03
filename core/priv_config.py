from ast import literal_eval
import copy
import os
import os.path as osp
import numpy as np
import yaml

"""config system.
This file specifies default config options. You should not
change values in this file. Instead, you should write a config file (in yaml)
and use merge_cfg_from_file(yaml_file) to load it and override the default
options.
"""


class AttrDict(dict):
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self[name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            self[name] = value

__C = AttrDict()
cfg_priv = __C

# __C.PET_ROOT = '/home/zhubin/ATM-stuff/Pet-dev'
__C.TASK = ('hop', 'turn_round', 'group', 'entry')

__C.HOP = AttrDict()
__C.HOP.CLASSES = ('hat', 'sunglasses', 'mask')
__C.HOP.DATA_PATH = ()

__C.TROUND = AttrDict()
__C.TROUND.TIMES = 3
__C.TROUND.TROUND_SENSE = 0.5
__C.TROUND.FRONT_SENSE = (0.8, 1.2)
__C.TROUND.DATA_PATH = ()

__C.GROUP = AttrDict()
__C.GROUP.MAX_NUM = 2
__C.GROUP.MIN_DISTANCE = 0
__C.GROUP.DATA_PATH = ()

__C.ENTRY = AttrDict()
__C.ENTRY.FREQUENCY = 3
__C.ENTRY.DATA_PATH = ()

__C.FACE_RECO = AttrDict()
# > 0.7 means same person, < 0.4 means a new person
__C.FACE_RECO.SIMILARITY_THRESHOLD = (0.2, 0.7)
__C.FACE_RECO.FEATURE_PATH = '/home/zhubin/ATM-stuff/PostProcess/task/task4/utils/face_lib/'


# ---------------------------------------------------------------------------- #
# Deprecated options
# If an option is removed from the code and you don't want to break existing
# yaml configs, you can add the full config key as a string to the set below.
# ---------------------------------------------------------------------------- #
_DEPCRECATED_KEYS = set()

# ---------------------------------------------------------------------------- #
# Renamed options
# If you rename a config option, record the mapping from the old name to the new
# name in the dictionary below. Optionally, if the type also changed, you can
# make the value a tuple that specifies first the renamed key and then
# instructions for how to edit the config file.
# ---------------------------------------------------------------------------- #
_RENAMED_KEYS = {
    'EXAMPLE.RENAMED.KEY': 'EXAMPLE.KEY',  # Dummy example to follow
    'PIXEL_MEAN': 'PIXEL_MEANS',
    'PIXEL_STD': 'PIXEL_STDS',
}


def merge_priv_cfg_to_objdet_cfg():
    cfg_list = []
    cfg_list.extend(['TEST.SCALE', __C.MODULES.OBJDET.TEST_SCALE])
    cfg_list.extend(['TEST.MAX_SIZE', __C.MODULES.OBJDET.TEST_MAX_SIZE])
    cfg_list.extend(['TEST.SOFT_NMS.ENABLED', __C.MODULES.OBJDET.SOFT_NMS.ENABLED])
    cfg_list.extend(['TEST.BBOX_VOTE.ENABLED', __C.MODULES.OBJDET.BBOX_VOTE.ENABLED])
    cfg_list.extend(['TEST.BBOX_VOTE.VOTE_TH', __C.MODULES.OBJDET.BBOX_VOTE.VOTE_TH])
    cfg_list.extend(['FAST_RCNN.DETECTIONS_PER_IMG', __C.MODULES.OBJDET.DETECTIONS_PER_IMG])
    cfg_list.extend(['RETINANET.DETECTIONS_PER_IMG', __C.MODULES.OBJDET.DETECTIONS_PER_IMG])
    cfg_list.extend(['FCOS.DETECTIONS_PER_IMG', __C.MODULES.OBJDET.DETECTIONS_PER_IMG])
    return cfg_list


def merge_priv_cfg_to_ssddet_cfg():
    cfg_list = []
    cfg_list.extend(['TEST.SOFT_NMS.ENABLED', __C.MODULES.OBJDET.SOFT_NMS.ENABLED])
    cfg_list.extend(['TEST.BBOX_VOTE.ENABLED', __C.MODULES.OBJDET.BBOX_VOTE.ENABLED])
    cfg_list.extend(['TEST.BBOX_VOTE.VOTE_TH', __C.MODULES.OBJDET.BBOX_VOTE.VOTE_TH])
    return cfg_list


def _merge_a_into_b(a, b, stack=None):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    assert isinstance(a, AttrDict), \
        '`a` (cur type {}) must be an instance of {}'.format(type(a), AttrDict)
    assert isinstance(b, AttrDict), \
        '`b` (cur type {}) must be an instance of {}'.format(type(b), AttrDict)

    for k, v_ in a.items():
        full_key = '.'.join(stack) + '.' + k if stack is not None else k
        # a must specify keys that are in b
        if k not in b:
            if _key_is_deprecated(full_key):
                continue
            elif _key_is_renamed(full_key):
                _raise_key_rename_error(full_key)
            else:
                raise KeyError('Non-existent config key: {}'.format(full_key))

        v = copy.deepcopy(v_)
        v = _decode_cfg_value(v)
        v = _check_and_coerce_cfg_value_type(v, b[k], k, full_key)

        # Recursively merge dicts
        if isinstance(v, AttrDict):
            try:
                stack_push = [k] if stack is None else stack + [k]
                _merge_a_into_b(v, b[k], stack=stack_push)
            except BaseException:
                raise
        else:
            b[k] = v


def merge_priv_cfg_from_file(filename):
    """Load a config file and merge it into the default options."""
    with open(filename, 'r') as f:
        yaml_cfg = AttrDict(yaml.load(f))
    _merge_a_into_b(yaml_cfg, __C)
    # update_cfg()


def merge_priv_cfg_from_cfg(cfg_other):
    """Merge `cfg_other` into the global config."""
    _merge_a_into_b(cfg_other, __C)


def merge_priv_cfg_from_list(cfg_list):
    """Merge config keys, values in a list (e.g., from command line) into the
    global config. For example, `cfg_list = ['TEST.NMS', 0.5]`.
    """
    assert len(cfg_list) % 2 == 0
    for full_key, v in zip(cfg_list[0::2], cfg_list[1::2]):
        if _key_is_deprecated(full_key):
            continue
        if _key_is_renamed(full_key):
            _raise_key_rename_error(full_key)
        key_list = full_key.split('.')
        d = __C
        for subkey in key_list[:-1]:
            assert subkey in d, 'Non-existent key: {}'.format(full_key)
            d = d[subkey]
        subkey = key_list[-1]
        assert subkey in d, 'Non-existent key: {}'.format(full_key)
        value = _decode_cfg_value(v)
        value = _check_and_coerce_cfg_value_type(
            value, d[subkey], subkey, full_key
        )
        d[subkey] = value


def _decode_cfg_value(v):
    """Decodes a raw config value (e.g., from a yaml config files or command
    line argument) into a Python object.
    """
    # Configs parsed from raw yaml will contain dictionary keys that need to be
    # converted to AttrDict objects
    if isinstance(v, dict):
        return AttrDict(v)
    # All remaining processing is only applied to strings
    if not isinstance(v, str):
        return v
    # Try to interpret `v` as a:
    #   string, number, tuple, list, dict, boolean, or None
    try:
        v = literal_eval(v)
    # The following two excepts allow v to pass through when it represents a
    # string.
    #
    # Longer explanation:
    # The type of v is always a string (before calling literal_eval), but
    # sometimes it *represents* a string and other times a data structure, like
    # a list. In the case that v represents a string, what we got back from the
    # yaml parser is 'foo' *without quotes* (so, not '"foo"'). literal_eval is
    # ok with '"foo"', but will raise a ValueError if given 'foo'. In other
    # cases, like paths (v = 'foo/bar' and not v = '"foo/bar"'), literal_eval
    # will raise a SyntaxError.
    except ValueError:
        pass
    except SyntaxError:
        pass
    return v


def _check_and_coerce_cfg_value_type(value_a, value_b, key, full_key):
    """Checks that `value_a`, which is intended to replace `value_b` is of the
    right type. The type is correct if it matches exactly or is one of a few
    cases in which the type can be easily coerced.
    """
    # The types must match (with some exceptions)
    type_b = type(value_b)
    type_a = type(value_a)
    if type_a is type_b:
        return value_a

    # Exceptions: numpy arrays, strings, tuple<->list
    if isinstance(value_b, np.ndarray):
        value_a = np.array(value_a, dtype=value_b.dtype)
    elif isinstance(value_b, str):
        value_a = str(value_a)
    elif isinstance(value_a, tuple) and isinstance(value_b, list):
        value_a = list(value_a)
    elif isinstance(value_a, list) and isinstance(value_b, tuple):
        value_a = tuple(value_a)
    else:
        raise ValueError(
            'Type mismatch ({} vs. {}) with values ({} vs. {}) for config '
            'key: {}'.format(type_b, type_a, value_b, value_a, full_key)
        )
    return value_a


def _key_is_deprecated(full_key):
    if full_key in _DEPCRECATED_KEYS:
        return True
    return False


def _key_is_renamed(full_key):
    return full_key in _RENAMED_KEYS


def _raise_key_rename_error(full_key):
    new_key = _RENAMED_KEYS[full_key]
    if isinstance(new_key, tuple):
        msg = ' Note: ' + new_key[1]
        new_key = new_key[0]
    else:
        msg = ''
    raise KeyError(
        'Key {} was renamed to {}; please update your config.{}'.
            format(full_key, new_key, msg)
    )
