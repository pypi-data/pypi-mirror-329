import asyncio
from typing import Any, Callable, List, Optional, Type, TypeVar, Union

from clients.admin import AdminClient
from clients.client import Client, new_client, new_client_raw
from clients.events import EventClient
from clients.rest_client import RestApi
from mtlibs.callable import ConcurrencyFunction, HatchetCallable
from pydantic import BaseModel
from typing_extensions import deprecated

from mtmai.context.context import Context
from mtmai.contracts.workflows_pb2 import (
    ConcurrencyLimitStrategy,
    CreateStepRateLimit,
    DesiredWorkerLabels,
    StickyStrategy,
)
from mtmai.features.cron import CronClient
from mtmai.features.scheduled import ScheduledClient
from mtmai.loader import ClientConfig, ConfigLoader
from mtmai.models._types import DesiredWorkerLabel, RateLimit
from mtmai.run_event_listener import RunEventListenerClient
from mtmai.worker.dispatcher.dispatcher import DispatcherClient
from mtmai.worker.worker import Worker, register_on_worker
from mtmai.workflow import ConcurrencyExpression, WorkflowMeta

T = TypeVar("T", bound=BaseModel)
TWorkflow = TypeVar("TWorkflow", bound=object)


def workflow(
    name: str = "",
    on_events: list[str] | None = None,
    on_crons: list[str] | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: Union[StickyStrategy.Value, None] = None,  # type: ignore[name-defined]
    default_priority: int | None = None,
    concurrency: ConcurrencyExpression | None = None,
    input_validator: Type[T] | None = None,
) -> Callable[[Type[TWorkflow]], WorkflowMeta]:
    on_events = on_events or []
    on_crons = on_crons or []

    def inner(cls: Type[TWorkflow]) -> WorkflowMeta:
        nonlocal name
        name = name or str(cls.__name__)

        setattr(cls, "on_events", on_events)
        setattr(cls, "on_crons", on_crons)
        setattr(cls, "name", name)
        setattr(cls, "version", version)
        setattr(cls, "timeout", timeout)
        setattr(cls, "schedule_timeout", schedule_timeout)
        setattr(cls, "sticky", sticky)
        setattr(cls, "default_priority", default_priority)
        setattr(cls, "concurrency_expression", concurrency)

        # Define a new class with the same name and bases as the original, but
        # with WorkflowMeta as its metaclass

        ## TODO: Figure out how to type this metaclass correctly
        setattr(cls, "input_validator", input_validator)

        return WorkflowMeta(name, cls.__bases__, dict(cls.__dict__))

    return inner


def step(
    name: str = "",
    timeout: str = "",
    parents: list[str] | None = None,
    retries: int = 0,
    rate_limits: list[RateLimit] | None = None,
    desired_worker_labels: dict[str, DesiredWorkerLabel] = {},
    backoff_factor: float | None = None,
    backoff_max_seconds: int | None = None,
) -> Callable[..., Any]:
    parents = parents or []

    def inner(func: Callable[[Context], Any]) -> Callable[[Context], Any]:
        limits = None
        if rate_limits:
            limits = [rate_limit._req for rate_limit in rate_limits or []]

        setattr(func, "_step_name", name.lower() or str(func.__name__).lower())
        setattr(func, "_step_parents", parents)
        setattr(func, "_step_timeout", timeout)
        setattr(func, "_step_retries", retries)
        setattr(func, "_step_rate_limits", retries)
        setattr(func, "_step_rate_limits", limits)
        setattr(func, "_step_backoff_factor", backoff_factor)
        setattr(func, "_step_backoff_max_seconds", backoff_max_seconds)

        def create_label(d: DesiredWorkerLabel) -> DesiredWorkerLabels:
            value = d["value"] if "value" in d else None
            return DesiredWorkerLabels(
                strValue=str(value) if not isinstance(value, int) else None,
                intValue=value if isinstance(value, int) else None,
                required=d["required"] if "required" in d else None,  # type: ignore[arg-type]
                weight=d["weight"] if "weight" in d else None,
                comparator=d["comparator"] if "comparator" in d else None,  # type: ignore[arg-type]
            )

        setattr(
            func,
            "_step_desired_worker_labels",
            {key: create_label(d) for key, d in desired_worker_labels.items()},
        )

        return func

    return inner


def on_failure_step(
    name: str = "",
    timeout: str = "",
    retries: int = 0,
    rate_limits: list[RateLimit] | None = None,
    backoff_factor: float | None = None,
    backoff_max_seconds: int | None = None,
) -> Callable[..., Any]:
    def inner(func: Callable[[Context], Any]) -> Callable[[Context], Any]:
        limits = None
        if rate_limits:
            limits = [
                CreateStepRateLimit(key=rate_limit.static_key, units=rate_limit.units)  # type: ignore[arg-type]
                for rate_limit in rate_limits or []
            ]

        setattr(
            func, "_on_failure_step_name", name.lower() or str(func.__name__).lower()
        )
        setattr(func, "_on_failure_step_timeout", timeout)
        setattr(func, "_on_failure_step_retries", retries)
        setattr(func, "_on_failure_step_rate_limits", limits)
        setattr(func, "_on_failure_step_backoff_factor", backoff_factor)
        setattr(func, "_on_failure_step_backoff_max_seconds", backoff_max_seconds)

        return func

    return inner


def concurrency(
    name: str = "",
    max_runs: int = 1,
    limit_strategy: ConcurrencyLimitStrategy = ConcurrencyLimitStrategy.CANCEL_IN_PROGRESS,
) -> Callable[..., Any]:
    def inner(func: Callable[[Context], Any]) -> Callable[[Context], Any]:
        setattr(
            func,
            "_concurrency_fn_name",
            name.lower() or str(func.__name__).lower(),
        )
        setattr(func, "_concurrency_max_runs", max_runs)
        setattr(func, "_concurrency_limit_strategy", limit_strategy)

        return func

    return inner


class HatchetRest:
    """
    Main client for interacting with the Hatchet API.

    This class provides access to various client interfaces and utility methods
    for working with Hatchet via the REST API,

    Attributes:
        rest (RestApi): Interface for REST API operations.
    """

    rest: RestApi

    def __init__(self, config: ClientConfig = ClientConfig()):
        _config: ClientConfig = ConfigLoader(".").load_client_config(config)
        self.rest = RestApi(_config.server_url, _config.token, _config.tenant_id)


class HatchetV1:
    """
    Main client for interacting with the Hatchet SDK.

    This class provides access to various client interfaces and utility methods
    for working with Hatchet workers, workflows, and steps.

    Attributes:
        cron (CronClient): Interface for cron trigger operations.

        admin (AdminClient): Interface for administrative operations.
        dispatcher (DispatcherClient): Interface for dispatching operations.
        event (EventClient): Interface for event-related operations.
        rest (RestApi): Interface for REST API operations.
    """

    _client: Client
    cron: CronClient
    scheduled: ScheduledClient

    @classmethod
    def from_environment(
        cls, defaults: ClientConfig = ClientConfig(), **kwargs: Any
    ) -> "Hatchet":
        return cls(client=new_client(defaults), **kwargs)

    @classmethod
    def from_config(cls, config: ClientConfig, **kwargs: Any) -> "Hatchet":
        return cls(client=new_client_raw(config), **kwargs)

    def __init__(
        self,
        debug: bool = False,
        client: Optional[Client] = None,
        config: ClientConfig = ClientConfig(),
    ):
        """
        Initialize a new Hatchet instance.

        Args:
            debug (bool, optional): Enable debug logging. Defaults to False.
            client (Optional[Client], optional): A pre-configured Client instance. Defaults to None.
            config (ClientConfig, optional): Configuration for creating a new Client. Defaults to ClientConfig().
        """
        if client is not None:
            self._client = client
        else:
            self._client = new_client(config, debug)

        # if debug:
        #     logger.setLevel(logging.DEBUG)

        self.cron = CronClient(self._client)
        self.scheduled = ScheduledClient(self._client)

    @property
    @deprecated(
        "Direct access to client is deprecated and will be removed in a future version. Use specific client properties (Hatchet.admin, Hatchet.dispatcher, Hatchet.event, Hatchet.rest) instead. [0.32.0]",
    )
    def client(self) -> Client:
        return self._client

    @property
    def admin(self) -> AdminClient:
        return self._client.admin

    @property
    def dispatcher(self) -> DispatcherClient:
        return self._client.dispatcher

    @property
    def event(self) -> EventClient:
        return self._client.event

    @property
    def rest(self) -> RestApi:
        return self._client.rest

    @property
    def listener(self) -> RunEventListenerClient:
        return self._client.listener

    @property
    def config(self) -> ClientConfig:
        return self._client.config

    @property
    def tenant_id(self) -> str:
        return self._client.config.tenant_id

    concurrency = staticmethod(concurrency)

    workflow = staticmethod(workflow)

    step = staticmethod(step)

    on_failure_step = staticmethod(on_failure_step)

    def worker(
        self, name: str, max_runs: int | None = None, labels: dict[str, str | int] = {}
    ) -> Worker:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        return Worker(
            name=name,
            max_runs=max_runs,
            labels=labels,
            config=self._client.config,
            debug=self._client.debug,
            owned_loop=loop is None,
        )


T = TypeVar("T")


def concurrency(
    name: str = "",
    max_runs: int = 1,
    limit_strategy: ConcurrencyLimitStrategy = ConcurrencyLimitStrategy.GROUP_ROUND_ROBIN,
):
    def inner(func: Callable[[Context], str]) -> ConcurrencyFunction:
        return ConcurrencyFunction(func, name, max_runs, limit_strategy)

    return inner


def function(
    name: str = "",
    auto_register: bool = True,
    on_events: list | None = None,
    on_crons: list | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: StickyStrategy = None,
    retries: int = 0,
    rate_limits: List[RateLimit] | None = None,
    desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
    concurrency: ConcurrencyFunction | None = None,
    on_failure: Optional["HatchetCallable"] = None,
    default_priority: int | None = None,
):
    def inner(func: Callable[[Context], T]) -> HatchetCallable[T]:
        return HatchetCallable(
            func=func,
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

    return inner


def durable(
    name: str = "",
    auto_register: bool = True,
    on_events: list | None = None,
    on_crons: list | None = None,
    version: str = "",
    timeout: str = "60m",
    schedule_timeout: str = "5m",
    sticky: StickyStrategy = None,
    retries: int = 0,
    rate_limits: List[RateLimit] | None = None,
    desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
    concurrency: ConcurrencyFunction | None = None,
    on_failure: HatchetCallable | None = None,
    default_priority: int | None = None,
):
    def inner(func: HatchetCallable) -> HatchetCallable:
        func.durable = True

        f = function(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        resp = f(func)

        resp.durable = True

        return resp

    return inner


def concurrency(
    name: str = "concurrency",
    max_runs: int = 1,
    limit_strategy: ConcurrencyLimitStrategy = ConcurrencyLimitStrategy.GROUP_ROUND_ROBIN,
):
    def inner(func: Callable[[Context], str]) -> ConcurrencyFunction:
        return ConcurrencyFunction(func, name, max_runs, limit_strategy)

    return inner


class Hatchet(HatchetV1):
    dag = staticmethod(workflow)
    concurrency = staticmethod(concurrency)

    functions: List[HatchetCallable] = []

    def function(
        self,
        name: str = "",
        auto_register: bool = True,
        on_events: list | None = None,
        on_crons: list | None = None,
        version: str = "",
        timeout: str = "60m",
        schedule_timeout: str = "5m",
        retries: int = 0,
        rate_limits: List[RateLimit] | None = None,
        desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
        concurrency: ConcurrencyFunction | None = None,
        on_failure: Optional["HatchetCallable"] = None,
        default_priority: int | None = None,
    ):
        resp = function(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        def wrapper(func: Callable[[Context], T]) -> HatchetCallable[T]:
            wrapped_resp = resp(func)

            if wrapped_resp.function_auto_register:
                self.functions.append(wrapped_resp)

            wrapped_resp.with_namespace(self._client.config.namespace)

            return wrapped_resp

        return wrapper

    def durable(
        self,
        name: str = "",
        auto_register: bool = True,
        on_events: list | None = None,
        on_crons: list | None = None,
        version: str = "",
        timeout: str = "60m",
        schedule_timeout: str = "5m",
        sticky: StickyStrategy = None,
        retries: int = 0,
        rate_limits: List[RateLimit] | None = None,
        desired_worker_labels: dict[str:DesiredWorkerLabel] = {},
        concurrency: ConcurrencyFunction | None = None,
        on_failure: Optional["HatchetCallable"] = None,
        default_priority: int | None = None,
    ) -> Callable[[HatchetCallable], HatchetCallable]:
        resp = durable(
            name=name,
            auto_register=auto_register,
            on_events=on_events,
            on_crons=on_crons,
            version=version,
            timeout=timeout,
            schedule_timeout=schedule_timeout,
            sticky=sticky,
            retries=retries,
            rate_limits=rate_limits,
            desired_worker_labels=desired_worker_labels,
            concurrency=concurrency,
            on_failure=on_failure,
            default_priority=default_priority,
        )

        def wrapper(func: Callable[[Context], T]) -> HatchetCallable[T]:
            wrapped_resp = resp(func)

            if wrapped_resp.function_auto_register:
                self.functions.append(wrapped_resp)

            wrapped_resp.with_namespace(self._client.config.namespace)

            return wrapped_resp

        return wrapper

    def worker(
        self, name: str, max_runs: int | None = None, labels: dict[str, str | int] = {}
    ):
        worker = Worker(
            name=name,
            max_runs=max_runs,
            labels=labels,
            config=self._client.config,
            debug=self._client.debug,
        )

        for func in self.functions:
            register_on_worker(func, worker)

        return worker
