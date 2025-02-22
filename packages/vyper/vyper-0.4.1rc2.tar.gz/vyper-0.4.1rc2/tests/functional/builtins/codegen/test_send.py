from tests.utils import ZERO_ADDRESS


def test_send(tx_failed, get_contract, env):
    send_test = """
@external
def foo():
    send(msg.sender, self.balance + 1)

@external
def fop():
    send(msg.sender, 10)
    """
    env.set_balance(env.deployer, 1000)
    c = get_contract(send_test, value=10)
    with tx_failed():
        c.foo()
    assert env.get_balance(c.address) == 10
    c.fop()
    assert env.get_balance(c.address) == 0
    with tx_failed():
        c.fop()


def test_default_gas(get_contract, env, tx_failed):
    """
    Tests to verify that send to default function will send limited gas (2300),
    but raw_call can send more.
    """

    sender_code = """
@external
def test_send(receiver: address):
    send(receiver, 1)

@external
def test_call(receiver: address):
    raw_call(receiver, b"", gas=50000, max_outsize=0, value=1)
    """

    # default function writes variable, this requires more gas than send can pass
    receiver_code = """
last_sender: public(address)

@external
@payable
def __default__():
    self.last_sender = msg.sender
    """

    env.set_balance(env.deployer, 300000)
    sender = get_contract(sender_code, value=1)
    receiver = get_contract(receiver_code)

    with tx_failed():
        sender.test_send(receiver.address, gas=100000)

    # no value transfer happened, variable was not changed
    assert receiver.last_sender() == ZERO_ADDRESS
    assert env.get_balance(sender.address) == 1
    assert env.get_balance(receiver.address) == 0

    sender.test_call(receiver.address, gas=100000)

    # value transfer happened, variable was changed
    assert receiver.last_sender() == sender.address
    assert env.get_balance(sender.address) == 0
    assert env.get_balance(receiver.address) == 1


def test_send_gas_stipend(get_contract, env):
    """
    Tests to verify that adding gas stipend to send() will send sufficient gas
    """

    sender_code = """

@external
def test_send_stipend(receiver: address):
    send(receiver, 1, gas=50000)
    """

    # default function writes variable, this requires more gas than
    # send would pass without gas stipend
    receiver_code = """
last_sender: public(address)

@external
@payable
def __default__():
    self.last_sender = msg.sender
    """

    env.set_balance(env.deployer, 300000)
    sender = get_contract(sender_code, value=1)
    receiver = get_contract(receiver_code)

    sender.test_send_stipend(receiver.address, gas=100000)

    # value transfer happened, variable was changed
    assert receiver.last_sender() == sender.address
    assert env.get_balance(sender.address) == 0
    assert env.get_balance(receiver.address) == 1
