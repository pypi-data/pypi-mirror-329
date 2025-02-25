"""
Flow is the main interface for building and running flows.
"""

from __future__ import annotations

import re
import json
import inspect
from typing import Any, Callable, Sequence, TypeVar, Iterator
from threading import Lock

from . import _engine
from . import op, vector
from .typing import dump_type

class _NameBuilder:
    _existing_names: set[str]
    _next_name_index: dict[str, int]

    def __init__(self):
        self._existing_names = set()
        self._next_name_index = {}

    def build_name(self, name: str | None, /, prefix: str) -> str:
        """
        Build a name. If the name is None, generate a name with the given prefix.
        """
        if name is not None:
            self._existing_names.add(name)
            return name

        next_idx = self._next_name_index.get(prefix, 0)
        while True:
            name = f"{prefix}{next_idx}"
            next_idx += 1
            self._next_name_index[prefix] = next_idx
            if name not in self._existing_names:
                self._existing_names.add(name)
                return name


_WORD_BOUNDARY_RE = re.compile('(?<!^)(?=[A-Z])')
def _to_snake_case(name: str) -> str:
    return _WORD_BOUNDARY_RE.sub('_', name).lower()

def _create_data_slice(flow_builder: FlowBuilder, creator: Callable[[_engine.DataScopeRef | None, str | None], _engine.DataSlice], name: str | None = None) -> DataSlice:
    if name is None:
        return DataSlice(flow_builder,
                         lambda target: creator(target[0], target[1]) if target is not None else creator(None, None))
    else:
        return DataSlice(flow_builder, creator(None, name))


def _spec_kind(spec: Any) -> str:
    return spec.__class__.__name__

def _spec_json_dump(spec: Any) -> str:
    return json.dumps(spec.__dict__)

T = TypeVar('T')

class DataScope:
    """A data scope in a flow."""
    _flow_builder: FlowBuilder
    _engine_data_scope: _engine.DataScopeRef

    def __init__(self, flow: FlowBuilder, data_scope: _engine.DataScopeRef):
        self._flow_builder = flow
        self._engine_data_scope = data_scope

    def __str__(self):
        return str(self._engine_data_scope)

    def __repr__(self):
        return repr(self._engine_data_scope)

    def __getitem__(self, field_name: str) -> DataSlice:
        return DataSlice(self._flow_builder, self._flow_builder.internal_flow_builder.scope_field(self._engine_data_scope, field_name))

    def __setitem__(self, field_name: str, value: DataSlice):
        value.internal_attach_to_scope(self._engine_data_scope, field_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del self._engine_data_scope

    def add_collector(self, name: str | None = None) -> DataCollector:
        """
        Add a collector to the flow.
        """
        return DataCollector(
            self._flow_builder,
            self._engine_data_scope.add_collector(
                self._flow_builder._field_name_builder.build_name(name, prefix="_collector_")
            )
        )


class DataSlice:
    """A data slice is a slice of data in a flow. """
    _flow_builder: FlowBuilder

    _lazy_lock: Lock | None = None  # None means it's not lazy.
    _data_slice: _engine.DataSlice | None = None
    _data_slice_creator: Callable[[tuple[_engine.DataScopeRef, str] | None], _engine.DataSlice] | None = None

    def __init__(self, flow: FlowBuilder, data_slice: _engine.DataSlice | Callable[[tuple[_engine.DataScopeRef, str] | None], _engine.DataSlice]):
        self._flow_builder = flow

        if isinstance(data_slice, _engine.DataSlice):
            self._data_slice = data_slice
        else:
            self._lazy_lock = Lock()
            self._data_slice_creator = data_slice

    def __str__(self):
        return str(self.internal_data_slice)

    def __repr__(self):
        return repr(self.internal_data_slice)

    def __getitem__(self, field_name: str) -> DataSlice:
        field_slice = self.internal_data_slice.field(field_name)
        if field_slice is None:
            raise KeyError(field_name)
        return DataSlice(self._flow_builder, field_slice)

    @property
    def _engine_flow_builder(self) -> _engine.FlowBuilder:
        return self._flow_builder._engine_flow_builder  # pylint: disable=protected-access

    @property
    def _field_name_builder(self) -> _NameBuilder:
        return self._flow_builder._field_name_builder  # pylint: disable=protected-access

    @property
    def internal_data_slice(self) -> _engine.DataSlice:
        """
        Get the internal DataSlice.
        """
        if self._lazy_lock is None:
            if self._data_slice is None:
                raise ValueError("Data slice is not initialized")
            return self._data_slice
        else:
            if self._data_slice_creator is None:
                raise ValueError("Data slice creator is not initialized")
            with self._lazy_lock:
                if self._data_slice is None:
                    self._data_slice = self._data_slice_creator(None)
                return self._data_slice

    def internal_attach_to_scope(self, scope: _engine.DataScopeRef, field_name: str) -> None:
        """
        Attach the current data slice (if not yet attached) to the given scope.
        """
        if self._lazy_lock is not None:
            with self._lazy_lock:
                if self._data_slice_creator is None:
                    raise ValueError("Data slice creator is not initialized")
                if self._data_slice is None:
                    self._data_slice = self._data_slice_creator((scope, field_name))
                    return
        # TODO: We'll support this by an identity transformer or "aliasing" in the future.
        raise ValueError("DataSlice is already attached to a field")


    def entry(self) -> DataScope:
        """
        Return a scope representing each entry of the collection.
        """
        entry_scope = self.internal_data_slice.collection_entry_scope()
        return DataScope(self._flow_builder, entry_scope)

    def for_each(self, f: Callable[[DataScope], None]) -> None:
        """
        Apply a function to each element of the collection.
        """
        f(self.entry())

    def transform(self, spec, /, name: str | None = None) -> DataSlice:
        """
        Apply a transform to the data slice.
        """
        args = [(self.internal_data_slice, None)]
        return _create_data_slice(
            self._flow_builder,
            lambda target_scope, name: self._engine_flow_builder.transform(
                _spec_kind(spec),
                _spec_json_dump(spec),
                args,
                target_scope,
                self._field_name_builder.build_name(name, prefix=_to_snake_case(_spec_kind(spec))+'_'),
            ),
            name)

    def call(self, func: Callable[[DataSlice], T]) -> T:
        """
        Call a function with the data slice.
        """
        return func(self)

class DataCollector:
    """A data collector is used to collect data into a collector."""
    _flow_builder: FlowBuilder
    _engine_data_collector: _engine.DataCollector

    def __init__(self, flow: FlowBuilder, data_collector: _engine.DataCollector):
        self._flow_builder = flow
        self._engine_data_collector = data_collector

    def collect(self, **kwargs):
        """
        Collect data into the collector.
        """
        self._flow_builder.internal_flow_builder.collect(
            self._engine_data_collector, [(k, v.internal_data_slice) for k, v in kwargs.items()])

    def export(self, name: str, target_spec, /, *,
              primary_key_fields: Sequence[str] | None = None,
              vector_index: Sequence[tuple[str, vector.VectorSimilarityMetric]] = ()):
        """
        Export the collected data to the specified target.
        """
        index_options: dict[str, Any] = {}
        if primary_key_fields is not None:
            index_options["primary_key_fields"] = primary_key_fields
        index_options["vector_index_defs"] = [
            {"field_name": field_name, "metric": metric.value}
            for field_name, metric in vector_index]
        self._flow_builder.internal_flow_builder.export(
            name, _spec_kind(target_spec), _spec_json_dump(target_spec), json.dumps(index_options), self._engine_data_collector)


_flow_name_builder = _NameBuilder()

class FlowBuilder:
    """
    A flow builder is used to build a flow.
    """
    _engine_flow_builder: _engine.FlowBuilder
    _field_name_builder: _NameBuilder

    def __init__(self, /, name: str | None = None):
        flow_name = _flow_name_builder.build_name(name, prefix="_flow_")
        self._engine_flow_builder = _engine.FlowBuilder(flow_name)
        self._field_name_builder = _NameBuilder()

    def __str__(self):
        return str(self._engine_flow_builder)

    def __repr__(self):
        return repr(self._engine_flow_builder)

    @property
    def internal_flow_builder(self) -> _engine.FlowBuilder:
        return self._engine_flow_builder

    def add_source(self, spec, /, name: str | None = None) -> DataSlice:
        """
        Add a source to the flow.
        """
        return _create_data_slice(
            self,
            lambda target_scope, name: self._engine_flow_builder.add_source(
                _spec_kind(spec),
                _spec_json_dump(spec),
                target_scope,
                self._field_name_builder.build_name(name, prefix=_to_snake_case(_spec_kind(spec))+'_'),
            ),
            name
        )

    def build(self) -> Flow:
        """
        Build the flow.
        """
        flow = self._engine_flow_builder.build_flow()
        return Flow(lambda: flow)


class Flow:
    """
    A flow describes an indexing pipeline.
    """
    _lazy_engine_flow: Callable[[], _engine.Flow]

    def __init__(self, engine_flow_creator: Callable[[], _engine.Flow]):
        engine_flow = None
        lock = Lock()
        def _lazy_engine_flow() -> _engine.Flow:
            nonlocal engine_flow, lock
            if engine_flow is None:
                with lock:
                    if engine_flow is None:
                        engine_flow = engine_flow_creator()
            return engine_flow
        self._lazy_engine_flow = _lazy_engine_flow

    def __str__(self):
        return str(self._lazy_engine_flow())

    def __repr__(self):
        return repr(self._lazy_engine_flow())

    def update(self):
        """
        Update the indice defined by the flow.
        Once the function returns, the indice is fresh up to the moment when the function is called.
        """
        return self._lazy_engine_flow().update()

    def keep_updated(self):
        """
        Keep the indice up-to-date bassed on the source data changes.
        This is a blocking call.
        """
        raise NotImplementedError()

    def internal_flow(self) -> _engine.Flow:
        """
        Get the engine flow.
        """
        return self._lazy_engine_flow()
    

def _create_lazy_flow(name: str | None, fl_def: Callable[[FlowBuilder, DataScope], None]) -> Flow:
    """
    Create a flow without really building it yet.
    The flow will be built the first time when it's really needed.
    """
    def _create_engine_flow() -> _engine.Flow:
        flow_builder = FlowBuilder(name=name)
        root_scope = DataScope(flow_builder, flow_builder.internal_flow_builder.root_scope())
        fl_def(flow_builder, root_scope)
        return flow_builder.internal_flow_builder.build_flow()

    return Flow(_create_engine_flow)


_flows_lock = Lock()
_flows: dict[str, Flow] = {}

def add_flow_def(name: str, fl_def: Callable[[FlowBuilder, DataScope], None]) -> Flow:
    """Add a flow definition to the cocoindex library."""
    with _flows_lock:
        if name in _flows:
            raise KeyError(f"Flow with name {name} already exists")
        fl = _flows[name] = _create_lazy_flow(name, fl_def)
    return fl

def flow_def(name = None):
    """
    A decorator to wrap the flow definition.
    """
    return lambda fl_def: add_flow_def(name or fl_def.__name__, fl_def)

def flow_names() -> list[str]:
    """
    Get the names of all flows.
    """
    with _flows_lock:
        return list(_flows.keys())

def flow_by_name(name: str) -> Flow:
    """
    Get a flow by name.
    """
    with _flows_lock:
        return _flows[name]

def ensure_all_flows_built() -> None:
    """
    Ensure all flows are built.
    """
    with _flows_lock:
        for fl in _flows.values():
            fl.internal_flow()

_transient_flow_name_builder = _NameBuilder()
class TransientFlow:
    """
    A transient transformation flow that transforms in-memory data.
    """
    _engine_flow: _engine.TransientFlow

    def __init__(self, flow_fn: Callable[..., DataSlice], flow_arg_types: Sequence[Any], /, name: str | None = None):

        flow_builder = FlowBuilder(
            name=_transient_flow_name_builder.build_name(name, prefix="_transient_flow_"))
        sig = inspect.signature(flow_fn)
        if len(sig.parameters) != len(flow_arg_types):
            raise ValueError(
                f"Number of parameters in the flow function ({len(sig.parameters)}) "
                "does not match the number of argument types ({len(flow_arg_types)})")

        kwargs: dict[str, DataSlice] = {}
        for (param_name, param), param_type in zip(sig.parameters.items(), flow_arg_types):
            if param.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                  inspect.Parameter.KEYWORD_ONLY):
                raise ValueError(f"Parameter {param_name} is not a parameter can be passed by name")
            engine_ds = flow_builder._engine_flow_builder.add_direct_input(
                param_name, dump_type(param_type))
            kwargs[param_name] = DataSlice(flow_builder, engine_ds)

        output = flow_fn(**kwargs)
        flow_builder._engine_flow_builder.set_direct_output(output.internal_data_slice)
        self._engine_flow = flow_builder._engine_flow_builder.build_transient_flow()

    def __str__(self):
        return str(self._engine_flow)

    def __repr__(self):
        return repr(self._engine_flow)

    def internal_flow(self) -> _engine.TransientFlow:
        """
        Get the internal flow.
        """
        return self._engine_flow
