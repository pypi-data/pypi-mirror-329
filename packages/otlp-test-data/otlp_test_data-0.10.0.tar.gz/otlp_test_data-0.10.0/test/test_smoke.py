import json

from otlp_test_data import sample_proto, sample_spans, sample_json


def test_spans():
    assert sample_spans()


def test_json():
    assert json.loads(sample_json())


def test_proto():
    assert sample_proto()
