import os
from typing import Any
from evalsync.proto.sync_pb2 import (
    StateSync,
    ServiceState,
    ManagerMessage,
    ExperimentCommand,
)
import zmq


class ExperimentWorker:
    def __init__(self, experiment_id: str | None, client_id: str | None):
        self.context = zmq.Context()
        self.experiment_id = (
            experiment_id if experiment_id else os.environ["EVALSYNC_EXPERIMENT_ID"]
        )
        self.client_id = client_id if client_id else os.environ["EVALSYNC_CLIENT_ID"]
        self.state = ServiceState.INIT

        self.state_socket = self.context.socket(zmq.DEALER)
        self.state_socket.setsockopt(zmq.LINGER, 1000)
        self.state_socket.setsockopt(zmq.IDENTITY, f"{client_id}".encode())
        self.state_socket.connect(f"ipc:///tmp/{experiment_id}-STATE")

        self.command_socket = self.context.socket(zmq.DEALER)
        self.command_socket.setsockopt(zmq.LINGER, 1000)
        self.command_socket.setsockopt(zmq.IDENTITY, f"{client_id}".encode())
        self.command_socket.connect(f"ipc:///tmp/{experiment_id}-COMMAND")

        self.metadata: dict[str, Any] = {}

    def cleanup(self):
        self.state_socket.close()
        self.command_socket.close()
        self.context.term()

    def notify_manager(self, msg: str) -> bool:
        message = StateSync(
            state=self.state, error_message=msg, metadata=self.metadata
        ).SerializeToString()
        self.state_socket.send_multipart([b"", message])
        return True

    def ready(self) -> bool:
        if self.state == ServiceState.INIT:
            self.state = ServiceState.READY
            self.notify_manager("ready")
            return True
        else:
            return False

    def wait_for_start(self) -> bool:
        if self.state == ServiceState.READY:
            while self.state != ServiceState.RUNNING:
                _, raw_message = self.command_socket.recv_multipart()
                message = ManagerMessage()

                ManagerMessage.ParseFromString(message, raw_message)
                match message.command:
                    case ExperimentCommand.BEGIN:
                        self.state = ServiceState.RUNNING
                        self.notify_manager("running")
                        return True
                    case ExperimentCommand.END | ExperimentCommand.ABORT:
                        self.state = ServiceState.ERROR
                        self.notify_manager("error")
                        return False

        return False

    def end(self):
        if self.state == ServiceState.RUNNING:
            self.state = ServiceState.DONE
            self.notify_manager("done")
            return True
        else:
            return False

    def wait_for_stop(self):
        if self.state == ServiceState.RUNNING:
            while self.state != ServiceState.DONE:
                _, raw_message = self.command_socket.recv_multipart()
                message = ManagerMessage()
                ManagerMessage.ParseFromString(message, raw_message)
                match message.command:
                    case ExperimentCommand.END:
                        self.state = ServiceState.DONE
                        self.notify_manager("done")
                        return True
                    case ExperimentCommand.BEGIN | ExperimentCommand.ABORT:
                        self.state = ServiceState.ERROR
                        self.notify_manager("error")
                        return True
        return False
