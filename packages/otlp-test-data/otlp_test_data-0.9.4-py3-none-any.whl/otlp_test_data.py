from __future__ import annotations

import base64
import dataclasses
import json
import random
from typing import Sequence, TYPE_CHECKING
from typing_extensions import reveal_type as reveal_type  # temp

import freezegun
from google.protobuf.json_format import MessageToDict
from opentelemetry.exporter.otlp.proto.common._internal import trace_encoder
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

if TYPE_CHECKING:
    from google.protobuf.message import Message
    from opentelemetry.sdk.trace import ReadableSpan
    from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
        ExportTraceServiceRequest,
    )


@dataclasses.dataclass
class Config:
    start_time: str = "2020-01-01 00:00:00Z"
    random_seed: int = 42


time = None


def sample_proto(config: Config | None = None) -> bytes:
    return _proto_to_bytes(_spans_to_proto_object(sample_spans(config)))


def sample_json(config: Config | None = None) -> bytes:
    return _proto_to_json(_spans_to_proto_object(sample_spans(config)))


def sample_spans(config: Config | None = None) -> Sequence[ReadableSpan]:
    """Creates and finishes two spans, then returns them as a list."""
    global time
    config = config or Config()
    tracer_provider = TracerProvider()
    exporter = InMemorySpanExporter()
    tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = tracer_provider.get_tracer(__name__)

    with freezegun.freeze_time(config.start_time) as time:
        random.seed(config.random_seed)

        # FIXME the workload section is expected to grow a lot
        # TODO: attributes
        # bool, int, float, str
        # list[bool], ...
        # tuple[bool], ...
        # Sequence[bool], ... (maybe)
        with tracer.start_as_current_span("span-one"):
            time.tick()
        with tracer.start_as_current_span("span-two"):
            time.tick()

    return exporter.get_finished_spans()


def _spans_to_proto_object(spans: Sequence[ReadableSpan]) -> ExportTraceServiceRequest:
    return trace_encoder.encode_spans(spans)


def _proto_to_bytes(data: Message) -> bytes:
    return data.SerializePartialToString()


# FIXME: there are probably 3 different enumerated types in the API
def _proto_to_json(data: Message) -> bytes:
    dic = MessageToDict(data)

    for rs in dic["resourceSpans"]:
        for ss in rs["scopeSpans"]:
            for sp in ss["spans"]:
                for k in "parentSpanId spanId traceId".split():
                    if k in sp:
                        sp[k] = base64.b64decode(sp[k]).hex()
                sp["kind"] = {
                    "SPAN_KIND_UNSPECIFIED": 0,
                    "SPAN_KIND_INTERNAL": 1,
                    "SPAN_KIND_SERVER": 2,
                    "SPAN_KIND_CLIENT": 3,
                    "SPAN_KIND_PRODUCER": 4,
                    "SPAN_KIND_CONSUMER": 5,
                }[sp["kind"]]

    return json.dumps(dic).encode("utf-8")
