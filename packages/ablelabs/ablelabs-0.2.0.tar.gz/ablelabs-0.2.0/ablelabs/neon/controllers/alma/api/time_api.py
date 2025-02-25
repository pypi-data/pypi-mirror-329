import sys, os

sys.path.append(os.path.abspath(os.curdir))
from ablelabs.neon.utils.network.messenger import MessengerClient, run_server_func
from ablelabs.neon.utils.network.tcp_client import TcpClient
from ablelabs.neon.controllers.alma.api.robot_router import RobotRouter
from ablelabs.neon.common.alma.structs import Location, Speed, FlowRate


class TimeAPI(MessengerClient):
    def __init__(self, tcp_client: TcpClient) -> None:
        super().__init__(tcp_client)

    @run_server_func(RobotRouter.time_initialize)
    async def initialize(self) -> float:
        pass
