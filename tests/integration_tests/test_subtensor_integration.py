import json
import os
from collections import deque
import random
from unittest.mock import patch
import websocket

import pytest
from bittensor.core import settings
from bittensor.core.subtensor import Subtensor
from tests.helpers.refined_output import WEBSOCKET_RESPONSES


# TODO new dict design:
# {
#     method: {
#         params_list: result,
#         params_list: result,
#         ...
#     },
#     method: {
#         params_list: result,
#         ...
#     },
#     ...
# }


class FakeWebsocket(websocket.WebSocket):
    def __init__(self, *args, seed, **kwargs):
        super().__init__(**kwargs)
        self.seed = seed
        self.received = deque()

    def send(self, payload: str, *args, **kwargs):
        received = json.loads(payload)
        id_ = received.pop("id")
        self.received.append((received, id_))

    def recv(self):
        item, _id = self.received.pop()
        try:
            response = WEBSOCKET_RESPONSES[self.seed][item["method"]][
                json.dumps(item["params"])
            ]
            response["id"] = _id
            return json.dumps(response)
        except KeyError:
            print("ERROR", self.seed, item["method"], item["params"])
            raise
        except TypeError:
            print("TypeError", response)
            raise

    def close(self, *args, **kwargs):
        pass


# @pytest.fixture
# def subtensor():
#     subtensor_ = Subtensor(websocket=FakeWebsocket())
#     yield subtensor_
#     print("Subtensor closed")


# @pytest.mark.parametrize(
#     "input_, runtime_api, method, output",
#     [
#         (
#             [1],
#             "NeuronInfoRuntimeApi",
#             "get_neurons_lite",
#             "0x0100"
#         ),
#         (
#             [],
#             "SubnetRegistrationRuntimeApi",
#             "get_network_registration_cost",
#             "0x"
#         )
#     ]
# )
# def test_encode_params(subtensor, input_, runtime_api, method, output):
#     call_definition = settings.TYPE_REGISTRY["runtime_api"][runtime_api]["methods"][
#         method
#     ]
#     result = subtensor._encode_params(call_definition=call_definition, params=input_)
#     assert result == output


# def test_blocks_since_last_update():
#     subtensor = Subtensor(websocket=FakeWebsocket(seed="blocks_since_last_update"))
#     netuid = 1
#     query = subtensor.blocks_since_last_update(netuid=netuid, uid=5)
#     assert isinstance(query, int)


def test_get_all_subnets_info():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="get_all_subnets_info"))
    result = subtensor.get_all_subnets_info()
    assert isinstance(result, list)
    assert result[0].owner_ss58 == "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"
    assert result[1].kappa == 32767
    assert result[1].max_weight_limit == 65535
    assert result[1].blocks_since_epoch == 1


def test_metagraph():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="metagraph"))
    result = subtensor.metagraph(23)
    assert result.n == 19
    assert result.netuid == 23
    assert result.block == 3264143


def test_get_netuids_for_hotkey():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="get_netuids_for_hotkey"))
    result = subtensor.get_netuids_for_hotkey(
        "5DkzsviNQr4ZePXMmEfNPDcE7cQ9cVyepmQbgUw6YT3odcwh"
    )
    assert result == [23]


def test_get_current_block():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="get_current_block"))
    result = subtensor.get_current_block()
    assert result == 3264143


def test_is_hotkey_registered_any():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="is_hotkey_registered_any"))
    result = subtensor.is_hotkey_registered_any(
        "5DkzsviNQr4ZePXMmEfNPDcE7cQ9cVyepmQbgUw6YT3odcwh"
    )
    assert result is True


def test_is_hotkey_registered_on_subnet():
    subtensor = Subtensor(
        websocket=FakeWebsocket(seed="is_hotkey_registered_on_subnet")
    )
    result = subtensor.is_hotkey_registered_on_subnet(
        "5DkzsviNQr4ZePXMmEfNPDcE7cQ9cVyepmQbgUw6YT3odcwh", 23
    )
    assert result is True


def test_is_hotkey_registered():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="is_hotkey_registered"))
    result = subtensor.is_hotkey_registered(
        "5DkzsviNQr4ZePXMmEfNPDcE7cQ9cVyepmQbgUw6YT3odcwh"
    )
    assert result is True


def test_blocks_since_last_update():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="blocks_since_last_update"))
    result = subtensor.blocks_since_last_update(23, 5)
    assert result == 1293687


def test_get_block_hash():
    subtensor = Subtensor(websocket=FakeWebsocket(seed="get_block_hash"))
    result = subtensor.get_block_hash(3234677)
    assert (
        result == "0xe89482ae7892ab5633f294179245f4058a99781e15f21da31eb625169da5d409"
    )
