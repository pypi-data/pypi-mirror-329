import pytest
from eth_utils import to_wei

from tests.utils import decimal_to_int
from vyper.semantics.types import DecimalT
from vyper.utils import quantize, round_towards_zero

wei_denoms = {
    "femtoether": 3,
    "kwei": 3,
    "babbage": 3,
    "picoether": 6,
    "mwei": 6,
    "lovelace": 6,
    "nanoether": 9,
    "gwei": 9,
    "shannon": 9,
    "microether": 12,
    "szabo": 12,
    "milliether": 15,
    "finney": 15,
    "ether": 18,
    "kether": 21,
    "grand": 21,
}


@pytest.mark.parametrize("denom,multiplier", wei_denoms.items())
def test_wei_uint256(get_contract, tx_failed, denom, multiplier):
    code = f"""
@external
def foo(a: uint256) -> uint256:
    return as_wei_value(a, "{denom}")
    """

    c = get_contract(code)

    value = (2**256 - 1) // (10**multiplier)
    assert c.foo(value) == value * (10**multiplier)

    value = (2**256 - 1) // (10 ** (multiplier - 1))
    with tx_failed():
        c.foo(value)


@pytest.mark.parametrize("denom,multiplier", wei_denoms.items())
def test_wei_int128(get_contract, tx_failed, denom, multiplier):
    code = f"""
@external
def foo(a: int128) -> uint256:
    return as_wei_value(a, "{denom}")
    """

    c = get_contract(code)
    value = (2**127 - 1) // (10**multiplier)

    assert c.foo(value) == value * (10**multiplier)


@pytest.mark.parametrize("denom,multiplier", wei_denoms.items())
def test_wei_decimal(get_contract, tx_failed, denom, multiplier):
    code = f"""
@external
def foo(a: decimal) -> uint256:
    return as_wei_value(a, "{denom}")
    """
    c = get_contract(code)

    denom_int = 10**multiplier
    # TODO: test with more values
    _, hi = DecimalT().ast_bounds
    value = quantize(hi / denom_int)

    assert c.foo(decimal_to_int(value)) == round_towards_zero(value * denom_int)


@pytest.mark.parametrize("value", (-1, -(2**127)))
@pytest.mark.parametrize("data_type", ["decimal", "int128"])
def test_negative_value_reverts(get_contract, tx_failed, value, data_type):
    code = f"""
@external
def foo(a: {data_type}) -> uint256:
    return as_wei_value(a, "ether")
    """

    c = get_contract(code)
    with tx_failed():
        c.foo(value)


@pytest.mark.parametrize("denom,multiplier", wei_denoms.items())
@pytest.mark.parametrize("data_type", ["decimal", "int128", "uint256"])
def test_zero_value(get_contract, tx_failed, denom, multiplier, data_type):
    code = f"""
@external
def foo(a: {data_type}) -> uint256:
    return as_wei_value(a, "{denom}")
    """

    c = get_contract(code)
    assert c.foo(0) == 0


def test_ext_call(side_effects_contract, assert_side_effects_invoked, get_contract):
    code = """
interface Foo:
    def foo(x: uint8) -> uint8: nonpayable

@external
def foo(a: Foo) -> uint256:
    return as_wei_value(extcall a.foo(7), "ether")
    """

    c1 = side_effects_contract("uint8")
    c2 = get_contract(code)

    assert c2.foo(c1.address) == to_wei(7, "ether")
    assert_side_effects_invoked(c1, lambda: c2.foo(c1.address))


def test_internal_call(get_contract):
    code = """
@external
def foo() -> uint256:
    return as_wei_value(self.bar(), "ether")

@internal
def bar() -> uint8:
    return 7
    """
    c = get_contract(code)
    assert c.foo() == to_wei(7, "ether")
