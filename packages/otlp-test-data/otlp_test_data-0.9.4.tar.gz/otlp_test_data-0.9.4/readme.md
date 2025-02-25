# otlp-test-data

Produces OTLP data using OTEL instrumentation.

### Features

- fixed, configurable timestamps
- aims to cover as much of OTEL API as possible
- aims to cover all valid data types

### Limitations

- currently only tracing data is generated, PRs are welcome to add metrics and logs data
- data is generated in process, remote (forwarded) spans are not supported

### TODO

- Events
- Links
- Baggage
- Schemata, when https://github.com/open-telemetry/opentelemetry-python/pull/4359 lands
