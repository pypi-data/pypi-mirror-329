# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Agent Quickstart script."""

import json
import os
import textwrap
import time
import typing as t
import warnings
from dataclasses import dataclass
from pathlib import Path

import requests
from aea.crypto.registries import make_ledger_api
from aea_ledger_ethereum import LedgerApi
from halo import Halo  # type: ignore[import]
from web3.exceptions import Web3Exception

from operate.account.user import UserAccount
from operate.constants import IPFS_ADDRESS, OPERATE_HOME, ZERO_ADDRESS
from operate.data import DATA_DIR
from operate.data.contracts.staking_token.contract import StakingTokenContract
from operate.ledger.profiles import STAKING
from operate.operate_types import (
    Chain,
    LedgerType,
    OnChainState,
    ServiceEnvProvisionType,
    ServiceTemplate,
)
from operate.quickstart.utils import (
    CHAIN_TO_METADATA,
    ask_or_get_from_env,
    check_rpc,
    print_box,
    print_section,
    print_title,
    wei_to_token,
)
from operate.resource import LocalResource, deserialize
from operate.services.manage import ServiceManager
from operate.services.service import NON_EXISTENT_MULTISIG, Service
from operate.utils.gnosis import get_asset_balance


warnings.filterwarnings("ignore", category=UserWarning)


if t.TYPE_CHECKING:
    from operate.cli import OperateApp

NO_STAKING_PROGRAM_ID = "no_staking"
NO_STAKING_PROGRAM_METADATA = {
    "name": "No staking",
    "description": "Your Olas Predict agent will still actively participate in prediction\
        markets, but it will not be staked within any staking program.",
    "available_staking_slots": "∞",
}
QS_STAKING_PROGRAMS: t.Dict[Chain, t.Dict[str, int]] = {
    Chain.GNOSIS: {
        "quickstart_beta_hobbyist": 25,
        "quickstart_beta_hobbyist_2": 25,
        "quickstart_beta_expert": 25,
        "quickstart_beta_expert_2": 25,
        "quickstart_beta_expert_3": 25,
        "quickstart_beta_expert_4": 25,
        "quickstart_beta_expert_5": 25,
        "quickstart_beta_expert_6": 25,
        "quickstart_beta_expert_7": 25,
        "quickstart_beta_expert_8": 25,
        "quickstart_beta_expert_9": 25,
        "quickstart_beta_expert_10": 25,
        "quickstart_beta_expert_11": 25,
        "quickstart_beta_expert_12": 25,
        "quickstart_beta_expert_15_mech_marketplace": 25,
        "quickstart_beta_expert_16_mech_marketplace": 25,
        "mech_marketplace": 37,
    },
    Chain.OPTIMISTIC: {
        "optimus_alpha": 40,
    },
    Chain.ETHEREUM: {},
    Chain.BASE: {
        "meme_base_alpha_2": 43,
    },
    Chain.CELO: {},
    Chain.MODE: {
        "optimus_alpha": 40,
    },
}


@dataclass
class QuickstartConfig(LocalResource):
    """Local configuration."""

    path: Path
    rpc: t.Optional[t.Dict[str, str]] = None
    password_migrated: t.Optional[bool] = None
    staking_program_id: t.Optional[str] = None
    principal_chain: t.Optional[str] = None
    user_provided_args: t.Optional[t.Dict[str, str]] = None

    @classmethod
    def from_json(cls, obj: t.Dict) -> "LocalResource":
        """Load LocalResource from json."""
        kwargs = {}
        for pname, ptype in cls.__annotations__.items():
            if pname.startswith("_"):
                continue

            # allow for optional types
            is_optional_type = t.get_origin(ptype) is t.Union and type(
                None
            ) in t.get_args(ptype)
            value = obj.get(pname, None)
            if is_optional_type and value is None:
                continue

            kwargs[pname] = deserialize(obj=obj[pname], otype=ptype)
        return cls(**kwargs)


def ask_confirm_password() -> str:
    """Ask for password confirmation."""
    while True:
        password = ask_or_get_from_env(
            "Please input your password (or press enter): ", True, "OPERATE_PASSWORD"
        )
        confirm_password = ask_or_get_from_env(
            "Please confirm your password: ", True, "OPERATE_PASSWORD"
        )

        if password == confirm_password:
            return password
        else:
            print("Passwords do not match!")


def load_local_config() -> QuickstartConfig:
    """Load the local quickstart configuration."""
    path = OPERATE_HOME / "local_config.json"
    if path.exists():
        config = QuickstartConfig.load(path)
    else:
        config = QuickstartConfig(path)

    return config  # type: ignore[return-value]


def configure_local_config(template: ServiceTemplate) -> QuickstartConfig:
    """Configure local quickstart configuration."""
    config = load_local_config()

    if config.rpc is None:
        config.rpc = {}

    for chain in template["configurations"]:
        while not check_rpc(config.rpc.get(chain)):
            config.rpc[chain] = ask_or_get_from_env(
                f"Enter a {CHAIN_TO_METADATA[chain]['name']} RPC that supports eth_newFilter [hidden input]: ",
                True,
                f"{chain.upper()}_LEDGER_RPC",
            )
        os.environ[f"{chain.upper()}_LEDGER_RPC"] = config.rpc[chain]

    if config.password_migrated is None:
        config.password_migrated = False

    if config.principal_chain is None:
        config.principal_chain = template["home_chain"]

    agent_id = template["configurations"][config.principal_chain]["agent_id"]
    home_chain = Chain.from_string(config.principal_chain)
    staking_ctr = t.cast(
        StakingTokenContract,
        StakingTokenContract.from_dir(
            directory=str(DATA_DIR / "contracts" / "staking_token")
        ),
    )
    ledger_api = make_ledger_api(
        LedgerType.ETHEREUM.lower(),
        address=config.rpc[config.principal_chain],
        chain_id=home_chain.id,
    )

    if config.staking_program_id is None:
        print_section("Please, select your staking program preference")
        available_choices = {}
        ids = [NO_STAKING_PROGRAM_ID] + [
            id
            for id in STAKING[home_chain]
            if id in QS_STAKING_PROGRAMS[home_chain]
            and QS_STAKING_PROGRAMS[home_chain][id] == agent_id
        ]

        for index, program_id in enumerate(ids):
            if program_id == NO_STAKING_PROGRAM_ID:
                metadata = NO_STAKING_PROGRAM_METADATA
            else:
                instance = staking_ctr.get_instance(
                    ledger_api=ledger_api,
                    contract_address=STAKING[home_chain][program_id],
                )
                try:
                    metadata_hash = instance.functions.metadataHash().call().hex()
                    ipfs_address = IPFS_ADDRESS.format(hash=metadata_hash)
                    response = requests.get(ipfs_address)
                    if response.status_code != 200:
                        raise requests.RequestException(
                            f"Failed to fetch data from {ipfs_address}: {response.status_code}"
                        )
                    metadata = response.json()
                except (Web3Exception, requests.RequestException):
                    metadata = {
                        "name": program_id,
                        "description": program_id,
                        "available_staking_slots": "?",
                    }

                # Add staking slots count to successful response
                try:
                    max_services = instance.functions.maxNumServices().call()
                    current_services = instance.functions.getServiceIds().call()
                    metadata["available_staking_slots"] = max_services - len(
                        current_services
                    )
                except Web3Exception:
                    metadata["available_staking_slots"] = "?"

            name = metadata["name"]
            description = metadata["description"]
            available_slots = metadata["available_staking_slots"]
            wrapped_description = textwrap.fill(
                description, width=80, initial_indent="   ", subsequent_indent="   "
            )
            print(
                f"{index + 1}) {name}\t(available slots : {available_slots})\n{wrapped_description}\n"
            )
            if available_slots != 0:
                available_choices[index + 1] = {
                    "program_id": program_id,
                    "slots": available_slots,
                    "name": name,
                }

        while True:
            try:
                input_value = ask_or_get_from_env(
                    f"Enter your choice (1 - {len(ids)}): ", False, "STAKING_PROGRAM"
                )
                try:
                    choice = int(input_value)
                    if choice not in available_choices:
                        print("\nPlease select a program with available slots:")
                        for idx, prog in available_choices.items():
                            print(
                                f"{idx}) {prog['name']} : available slots {prog['slots']}"
                            )
                        continue
                    selected_program = available_choices[choice]
                    config.staking_program_id = selected_program["program_id"]
                    print(f"Selected staking program: {selected_program['name']}")
                    break
                except ValueError:
                    if input_value in ids:
                        config.staking_program_id = input_value
                        break
                    else:
                        raise ValueError(f"STAKING_PROGRAM must be one of {ids}")
            except Exception as e:
                print(f"Error in getting input: {str(e)}")
                raise

    # set chain configs in the service template
    for chain in template["configurations"]:
        if chain == config.principal_chain:
            if config.staking_program_id == NO_STAKING_PROGRAM_ID:
                min_staking_deposit = 1
            else:
                instance = staking_ctr.get_instance(
                    ledger_api=ledger_api,
                    contract_address=STAKING[home_chain][config.staking_program_id],
                )
                min_staking_deposit = int(instance.functions.minStakingDeposit().call())

            template["configurations"][chain] |= {
                "staking_program_id": config.staking_program_id,
                "rpc": config.rpc[chain],
                "use_staking": config.staking_program_id != NO_STAKING_PROGRAM_ID,
                "cost_of_bond": min_staking_deposit,
            }
        else:
            template["configurations"][chain] |= {
                "staking_program_id": NO_STAKING_PROGRAM_ID,
                "rpc": config.rpc[chain],
                "use_staking": False,
                "cost_of_bond": 1,
            }

    if config.user_provided_args is None:
        config.user_provided_args = {}

    if any(
        (
            env_var_data["provision_type"] == ServiceEnvProvisionType.USER
            and env_var_name not in config.user_provided_args
        )
        for env_var_name, env_var_data in template["env_variables"].items()
    ):
        print_section("Please enter the arguments that will be used by the service.")

    for env_var_name, env_var_data in template["env_variables"].items():
        if env_var_data["provision_type"] == ServiceEnvProvisionType.USER:
            if env_var_name not in config.user_provided_args:
                print(f"Description: {env_var_data['description']}")
                if env_var_data["value"]:
                    print(f"Example: {env_var_data['value']}")
                config.user_provided_args[env_var_name] = ask_or_get_from_env(
                    f"Please enter {env_var_data['name']}: ", False, env_var_name
                )
                print()

            template["env_variables"][env_var_name][
                "value"
            ] = config.user_provided_args[env_var_name]

        # TODO: Handle it in a more generic way
        if (
            template["env_variables"][env_var_name]["provision_type"]
            == ServiceEnvProvisionType.COMPUTED
            and "SUBGRAPH_API_KEY" in config.user_provided_args
            and "{SUBGRAPH_API_KEY}" in template["env_variables"][env_var_name]["value"]
        ):
            template["env_variables"][env_var_name]["value"] = template[
                "env_variables"
            ][env_var_name]["value"].format(
                SUBGRAPH_API_KEY=config.user_provided_args["SUBGRAPH_API_KEY"],
            )

    config.store()
    return config


def ask_password_if_needed(operate: "OperateApp", config: QuickstartConfig) -> None:
    """Ask password if needed."""
    if operate.user_account is None:
        print_section("Set up local user account")
        print("Creating a new local user account...")
        password = ask_confirm_password()
        UserAccount.new(
            password=password,
            path=operate._path / "user.json",
        )
        config.password_migrated = True
        config.store()
    else:
        _password = None
        while _password is None:
            _password = ask_or_get_from_env(
                "\nEnter local user account password [hidden input]: ",
                True,
                "OPERATE_PASSWORD",
            )
            if operate.user_account.is_valid(password=_password):
                break
            _password = None
            print("Invalid password!")

        password = _password

    operate.password = password


def get_service(manager: ServiceManager, template: ServiceTemplate) -> Service:
    """Get service."""
    if len(manager.json) > 0:
        old_hash = manager.json[0]["hash"]
        if old_hash == template["hash"]:
            print(f'Loading service {template["hash"]}')
            service = manager.load(
                service_config_id=manager.json[0]["service_config_id"],
            )
        else:
            print(f"Updating service from {old_hash} to " + template["hash"])
            service = manager.update(
                service_config_id=manager.json[0]["service_config_id"],
                service_template=template,
            )

        service.env_variables = template["env_variables"]
        service.store()
    else:
        print(f'Creating service {template["hash"]}')
        service = manager.load_or_create(
            hash=template["hash"],
            service_template=template,
        )

    return service


def ask_funds_in_address(
    ledger_api: LedgerApi,
    required_balance: int,
    asset_address: str,
    recipient_name: str,
    recipient_address: str,
    chain: str,
) -> None:
    """Ask for funds in address."""
    if required_balance > get_asset_balance(
        ledger_api, asset_address, recipient_address
    ):
        print(
            f"[{chain}] Please make sure {recipient_name} {recipient_address} "
            f"has at least {wei_to_token(required_balance, chain, asset_address)}",
        )
        waiting_for_amount = required_balance - get_asset_balance(
            ledger_api, asset_address, recipient_address
        )
        spinner = Halo(
            text=f"[{chain}] Waiting for at least {wei_to_token(waiting_for_amount, chain, asset_address)}...",
            spinner="dots",
        )
        spinner.start()

        while True:
            time.sleep(1)
            updated_balance = get_asset_balance(
                ledger_api, asset_address, recipient_address
            )
            if updated_balance >= required_balance:
                break

        spinner.succeed(
            f"[{chain}] {recipient_name} updated balance: {wei_to_token(updated_balance, chain, asset_address)}."
        )


def ensure_enough_funds(operate: "OperateApp", service: Service) -> None:
    """Ensure enough funds."""
    if not operate.wallet_manager.exists(ledger_type=LedgerType.ETHEREUM):
        print("Creating the Master EOA...")
        wallet, mnemonic = operate.wallet_manager.create(
            ledger_type=LedgerType.ETHEREUM
        )
        wallet.password = operate.password
        print_box(
            f"Please save the mnemonic phrase for the Master EOA:\n{', '.join(mnemonic)}",
            0,
            "-",
        )
        ask_or_get_from_env(
            "Press enter to continue...", False, "CONTINUE", raise_if_missing=False
        )
    else:
        wallet = operate.wallet_manager.load(ledger_type=LedgerType.ETHEREUM)

    manager = operate.service_manager()
    config = load_local_config()

    for chain_name, chain_config in service.chain_configs.items():
        print_section(f"[{chain_name}] Set up the service in the Olas Protocol")
        chain_metadata = CHAIN_TO_METADATA[chain_name]

        if chain_config.ledger_config.rpc is not None:
            os.environ["CUSTOM_CHAIN_RPC"] = chain_config.ledger_config.rpc

        chain = chain_config.ledger_config.chain
        ledger_api = wallet.ledger_api(
            chain=chain,
            rpc=chain_config.ledger_config.rpc,
        )

        for (
            asset_address,
            fund_requirements,
        ) in chain_config.chain_data.user_params.fund_requirements.items():
            gas_fund_req = 0
            agent_fund_requirement = fund_requirements.agent
            safe_fund_requirement = fund_requirements.safe
            service_state = manager._get_on_chain_state(service, chain_name)
            if asset_address == ZERO_ADDRESS:
                gas_fund_req = t.cast(int, chain_metadata.get("gasFundReq"))
                if service_state in (
                    OnChainState.NON_EXISTENT,
                    OnChainState.PRE_REGISTRATION,
                    OnChainState.ACTIVE_REGISTRATION,
                ):
                    agent_fund_requirement += (
                        2  # for 1 wei in msg.value during registration and activation
                    )

            # print the master EOA balance that was created above
            balance_str = wei_to_token(
                get_asset_balance(ledger_api, asset_address, wallet.crypto.address),
                chain_name,
                asset_address,
            )
            print(
                f"[{chain_name}] Master EOA balance: {balance_str}",
            )

            # if master safe exists print its balance
            safe_exists = wallet.safes.get(chain) is not None
            if safe_exists:
                balance_str = wei_to_token(
                    get_asset_balance(ledger_api, asset_address, wallet.safes[chain]),
                    chain_name,
                    asset_address,
                )
                print(f"[{chain_name}] Master safe balance: {balance_str}")

            # if service safe exists print its balance
            if chain_config.chain_data.multisig != NON_EXISTENT_MULTISIG:
                service_save_balance = get_asset_balance(
                    ledger_api, asset_address, chain_config.chain_data.multisig
                )
                print(
                    f"[{chain_name}] Service safe balance: {wei_to_token(service_save_balance, chain_name, asset_address)}"
                )
                if service_save_balance >= safe_fund_requirement:
                    safe_fund_requirement = (
                        0  # no need to fund the service safe if it has enough funds
                    )

            # if agent EOA exists print its balance
            if len(service.keys) > 0:
                agent_eoa_balance = get_asset_balance(
                    ledger_api, asset_address, service.keys[0].address
                )
                print(
                    f"[{chain_name}] Agent EOA balance: {wei_to_token(agent_eoa_balance, chain_name, asset_address)}"
                )
                if agent_eoa_balance >= agent_fund_requirement:
                    agent_fund_requirement = (
                        0  # no need to fund the agent EOA if it has enough funds
                    )

            # ask for enough funds in master EOA for gas fees
            ask_funds_in_address(
                ledger_api=ledger_api,
                required_balance=gas_fund_req,
                asset_address=asset_address,
                recipient_name="Master EOA",
                recipient_address=wallet.crypto.address,
                chain=chain_name,
            )

            # if master safe does not exist, create it
            if not safe_exists:
                print(f"[{chain_name}] Creating Master Safe")
                wallet_manager = operate.wallet_manager
                wallet = wallet_manager.load(ledger_type=LedgerType.ETHEREUM)
                backup_owner = ask_or_get_from_env(
                    "Please input your backup owner (leave empty to skip): ",
                    False,
                    "BACKUP_OWNER",
                    raise_if_missing=False,
                )

                wallet.create_safe(
                    chain=chain,
                    rpc=chain_config.ledger_config.rpc,
                    backup_owner=None if backup_owner == "" else backup_owner,
                )

            # ask for enough funds in master safe for agent EOA + service safe
            ask_funds_in_address(
                ledger_api=ledger_api,
                required_balance=agent_fund_requirement + safe_fund_requirement,
                asset_address=asset_address,
                recipient_name="Master Safe",
                recipient_address=wallet.safes[chain],
                chain=chain_name,
            )

        # if staking, ask for the required OLAS for it
        if chain_config.chain_data.user_params.use_staking:
            assert (  # nosec
                config.staking_program_id is not None
            ), "Staking vars not found"  # nosec
            if service_state in (
                OnChainState.NON_EXISTENT,
                OnChainState.PRE_REGISTRATION,
            ):
                required_olas = 2 * chain_config.chain_data.user_params.cost_of_bond
            elif service_state == OnChainState.ACTIVE_REGISTRATION:
                required_olas = chain_config.chain_data.user_params.cost_of_bond
            else:
                required_olas = 0

            sftxb = manager.get_eth_safe_tx_builder(
                ledger_config=chain_config.ledger_config
            )
            staking_contract = STAKING[chain_config.ledger_config.chain][
                config.staking_program_id
            ]
            ask_funds_in_address(
                ledger_api=ledger_api,
                required_balance=required_olas,
                asset_address=sftxb.get_staking_params(staking_contract)[
                    "staking_token"
                ],
                recipient_name="Master Safe",
                recipient_address=wallet.safes[chain],
                chain=chain_name,
            )


def run_service(
    operate: "OperateApp", config_path: str, build_only: bool = False
) -> None:
    """Run service."""

    with open(config_path, "r") as config_file:
        template = json.load(config_file)

    print_title(f"{template['name']} quickstart")
    config = configure_local_config(template)
    manager = operate.service_manager()
    service = get_service(manager, template)
    ask_password_if_needed(operate, config)

    # reload manger and config after setting operate.password
    manager = operate.service_manager()
    config = load_local_config()
    ensure_enough_funds(operate, service)

    print_box("PLEASE, DO NOT INTERRUPT THIS PROCESS.")
    print_section(f"Deploying on-chain service on {config.principal_chain}...")
    print(
        "Cancelling the on-chain service update prematurely could lead to an inconsistent state of the Safe or the on-chain service state, which may require manual intervention to resolve.\n"
    )
    manager.deploy_service_onchain_from_safe(
        service_config_id=service.service_config_id
    )

    print_section("Funding the service")
    manager.fund_service(service_config_id=service.service_config_id)

    print_section("Deploying the service")
    manager.deploy_service_locally(
        service_config_id=service.service_config_id,
        use_docker=True,
        use_kubernetes=True,
        build_only=build_only,
    )
    if build_only:
        print_section(f"Built the {template['name']}")
    else:
        print_section(f"Starting the {template['name']}")
