import json

from otlp_test_data import Config, sample_proto, sample_json


def test_same_json():
    assert json.loads(sample_json(Config())) == json.loads(sample_json(Config()))


def test_same_json_verbatim():
    assert sample_json(Config()) == sample_json(Config())


def test_same_proto_verbatim():
    assert sample_proto(Config()) == sample_proto(Config())
