# Author: Takayuki Jimba (@yudetamago), Ryuya Nakamura (@nrryuya)
# Modified from Philip Daian's tests:
# https://github.com/vyperlang/vyper/blob/v0.1.0-beta.5/tests/examples/tokens/ERC20_solidity_compatible/test/erc20_tests_1.py
import pytest
from eth.codecs.abi.exceptions import EncodeError

from tests.utils import ZERO_ADDRESS

MAX_UINT256 = (2**256) - 1  # Max uint256 value
TOKEN_NAME = "Vypercoin"
TOKEN_SYMBOL = "FANG"
TOKEN_DECIMALS = 18
TOKEN_INITIAL_SUPPLY = 0


@pytest.fixture(scope="module")
def c(get_contract):
    with open("examples/tokens/ERC20.vy") as f:
        code = f.read()
    return get_contract(code, *[TOKEN_NAME, TOKEN_SYMBOL, TOKEN_DECIMALS, TOKEN_INITIAL_SUPPLY])


@pytest.fixture(scope="module")
def c_bad(get_contract):
    # Bad contract is used for overflow checks on totalSupply corrupted
    with open("examples/tokens/ERC20.vy") as f:
        code = f.read()
    bad_code = code.replace("self.totalSupply += _value", "").replace(
        "self.totalSupply -= _value", ""
    )
    return get_contract(bad_code, *[TOKEN_NAME, TOKEN_SYMBOL, TOKEN_DECIMALS, TOKEN_INITIAL_SUPPLY])


def test_initial_state(c, env):
    a1, a2, a3 = env.accounts[1:4]
    # Check total supply, name, symbol and decimals are correctly set
    assert c.totalSupply() == TOKEN_INITIAL_SUPPLY
    assert c.name() == TOKEN_NAME
    assert c.symbol() == TOKEN_SYMBOL
    assert c.decimals() == TOKEN_DECIMALS
    # Check several account balances as 0
    assert c.balanceOf(a1) == 0
    assert c.balanceOf(a2) == 0
    assert c.balanceOf(a3) == 0
    # Check several allowances as 0
    assert c.allowance(a1, a1) == 0
    assert c.allowance(a1, a2) == 0
    assert c.allowance(a1, a3) == 0
    assert c.allowance(a2, a3) == 0


def test_mint_and_burn(c, env, tx_failed):
    minter, a1, a2 = env.accounts[0:3]

    # Test scenario were mints 2 to a1, burns twice (check balance consistency)
    assert c.balanceOf(a1) == 0
    c.mint(a1, 2, sender=minter)
    assert c.balanceOf(a1) == 2
    c.burn(2, sender=a1)
    assert c.balanceOf(a1) == 0
    with tx_failed():
        c.burn(2, sender=a1)
    assert c.balanceOf(a1) == 0
    # Test scenario were mintes 0 to a2, burns (check balance consistency, false burn)
    c.mint(a2, 0, sender=minter)
    assert c.balanceOf(a2) == 0
    with tx_failed():
        c.burn(2, sender=a2)
    # Check that a1 cannot burn after depleting their balance
    with tx_failed():
        c.burn(1, sender=a1)
    # Check that a1, a2 cannot mint
    with tx_failed():
        c.mint(a1, 1, sender=a1)
    with tx_failed():
        c.mint(a2, 1, sender=a2)
    # Check that mint to ZERO_ADDRESS failed
    with tx_failed():
        c.mint(ZERO_ADDRESS, 1, sender=a1)
    with tx_failed():
        c.mint(ZERO_ADDRESS, 1, sender=minter)


def test_totalSupply(c, env, tx_failed):
    # Test total supply initially, after mint, between two burns, and after failed burn
    minter, a1 = env.accounts[0:2]
    assert c.totalSupply() == 0
    c.mint(a1, 2, sender=minter)
    assert c.totalSupply() == 2
    c.burn(1, sender=a1)
    assert c.totalSupply() == 1
    c.burn(1, sender=a1)
    assert c.totalSupply() == 0
    with tx_failed():
        c.burn(1, sender=a1)
    assert c.totalSupply() == 0
    # Test that 0-valued mint can't affect supply
    c.mint(a1, 0, sender=minter)
    assert c.totalSupply() == 0


def test_transfer(c, env, tx_failed):
    minter, a1, a2 = env.accounts[0:3]
    with tx_failed():
        c.burn(1, sender=a2)
    c.mint(a1, 2, sender=minter)
    c.burn(1, sender=a1)
    c.transfer(a2, 1, sender=a1)
    with tx_failed():
        c.burn(1, sender=a1)
    c.burn(1, sender=a2)
    with tx_failed():
        c.burn(1, sender=a2)
    # Ensure transfer fails with insufficient balance
    with tx_failed():
        c.transfer(a1, 1, sender=a2)
    # Ensure 0-transfer always succeeds
    c.transfer(a1, 0, sender=a2)


def test_maxInts(c, env, tx_failed):
    minter, a1, a2 = env.accounts[0:3]
    c.mint(a1, MAX_UINT256, sender=minter)
    assert c.balanceOf(a1) == MAX_UINT256
    with tx_failed():
        c.mint(a1, 1, sender=a1)
    with tx_failed():
        c.mint(a1, MAX_UINT256, sender=a1)
    # Check that totalSupply cannot overflow, even when mint to other account
    with tx_failed():
        c.mint(a2, 1, sender=minter)
    # Check that corresponding mint is allowed after burn
    c.burn(1, sender=a1)
    c.mint(a2, 1, sender=minter)
    with tx_failed():
        c.mint(a2, 1, sender=minter)
    c.transfer(a1, 1, sender=a2)
    # Assert that after obtaining max number of tokens, a1 can transfer those but no more
    assert c.balanceOf(a1) == MAX_UINT256
    c.transfer(a2, MAX_UINT256, sender=a1)
    assert c.balanceOf(a2) == MAX_UINT256
    assert c.balanceOf(a1) == 0
    # [ next line should never work in EVM ]
    with pytest.raises(EncodeError):
        c.transfer(a1, MAX_UINT256 + 1, sender=a2)
    # Check approve/allowance w max possible token values
    assert c.balanceOf(a2) == MAX_UINT256
    c.approve(a1, MAX_UINT256, sender=a2)
    c.transferFrom(a2, a1, MAX_UINT256, sender=a1)
    assert c.balanceOf(a1) == MAX_UINT256
    assert c.balanceOf(a2) == 0
    # Check that max amount can be burned
    c.burn(MAX_UINT256, sender=a1)
    assert c.balanceOf(a1) == 0


def test_transferFrom_and_Allowance(c, env, tx_failed):
    minter, a1, a2, a3 = env.accounts[0:4]
    with tx_failed():
        c.burn(1, sender=a2)
    c.mint(a1, 1, sender=minter)
    c.mint(a2, 1, sender=minter)
    c.burn(1, sender=a1)
    # This should fail; no allowance or balance (0 always succeeds)
    with tx_failed():
        c.transferFrom(a1, a3, 1, sender=a2)
    c.transferFrom(a1, a3, 0, sender=a2)
    # Correct call to approval should update allowance (but not for reverse pair)
    c.approve(a2, 1, sender=a1)
    assert c.allowance(a1, a2) == 1
    assert c.allowance(a2, a1) == 0
    # transferFrom should succeed when allowed, fail with wrong sender
    with tx_failed():
        c.transferFrom(a1, a3, 1, sender=a3)
    assert c.balanceOf(a2) == 1
    c.approve(a1, 1, sender=a2)
    c.transferFrom(a2, a3, 1, sender=a1)
    # Allowance should be correctly updated after transferFrom
    assert c.allowance(a2, a1) == 0
    # transferFrom with no funds should fail despite approval
    c.approve(a1, 1, sender=a2)
    assert c.allowance(a2, a1) == 1
    with tx_failed():
        c.transferFrom(a2, a3, 1, sender=a1)
    # 0-approve should not change balance or allow transferFrom to change balance
    c.mint(a2, 1, sender=minter)
    assert c.allowance(a2, a1) == 1
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    with tx_failed():
        c.transferFrom(a2, a3, 1, sender=a1)
    # Test that if non-zero approval exists, 0-approval is NOT required to proceed
    # a non-conformant implementation is described in countermeasures at
    # https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit#heading=h.m9fhqynw2xvt
    # the final spec insists on NOT using this behavior
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 1, sender=a2)
    assert c.allowance(a2, a1) == 1
    c.approve(a1, 2, sender=a2)
    assert c.allowance(a2, a1) == 2
    # Check that approving 0 then amount also works
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 5, sender=a2)
    assert c.allowance(a2, a1) == 5


def test_burnFrom_and_Allowance(c, env, tx_failed):
    minter, a1, a2, a3 = env.accounts[0:4]
    with tx_failed():
        c.burn(1, sender=a2)
    c.mint(a1, 1, sender=minter)
    c.mint(a2, 1, sender=minter)
    c.burn(1, sender=a1)
    # This should fail; no allowance or balance (0 always succeeds)
    with tx_failed():
        c.burnFrom(a1, 1, sender=a2)
    c.burnFrom(a1, 0, sender=a2)
    # Correct call to approval should update allowance (but not for reverse pair)
    c.approve(a2, 1, sender=a1)
    assert c.allowance(a1, a2) == 1
    assert c.allowance(a2, a1) == 0
    # transferFrom should succeed when allowed, fail with wrong sender
    with tx_failed():
        c.burnFrom(a2, 1, sender=a3)
    assert c.balanceOf(a2) == 1
    c.approve(a1, 1, sender=a2)
    c.burnFrom(a2, 1, sender=a1)
    # Allowance should be correctly updated after transferFrom
    assert c.allowance(a2, a1) == 0
    # transferFrom with no funds should fail despite approval
    c.approve(a1, 1, sender=a2)
    assert c.allowance(a2, a1) == 1
    with tx_failed():
        c.burnFrom(a2, 1, sender=a1)
    # 0-approve should not change balance or allow transferFrom to change balance
    c.mint(a2, 1, sender=minter)
    assert c.allowance(a2, a1) == 1
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    with tx_failed():
        c.burnFrom(a2, 1, sender=a1)
    # Test that if non-zero approval exists, 0-approval is NOT required to proceed
    # a non-conformant implementation is described in countermeasures at
    # https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/edit#heading=h.m9fhqynw2xvt
    # the final spec insists on NOT using this behavior
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 1, sender=a2)
    assert c.allowance(a2, a1) == 1
    c.approve(a1, 2, sender=a2)
    assert c.allowance(a2, a1) == 2
    # Check that approving 0 then amount also works
    c.approve(a1, 0, sender=a2)
    assert c.allowance(a2, a1) == 0
    c.approve(a1, 5, sender=a2)
    assert c.allowance(a2, a1) == 5
    # Check that burnFrom to ZERO_ADDRESS failed
    with tx_failed():
        c.burnFrom(ZERO_ADDRESS, 0, sender=a1)


def test_raw_logs(c, env, get_logs):
    minter, a1, a2, a3 = env.accounts[0:4]

    def get_log_args(_, c, event_name):
        return get_logs(c, event_name)[0].args

    # Check that mint appropriately emits Transfer event
    args = get_log_args(c.mint(a1, 2, sender=minter), c, "Transfer")
    assert args.sender == ZERO_ADDRESS
    assert args.receiver == a1
    assert args.value == 2

    args = get_log_args(c.mint(a1, 0, sender=minter), c, "Transfer")
    assert args.sender == ZERO_ADDRESS
    assert args.receiver == a1
    assert args.value == 0

    # Check that burn appropriately emits Transfer event
    args = get_log_args(c.burn(1, sender=a1), c, "Transfer")
    assert args.sender == a1
    assert args.receiver == ZERO_ADDRESS
    assert args.value == 1

    args = get_log_args(c.burn(0, sender=a1), c, "Transfer")
    assert args.sender == a1
    assert args.receiver == ZERO_ADDRESS
    assert args.value == 0

    # Check that transfer appropriately emits Transfer event
    args = get_log_args(c.transfer(a2, 1, sender=a1), c, "Transfer")
    assert args.sender == a1
    assert args.receiver == a2
    assert args.value == 1

    args = get_log_args(c.transfer(a2, 0, sender=a1), c, "Transfer")
    assert args.sender == a1
    assert args.receiver == a2
    assert args.value == 0

    # Check that approving amount emits events
    args = get_log_args(c.approve(a1, 1, sender=a2), c, "Approval")
    assert args.owner == a2
    assert args.spender == a1
    assert args.value == 1

    args = get_log_args(c.approve(a2, 0, sender=a3), c, "Approval")
    assert args.owner == a3
    assert args.spender == a2
    assert args.value == 0

    # Check that transferFrom appropriately emits Transfer event
    args = get_log_args(c.transferFrom(a2, a3, 1, sender=a1), c, "Transfer")
    assert args.sender == a2
    assert args.receiver == a3
    assert args.value == 1

    args = get_log_args(c.transferFrom(a2, a3, 0, sender=a1), c, "Transfer")
    assert args.sender == a2
    assert args.receiver == a3
    assert args.value == 0


def test_bad_transfer(c_bad, env, tx_failed):
    # Ensure transfer fails if it would otherwise overflow balance when totalSupply is corrupted
    minter, a1, a2 = env.accounts[0:3]
    c_bad.mint(a1, MAX_UINT256, sender=minter)
    c_bad.mint(a2, 1, sender=minter)
    with tx_failed():
        c_bad.transfer(a1, 1, sender=a2)
    c_bad.transfer(a2, MAX_UINT256 - 1, sender=a1)
    assert c_bad.balanceOf(a1) == 1
    assert c_bad.balanceOf(a2) == MAX_UINT256


def test_bad_burn(c_bad, env, tx_failed):
    # Ensure burn fails if it would otherwise underflow balance when totalSupply is corrupted
    minter, a1 = env.accounts[0:2]
    assert c_bad.balanceOf(a1) == 0
    c_bad.mint(a1, 2, sender=minter)
    assert c_bad.balanceOf(a1) == 2
    with tx_failed():
        c_bad.burn(3, sender=a1)


def test_bad_transferFrom(c_bad, env, tx_failed):
    # Ensure transferFrom fails if it would otherwise overflow balance when totalSupply is corrupted
    minter, a1, a2 = env.accounts[0:3]
    c_bad.mint(a1, MAX_UINT256, sender=minter)
    c_bad.mint(a2, 1, sender=minter)
    c_bad.approve(a1, 1, sender=a2)
    with tx_failed():
        c_bad.transferFrom(a2, a1, 1, sender=a1)
    c_bad.approve(a2, MAX_UINT256 - 1, sender=a1)
    assert c_bad.allowance(a1, a2) == MAX_UINT256 - 1
    c_bad.transferFrom(a1, a2, MAX_UINT256 - 1, sender=a2)
    assert c_bad.balanceOf(a2) == MAX_UINT256
