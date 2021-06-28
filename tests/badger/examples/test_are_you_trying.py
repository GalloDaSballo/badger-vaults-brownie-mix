from brownie import *
from helpers.constants import MaxUint256


def test_are_you_trying(user, vault, strategy, want):
  """
    Verifies that you set up the Strategy properly
  """
  # Setup
  startingBalance = want.balanceOf(user)
  
  depositAmount = startingBalance // 2
  assert startingBalance >= depositAmount
  assert startingBalance >= 0
  # End Setup

  # Deposit
  assert want.balanceOf(vault) == 0

  want.approve(vault, MaxUint256, {"from": user})
  vault.deposit(depositAmount, {"from": user})

  assert want.balanceOf(vault) == depositAmount

  ## Load funds in strat
  strategy.harvest({"from": user})

  chain.mine(100) # Mine so we get some interest

  ## TEST 1: Does the want get used in any way?
  # Did the strategy do something with the asset?
  assert want.balanceOf(strategy) == depositAmount

  # Use this if it should invest all
  # assert want.balanceOf(strategy) == 0

  # Change to this if the strat is supposed to hodl and do nothing
  #assert strategy.balanceOf(want) = depositAmount

  ## TODO: Update with new architecture
  ## TEST 2: Is the Harvest profitable?
  harvest = strategy.harvest({"from": user})
  event = harvest.events["Harvest"]
  # If it doesn't print, we don't want it
  assert event["harvested"] > 0


  