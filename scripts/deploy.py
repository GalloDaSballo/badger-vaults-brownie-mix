"""
Deploy a fresh vault with your Strategy
"""
from pathlib import Path
from brownie import Strategy, accounts, config, network, project, web3

def main():
  project.load(
      Path.home() / ".brownie" / "packages" / config["dependencies"][0]
  )

  return deploy_script