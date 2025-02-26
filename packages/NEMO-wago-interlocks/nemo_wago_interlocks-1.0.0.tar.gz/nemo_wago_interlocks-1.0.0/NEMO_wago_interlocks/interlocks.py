from logging import getLogger
from time import sleep

from NEMO.interlocks import ModbusTcpInterlock, interlocks
from NEMO.models import Interlock as Interlock_model
from pymodbus.client import ModbusTcpClient

wago_logger = getLogger(__name__)


class WagoModbusTcpInterlocks(ModbusTcpInterlock):
    """
    Support for WAGO interlocks.
    WAGO interlocks implement Modbus but differ in the fact that they use an offset for reading back coil value
    """

    WAGO_READ_OFFSET = 512

    @classmethod
    def set_relay_state(cls, interlock: Interlock_model, state: {0, 1}) -> Interlock_model.State:
        coil = interlock.channel
        client = ModbusTcpClient(interlock.card.server, port=interlock.card.port)
        try:
            valid_connection = client.connect()
            if not valid_connection:
                raise Exception(
                    f"Connection to server {interlock.card.server}:{interlock.card.port} could not be established"
                )
            kwargs = {"slave": interlock.unit_id} if interlock.unit_id is not None else {}
            write_reply = client.write_coil(coil, state, **kwargs)
            if write_reply.isError():
                raise Exception(str(write_reply))
            sleep(0.3)
            read_reply = client.read_coils(cls.WAGO_READ_OFFSET + coil, 1, **kwargs)
            if read_reply.isError():
                raise Exception(str(read_reply))
            state = read_reply.bits[0]
            if state == cls.MODBUS_OFF:
                return Interlock_model.State.LOCKED
            elif state == cls.MODBUS_ON:
                return Interlock_model.State.UNLOCKED
        finally:
            client.close()


interlocks["wago_modbus_tcp"] = WagoModbusTcpInterlocks()
