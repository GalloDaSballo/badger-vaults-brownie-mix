"""
Deploy a fresh vault with your Strategy
"""
from brownie import Strategy
from scripts.vaults.deploy_badger_strategy import deploy_strategy_logic

def main():
  ## Deploy Vault and Add Strat
  strat_address = deploy_strategy_logic(Strategy)

  ## Return Strat Address
  return strat_address