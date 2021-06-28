import brownie
from brownie import *
from helpers.constants import MaxUint256
from helpers.SnapshotManager import SnapshotManager
from config import DEFAULT_WITHDRAWAL_FEE

MAX_BASIS = 10000

def test_is_profitable(user, strategy, token, vault):
  randomUser = accounts[6]

  initial_balance = token.balanceOf(user)
  
  settKeeper = accounts.at(vault.keeper(), force=True)

  snap = SnapshotManager(vault, strategy, "StrategySnapshot")

  # Deposit
  assert token.balanceOf(user) > 0

  depositAmount = int(token.balanceOf(user) * 0.8)
  assert depositAmount > 0

  token.approve(vault.address, MaxUint256, {"from": user})
  snap.settDeposit(depositAmount, {"from": user})
  

  # Earn
  with brownie.reverts("onlyAuthorizedActors"):
      vault.earn({"from": randomUser})

  min = vault.min()
  max = vault.max()
  remain = max - min

  snap.settHarvest({"from": settKeeper})

  chain.sleep(15)
  chain.mine(1)

  snap.settWithdrawAll({"from": user})

  ending_balance = token.balanceOf(user)

  initial_balance_with_fees = initial_balance * (1 - (DEFAULT_WITHDRAWAL_FEE / MAX_BASIS))

  print("Initial Balance")
  print(initial_balance)
  print("initial_balance_with_fees")
  print(initial_balance_with_fees)
  print("Ending Balance")
  print(ending_balance)

  assert ending_balance > initial_balance_with_fees