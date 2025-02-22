import asyncio
import contextlib
import datetime
import enum
import logging
import time
from dataclasses import dataclass, field
from functools import cached_property

import bittensor

from compute_horde.base.docker import DockerRunOptionsPreset
from compute_horde.base.output_upload import OutputUpload
from compute_horde.base.volume import Volume
from compute_horde.base_requests import BaseRequest
from compute_horde.executor_class import EXECUTOR_CLASS, ExecutorClass
from compute_horde.miner_client.base import (
    AbstractMinerClient,
    ErrorCallback,
    UnsupportedMessageReceived,
)
from compute_horde.mv_protocol import miner_requests, validator_requests
from compute_horde.mv_protocol.miner_requests import (
    BaseMinerRequest,
    UnauthorizedError,
    V0AcceptJobRequest,
    V0DeclineJobRequest,
    V0ExecutorFailedRequest,
    V0ExecutorManifestRequest,
    V0ExecutorReadyRequest,
    V0JobFailedRequest,
    V0JobFinishedRequest,
    V0MachineSpecsRequest,
    V0StreamingJobReadyRequest,
)
from compute_horde.mv_protocol.validator_requests import (
    AuthenticationPayload,
    V0AuthenticateRequest,
    V0InitialJobRequest,
    V0JobAcceptedReceiptRequest,
    V0JobFinishedReceiptRequest,
    V0JobRequest,
)
from compute_horde.receipts.models import JobAcceptedReceipt, JobFinishedReceipt, JobStartedReceipt
from compute_horde.receipts.schemas import (
    JobAcceptedReceiptPayload,
    JobFinishedReceiptPayload,
    JobStartedReceiptPayload,
)
from compute_horde.transport import AbstractTransport, TransportConnectionError, WSTransport
from compute_horde.utils import MachineSpecs, Timer, sign_blob

logger = logging.getLogger(__name__)

JOB_STARTED_RECEIPT_MIN_TTL = 30


class OrganicMinerClient(AbstractMinerClient):
    """
    Miner client to run organic job on a miner.
    This client is used by validators to connect to prod miners.
    Others can use this client to connect to their locally running miners to run jobs.

    The usual usage of this miner client is as follows::

        client = OrganicMinerClient(...)
        async with client:
            await client.send_model(V0InitialJobRequest(...))
            msg = await client.miner_ready_or_declining_future
            # handle msg

            await client.send_model(V0JobRequest(...))
            msg = client.miner_finished_or_failed_future
            # handle msg

    Note that the waiting on the response futures should properly be handled with timeouts
    (with ``asyncio.timeout()``, ``asyncio.wait_for()`` etc.).
    """

    def __init__(
        self,
        miner_hotkey: str,
        miner_address: str,
        miner_port: int,
        job_uuid: str,
        my_keypair: bittensor.Keypair,
        transport: AbstractTransport | None = None,
    ) -> None:
        self.job_uuid = job_uuid

        self.miner_hotkey = miner_hotkey
        self.miner_address = miner_address
        self.miner_port = miner_port
        self.my_keypair = my_keypair

        loop = asyncio.get_running_loop()
        self.miner_manifest = loop.create_future()
        self.online_executor_count = 0

        # for waiting on miner responses
        self.miner_accepting_or_declining_future: asyncio.Future[
            V0AcceptJobRequest | V0DeclineJobRequest
        ] = loop.create_future()
        self.miner_accepting_or_declining_timestamp: int = 0

        self.executor_ready_or_failed_future: asyncio.Future[
            V0ExecutorReadyRequest | V0ExecutorFailedRequest
        ] = loop.create_future()
        self.executor_ready_or_failed_timestamp: int = 0

        self.streaming_job_ready_or_not_future: asyncio.Future[
            V0StreamingJobReadyRequest | miner_requests.V0StreamingJobNotReadyRequest
        ] = loop.create_future()
        self.streaming_job_ready_or_not_timestamp: int = 0

        self.miner_finished_or_failed_future: asyncio.Future[
            V0JobFailedRequest | V0JobFinishedRequest
        ] = loop.create_future()
        self.miner_finished_or_failed_timestamp: int = 0

        self.miner_machine_specs: MachineSpecs | None = None

        name = f"{miner_hotkey}({miner_address}:{miner_port})"
        transport = transport or WSTransport(name, self.miner_url())
        super().__init__(name, transport)

    @cached_property
    def my_hotkey(self) -> str:
        return str(self.my_keypair.ss58_address)

    def miner_url(self) -> str:
        return (
            f"ws://{self.miner_address}:{self.miner_port}/v0.1/validator_interface/{self.my_hotkey}"
        )

    def accepted_request_type(self) -> type[BaseRequest]:
        return BaseMinerRequest

    def incoming_generic_error_class(self) -> type[BaseRequest]:
        return miner_requests.GenericError

    def outgoing_generic_error_class(self) -> type[BaseRequest]:
        return validator_requests.GenericError

    def build_outgoing_generic_error(self, msg: str):
        return validator_requests.GenericError(details=msg)

    async def notify_generic_error(self, msg: BaseRequest) -> None:
        """This method is called when miner sends a generic error message"""

    async def notify_unauthorized_error(self, msg: UnauthorizedError) -> None:
        """This method is called when miner refuses the authentication message"""

    async def notify_receipt_failure(self, comment: str) -> None:
        """This method is called when sending receipts to miner fails"""

    async def notify_send_failure(self, msg: str) -> None:
        """This method is called when sending messages to miner fails"""

    async def notify_job_accepted(self, msg: V0AcceptJobRequest) -> None:
        """This method is called when miner sends job accepted message"""

    async def notify_executor_ready(self, msg: V0ExecutorReadyRequest) -> None:
        """This method is called when miner sends executor ready message"""

    async def handle_manifest_request(self, msg: V0ExecutorManifestRequest) -> None:
        try:
            self.miner_manifest.set_result(msg.manifest)
        except asyncio.InvalidStateError:
            logger.warning(f"Received manifest from {msg} but future was already set")

    async def handle_machine_specs_request(self, msg: V0MachineSpecsRequest) -> None:
        self.miner_machine_specs = msg.specs

    async def handle_message(self, msg: BaseRequest) -> None:
        if isinstance(msg, self.incoming_generic_error_class()):
            logger.warning(
                f"Received error message from miner {self.miner_name}: {msg.model_dump_json()}"
            )
            await self.notify_generic_error(msg)
            return
        elif isinstance(msg, UnauthorizedError):
            logger.error(f"Unauthorized in {self.miner_name}: {msg.code}, details: {msg.details}")
            await self.notify_unauthorized_error(msg)
            return
        elif isinstance(msg, V0ExecutorManifestRequest):
            await self.handle_manifest_request(msg)
            return

        if (received_job_uuid := getattr(msg, "job_uuid", self.job_uuid)) != self.job_uuid:
            logger.warning(
                f"Received msg from {self.miner_name} for a different job (expected job {self.job_uuid}, got job {received_job_uuid}): {msg}"
            )
            return

        if isinstance(msg, V0AcceptJobRequest | V0DeclineJobRequest):
            try:
                self.miner_accepting_or_declining_future.set_result(msg)
                self.miner_accepting_or_declining_timestamp = int(time.time())
            except asyncio.InvalidStateError:
                logger.warning(f"Received {msg} from {self.miner_name} but future was already set")
        elif isinstance(msg, V0ExecutorReadyRequest | V0ExecutorFailedRequest):
            try:
                self.executor_ready_or_failed_future.set_result(msg)
                self.executor_ready_or_failed_timestamp = int(time.time())
            except asyncio.InvalidStateError:
                logger.warning(f"Received {msg} from {self.miner_name} but future was already set")
        elif isinstance(
            msg, V0StreamingJobReadyRequest | miner_requests.V0StreamingJobNotReadyRequest
        ):
            try:
                self.streaming_job_ready_or_not_future.set_result(msg)
                self.streaming_job_ready_or_not_timestamp = int(time.time())
            except asyncio.InvalidStateError:
                logger.warning(f"Received {msg} from {self.miner_name} but future was already set")
        elif isinstance(msg, V0JobFailedRequest | V0JobFinishedRequest):
            try:
                self.miner_finished_or_failed_future.set_result(msg)
                self.miner_finished_or_failed_timestamp = int(time.time())
            except asyncio.InvalidStateError:
                logger.warning(f"Received {msg} from {self.miner_name} but future was already set")
        elif isinstance(msg, V0MachineSpecsRequest):
            await self.handle_machine_specs_request(msg)
        else:
            raise UnsupportedMessageReceived(msg)

    def generate_authentication_message(self) -> V0AuthenticateRequest:
        payload = AuthenticationPayload(
            validator_hotkey=self.my_hotkey,
            miner_hotkey=self.miner_hotkey,
            timestamp=int(time.time()),
        )
        return V0AuthenticateRequest(
            payload=payload, signature=sign_blob(self.my_keypair, payload.blob_for_signing())
        )

    def generate_job_started_receipt_message(
        self,
        executor_class: ExecutorClass,
        max_timeout: int,
        ttl: int,
    ) -> tuple[JobStartedReceiptPayload, str]:
        receipt_payload = JobStartedReceiptPayload(
            job_uuid=self.job_uuid,
            miner_hotkey=self.miner_hotkey,
            validator_hotkey=self.my_hotkey,
            timestamp=datetime.datetime.now(datetime.UTC),
            executor_class=executor_class,
            max_timeout=max_timeout,
            is_organic=True,
            ttl=ttl,
        )
        signature = sign_blob(self.my_keypair, receipt_payload.blob_for_signing())
        return receipt_payload, signature

    def generate_job_accepted_receipt_message(
        self,
        accepted_timestamp: float,
        ttl: int,
    ) -> V0JobAcceptedReceiptRequest:
        time_accepted = datetime.datetime.fromtimestamp(accepted_timestamp, datetime.UTC)
        receipt_payload = JobAcceptedReceiptPayload(
            job_uuid=self.job_uuid,
            miner_hotkey=self.miner_hotkey,
            validator_hotkey=self.my_hotkey,
            timestamp=datetime.datetime.now(datetime.UTC),
            time_accepted=time_accepted,
            ttl=ttl,
        )
        return V0JobAcceptedReceiptRequest(
            payload=receipt_payload,
            signature=sign_blob(self.my_keypair, receipt_payload.blob_for_signing()),
        )

    async def send_job_accepted_receipt_message(
        self,
        accepted_timestamp: float,
        ttl: int,
    ) -> None:
        try:
            receipt_message = self.generate_job_accepted_receipt_message(
                accepted_timestamp,
                ttl,
            )
            await self.send_model(receipt_message)
            await JobAcceptedReceipt.from_payload(
                receipt_message.payload,
                validator_signature=receipt_message.signature,
            ).asave()
            logger.debug(f"Sent job accepted receipt for {self.job_uuid}")
        except Exception as e:
            comment = f"Failed to send job accepted receipt to miner {self.miner_name} for job {self.job_uuid}: {e}"
            logger.warning(comment)
            await self.notify_receipt_failure(comment)

    def generate_job_finished_receipt_message(
        self,
        started_timestamp: float,
        time_took_seconds: float,
        score: float,
    ) -> V0JobFinishedReceiptRequest:
        time_started = datetime.datetime.fromtimestamp(started_timestamp, datetime.UTC)
        receipt_payload = JobFinishedReceiptPayload(
            job_uuid=self.job_uuid,
            miner_hotkey=self.miner_hotkey,
            validator_hotkey=self.my_hotkey,
            timestamp=datetime.datetime.now(datetime.UTC),
            time_started=time_started,
            time_took_us=int(time_took_seconds * 1_000_000),
            score_str=f"{score:.6f}",
        )
        return V0JobFinishedReceiptRequest(
            payload=receipt_payload,
            signature=sign_blob(self.my_keypair, receipt_payload.blob_for_signing()),
        )

    async def send_job_finished_receipt_message(
        self,
        started_timestamp: float,
        time_took_seconds: float,
        score: float,
    ) -> None:
        try:
            receipt_message = self.generate_job_finished_receipt_message(
                started_timestamp, time_took_seconds, score
            )
            await self.send_model(receipt_message)
            await JobFinishedReceipt.from_payload(
                receipt_message.payload,
                validator_signature=receipt_message.signature,
            ).asave()
            logger.debug(f"Sent job finished receipt for {self.job_uuid}")
        except Exception as e:
            comment = f"Failed to send job finished receipt to miner {self.miner_name} for job {self.job_uuid}: {e}"
            logger.warning(comment)
            await self.notify_receipt_failure(comment)

    async def send_model(
        self, model: BaseRequest, error_event_callback: ErrorCallback | None = None
    ) -> None:
        if error_event_callback is None:
            error_event_callback = self.notify_send_failure

        await super().send_model(model, error_event_callback)

    async def connect(self) -> None:
        await super().connect()
        await self.transport.send(self.generate_authentication_message().model_dump_json())


class FailureReason(enum.Enum):
    MINER_CONNECTION_FAILED = enum.auto()
    INITIAL_RESPONSE_TIMED_OUT = enum.auto()
    EXECUTOR_READINESS_RESPONSE_TIMED_OUT = enum.auto()
    FINAL_RESPONSE_TIMED_OUT = enum.auto()
    JOB_DECLINED = enum.auto()
    EXECUTOR_FAILED = enum.auto()
    STREAMING_JOB_READY_TIMED_OUT = enum.auto()
    JOB_FAILED = enum.auto()


class OrganicJobError(Exception):
    def __init__(self, reason: FailureReason, received: BaseRequest | None = None):
        self.reason = reason
        self.received = received

    def __str__(self):
        s = f"Organic job failed, {self.reason=}"
        if self.received:
            s += f", received: {self.received_str()}"
        return s

    def __repr__(self):
        return f"{type(self).__name__}: {str(self)}"

    def received_str(self) -> str:
        if not self.received:
            return ""
        return self.received.model_dump_json()


@dataclass
class OrganicJobDetails:
    job_uuid: str
    executor_class: ExecutorClass = ExecutorClass.spin_up_4min__gpu_24gb
    docker_image: str | None = None
    raw_script: str | None = None
    docker_run_options_preset: DockerRunOptionsPreset = "nvidia_all"
    docker_run_cmd: list[str] = field(default_factory=list)
    total_job_timeout: int = 300
    volume: Volume | None = None
    output: OutputUpload | None = None
    artifacts_dir: str | None = None

    def __post_init__(self):
        if (self.docker_image, self.raw_script) == (None, None):
            raise ValueError("At least of of `docker_image` or `raw_script` must be not None")


async def run_organic_job(
    client: OrganicMinerClient,
    job_details: OrganicJobDetails,
    initial_response_timeout: int = 3,
    executor_ready_timeout: int = 300,
) -> tuple[str, str, dict[str, str]]:  # stdout, stderr, artifacts
    """
    Run an organic job. This is a simpler way to use OrganicMinerClient.

    :param client: the organic miner client
    :param job_details: details specific to the job that needs to be run
    :param initial_response_timeout: timeout for waiting for job acceptance/rejection
    :param executor_ready_timeout: timeout for waiting for executor readiness
    :return: standard out, standard error of the job container and artifacts
    """
    assert client.job_uuid == job_details.job_uuid

    async with contextlib.AsyncExitStack() as exit_stack:
        try:
            await exit_stack.enter_async_context(client)
        except TransportConnectionError as exc:
            raise OrganicJobError(FailureReason.MINER_CONNECTION_FAILED) from exc

        job_timer = Timer(timeout=job_details.total_job_timeout)

        receipt_payload, receipt_signature = client.generate_job_started_receipt_message(
            executor_class=job_details.executor_class,
            max_timeout=int(job_timer.time_left()),
            ttl=max(
                JOB_STARTED_RECEIPT_MIN_TTL,
                EXECUTOR_CLASS[job_details.executor_class].spin_up_time or 0,
            ),
        )
        await client.send_model(
            V0InitialJobRequest(
                job_uuid=job_details.job_uuid,
                executor_class=job_details.executor_class,
                base_docker_image_name=job_details.docker_image,
                timeout_seconds=job_details.total_job_timeout,
                volume_type=job_details.volume.volume_type if job_details.volume else None,
                job_started_receipt_payload=receipt_payload,
                job_started_receipt_signature=receipt_signature,
            ),
        )
        logger.debug(f"Sent initial job request for {job_details.job_uuid}")
        await JobStartedReceipt.from_payload(
            receipt_payload,
            validator_signature=receipt_signature,
        ).asave()

        try:
            try:
                initial_response = await asyncio.wait_for(
                    client.miner_accepting_or_declining_future,
                    timeout=min(job_timer.time_left(), initial_response_timeout),
                )
            except TimeoutError as exc:
                raise OrganicJobError(FailureReason.INITIAL_RESPONSE_TIMED_OUT) from exc
            if isinstance(initial_response, V0DeclineJobRequest):
                raise OrganicJobError(FailureReason.JOB_DECLINED, initial_response)

            await client.notify_job_accepted(initial_response)

            await client.send_job_accepted_receipt_message(
                accepted_timestamp=time.time(),
                ttl=int(job_timer.time_left()),
            )

            try:
                executor_readiness_response = await asyncio.wait_for(
                    client.executor_ready_or_failed_future,
                    timeout=min(job_timer.time_left(), executor_ready_timeout),
                )
            except TimeoutError as exc:
                raise OrganicJobError(FailureReason.EXECUTOR_READINESS_RESPONSE_TIMED_OUT) from exc
            if isinstance(executor_readiness_response, V0ExecutorFailedRequest):
                raise OrganicJobError(FailureReason.EXECUTOR_FAILED, executor_readiness_response)

            await client.notify_executor_ready(executor_readiness_response)

            await client.send_model(
                V0JobRequest(
                    job_uuid=job_details.job_uuid,
                    executor_class=job_details.executor_class,
                    docker_image_name=job_details.docker_image,
                    raw_script=job_details.raw_script,
                    docker_run_options_preset=job_details.docker_run_options_preset,
                    docker_run_cmd=job_details.docker_run_cmd,
                    volume=job_details.volume,
                    output_upload=job_details.output,
                    artifacts_dir=job_details.artifacts_dir,
                )
            )

            try:
                final_response = await asyncio.wait_for(
                    client.miner_finished_or_failed_future,
                    timeout=job_timer.time_left(),
                )
                if isinstance(final_response, V0JobFailedRequest):
                    raise OrganicJobError(FailureReason.JOB_FAILED, final_response)

                await client.send_job_finished_receipt_message(
                    started_timestamp=job_timer.start_time.timestamp(),
                    time_took_seconds=job_timer.passed_time(),
                    score=0,  # no score for organic jobs (at least right now)
                )

                return (
                    final_response.docker_process_stdout,
                    final_response.docker_process_stderr,
                    final_response.artifacts or {},
                )
            except TimeoutError as exc:
                raise OrganicJobError(FailureReason.FINAL_RESPONSE_TIMED_OUT) from exc

        except Exception:
            await client.send_job_finished_receipt_message(
                started_timestamp=job_timer.start_time.timestamp(),
                time_took_seconds=job_timer.passed_time(),
                score=0,
            )
            raise

    raise Exception("Organic job flow ended with no result")
