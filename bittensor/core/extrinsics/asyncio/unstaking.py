import asyncio
from asyncio import sleep
from typing import Union, Optional, TYPE_CHECKING

from bittensor.core.errors import StakeError, NotRegisteredError
from bittensor.utils import format_error_message, unlock_key
from bittensor.utils.balance import Balance
from bittensor.utils.btlogging import logging

if TYPE_CHECKING:
    from bittensor_wallet import Wallet
    from bittensor.core.async_subtensor import AsyncSubtensor


async def _do_unstake(
    subtensor: "AsyncSubtensor",
    wallet: "Wallet",
    hotkey_ss58: str,
    amount: "Balance",
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
) -> bool:
    """
    Sends an unstake extrinsic to the chain.

    Args:
        wallet: Wallet object that can sign the extrinsic.
        hotkey_ss58: Hotkey `ss58` address to unstake from.
        amount: Amount to unstake.
        wait_for_inclusion: If `True`, waits for inclusion before returning.
        wait_for_finalization: If `True`, waits for finalization before returning.

    Returns:
        success: `True` if the extrinsic was successful.

    Raises:
        StakeError: If the extrinsic failed.
    """
    async with subtensor.substrate as substrate:
        call = await substrate.compose_call(
            call_module="SubtensorModule",
            call_function="remove_stake",
            call_params={"hotkey": hotkey_ss58, "amount_unstaked": amount.rao},
        )
        extrinsic = await substrate.create_signed_extrinsic(
            call=call, keypair=wallet.coldkey
        )
        response = substrate.submit_extrinsic(
            extrinsic,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization,
        )
        # We only wait here if we expect finalization.
        if not wait_for_finalization and not wait_for_inclusion:
            return True

        if response.is_success:
            return True
        else:
            raise StakeError(format_error_message(response.error_message))


async def _check_threshold_amount(
    subtensor: "AsyncSubtensor", stake_balance: "Balance"
) -> bool:
    """
    Checks if the remaining stake balance is above the minimum required stake threshold.

    Args:
        subtensor: Subtensor instance.
        stake_balance: the balance to check for threshold limits.

    Returns:
        success: `True` if the unstaking is above the threshold or 0, or `False` if the unstaking is below
            the threshold, but not 0.
    """
    min_req_stake: Balance = await subtensor.get_minimum_required_stake()

    if min_req_stake > stake_balance > 0:
        logging.warning(
            f":cross_mark: [yellow]Remaining stake balance of {stake_balance} less than minimum of "
            f"{min_req_stake} TAO[/yellow]"
        )
        return False
    else:
        return True


async def __do_remove_stake_single(
    subtensor: "AsyncSubtensor",
    wallet: "Wallet",
    hotkey_ss58: str,
    amount: "Balance",
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
) -> bool:
    """
    Executes an unstake call to the chain using the wallet and the amount specified.

    Args:
        wallet: Bittensor wallet object.
        hotkey_ss58: Hotkey address to unstake from.
        amount: Amount to unstake as Bittensor balance object.
        wait_for_inclusion: If set, waits for the extrinsic to enter a block before returning `True`, or returns `False`
            if the extrinsic fails to enter the block within the timeout.
        wait_for_finalization: If set, waits for the extrinsic to be finalized on the chain before returning `True`, or
            returns `False` if the extrinsic fails to be finalized within the timeout.

    Returns:
        success: Flag is `True` if extrinsic was finalized or included in the block. If we did not wait for
            finalization/inclusion, the response is `True`.

    Raises:
        StakeError: If the extrinsic fails to be finalized or included in the block.
        NotRegisteredError: If the hotkey is not registered in any subnets.

    """
    if not (unlock := unlock_key(wallet)).success:
        logging.error(unlock.message)
        return False

    call = await subtensor.substrate.compose_call(
        call_module="SubtensorModule",
        call_function="remove_stake",
        call_params={"hotkey": hotkey_ss58, "amount_unstaked": amount.rao},
    )
    success, err_msg = await subtensor.sign_and_send_extrinsic(
        call,
        wallet,
        wait_for_inclusion=wait_for_inclusion,
        wait_for_finalization=wait_for_finalization,
    )
    if success:
        return True
    else:
        raise StakeError(format_error_message(err_msg))


async def unstake_extrinsic(
    subtensor: "AsyncSubtensor",
    wallet: "Wallet",
    hotkey_ss58: Optional[str] = None,
    amount: Optional[Union[Balance, float]] = None,
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
) -> bool:
    """
    Removes stake into the wallet coldkey from the specified hotkey `uid`.

    Args:
        subtensor: AsyncSubtensor instance.
        wallet: Bittensor wallet object.
        hotkey_ss58: The `ss58` address of the hotkey to unstake from. By default, the wallet hotkey is used.
        amount: Amount to stake as Bittensor balance, or `float` interpreted as Tao.
        wait_for_inclusion: If set, waits for the extrinsic to enter a block before returning `True`, or returns
            `False` if the extrinsic fails to enter the block within the timeout.
        wait_for_finalization: If set, waits for the extrinsic to be finalized on the chain before returning `True`,
            or returns `False` if the extrinsic fails to be finalized within the timeout.

    Returns:
        success: Flag is `True`` if extrinsic was finalized or included in the block. If we did not wait for
            finalization/inclusion, the response is `True`.
    """
    # Decrypt keys,
    if not (unlock := unlock_key(wallet)).success:
        logging.error(unlock.message)
        return False

    if hotkey_ss58 is None:
        hotkey_ss58 = wallet.hotkey.ss58_address  # Default to wallet's own hotkey.

    logging.info(
        f":satellite: [magenta]Syncing with chain:[/magenta] [blue]{subtensor.network}[/blue] [magenta]...[/magenta]"
    )
    block_hash = await subtensor.substrate.get_chain_head()
    old_balance_, old_stake, hotkey_owner = await asyncio.gather(
        subtensor.get_balance(wallet.coldkeypub.ss58_address, block_hash=block_hash),
        subtensor.get_stake_for_coldkey_and_hotkey(
            coldkey_ss58=wallet.coldkeypub.ss58_address,
            hotkey_ss58=hotkey_ss58,
            block_hash=block_hash,
        ),
        subtensor.get_hotkey_owner(hotkey_ss58, block_hash=block_hash),
    )
    old_balance = old_balance_[wallet.coldkeypub.ss58_address]
    own_hotkey: bool = wallet.coldkeypub.ss58_address == hotkey_owner

    # Convert to bittensor.Balance
    if amount is None:
        # Unstake it all.
        unstaking_balance = old_stake
    elif not isinstance(amount, Balance):
        unstaking_balance = Balance.from_tao(amount)
    else:
        unstaking_balance = amount

    # Check enough to unstake.
    stake_on_uid = old_stake
    if unstaking_balance > stake_on_uid:
        logging.error(
            f":cross_mark: [red]Not enough stake[/red]: [green]{stake_on_uid}[/green] to unstake: "
            f"[blue]{unstaking_balance}[/blue] from hotkey: [yellow]{wallet.hotkey_str}[/yellow]"
        )
        return False

    # If nomination stake, check threshold.
    if not own_hotkey and not await _check_threshold_amount(
        subtensor=subtensor, stake_balance=(stake_on_uid - unstaking_balance)
    ):
        logging.warning(
            ":warning: [yellow]This action will unstake the entire staked balance![/yellow]"
        )
        unstaking_balance = stake_on_uid

    try:
        logging.info(
            f":satellite: [magenta]Unstaking from chain:[/magenta] [blue]{subtensor.network}[/blue] [magenta]...[/magenta]"
        )
        staking_response: bool = __do_remove_stake_single(
            subtensor=subtensor,
            wallet=wallet,
            hotkey_ss58=hotkey_ss58,
            amount=unstaking_balance,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization,
        )

        if staking_response is True:  # If we successfully unstaked.
            # We only wait here if we expect finalization.
            if not wait_for_finalization and not wait_for_inclusion:
                return True

            logging.success(":white_heavy_check_mark: [green]Finalized[/green]")

            logging.info(
                f":satellite: [magenta]Checking Balance on:[/magenta] [blue]{subtensor.network}[/blue] [magenta]...[/magenta]"
            )
            block_hash = await subtensor.substrate.get_chain_head()
            new_balance_, new_stake = await asyncio.gather(
                subtensor.get_balance(
                    wallet.coldkeypub.ss58_address, block_hash=block_hash
                ),
                subtensor.get_stake_for_coldkey_and_hotkey(
                    coldkey_ss58=wallet.coldkeypub.ss58_address,
                    hotkey_ss58=hotkey_ss58,
                    block_hash=block_hash,
                ),
            )
            new_balance = new_balance_[wallet.coldkeypub.ss58_address]
            logging.info("Balance:")
            logging.info(
                f"\t\t[blue]{old_balance}[/blue] :arrow_right: [green]{new_balance}[/green]"
            )
            logging.info("Stake:")
            logging.info(
                f"\t\t[blue]{old_stake}[/blue] :arrow_right: [green]{new_stake}[/green]"
            )
            return True
        else:
            logging.error(":cross_mark: [red]Failed[/red]: Unknown Error.")
            return False

    except NotRegisteredError:
        logging.error(
            f":cross_mark: [red]Hotkey: {wallet.hotkey_str} is not registered.[/red]"
        )
        return False
    except StakeError as e:
        logging.error(":cross_mark: [red]Stake Error: {}[/red]".format(e))
        return False


async def unstake_multiple_extrinsic(
    subtensor: "AsyncSubtensor",
    wallet: "Wallet",
    hotkey_ss58s: list[str],
    amounts: Optional[list[Union[Balance, float]]] = None,
    wait_for_inclusion: bool = True,
    wait_for_finalization: bool = False,
) -> bool:
    """Removes stake from each `hotkey_ss58` in the list, using each amount, to a common coldkey.

    Args:
        subtensor: Subtensor instance.
        wallet: The wallet with the coldkey to unstake to.
        hotkey_ss58s: List of hotkeys to unstake from.
        amounts: List of amounts to unstake. If `None`, unstake all.
        wait_for_inclusion: If set, waits for the extrinsic to enter a block before returning `True`, or returns `False`
            if the extrinsic fails to enter the block within the timeout.
        wait_for_finalization: If set, waits for the extrinsic to be finalized on the chain before returning `True`, or
            returns `False` if the extrinsic fails to be finalized within the timeout.

    Returns:
        success: Flag is `True` if extrinsic was finalized or included in the block. Flag is `True` if any wallet was
            unstaked. If we did not wait for finalization/inclusion, the response is `True`.
    """
    if not isinstance(hotkey_ss58s, list) or not all(
        isinstance(hotkey_ss58, str) for hotkey_ss58 in hotkey_ss58s
    ):
        raise TypeError("hotkey_ss58s must be a list of str")

    if len(hotkey_ss58s) == 0:
        return True

    if amounts is not None and len(amounts) != len(hotkey_ss58s):
        raise ValueError("amounts must be a list of the same length as hotkey_ss58s")

    if amounts is not None and not all(
        isinstance(amount, (Balance, float)) for amount in amounts
    ):
        raise TypeError(
            "amounts must be a [list of bittensor.Balance or float] or None"
        )

    if amounts is None:
        amounts = [None] * len(hotkey_ss58s)
    else:
        # Convert to Balance
        amounts = [
            Balance.from_tao(amount) if isinstance(amount, float) else amount
            for amount in amounts
        ]

        if sum(amount.tao for amount in amounts) == 0:
            # Staking 0 tao
            return True

    # Unlock coldkey.
    if not (unlock := unlock_key(wallet)).success:
        logging.error(unlock.message)
        return False

    logging.info(
        f":satellite: [magenta]Syncing with chain:[/magenta] [blue]{subtensor.network}[/blue] [magenta]...[/magenta]"
    )
    block_hash = await subtensor.substrate.get_chain_head()
    old_balance_, old_stakes, hotkeys_ = await asyncio.gather(
        subtensor.get_balance(wallet.coldkeypub.ss58_address, block_hash=block_hash),
        asyncio.gather(
            *[
                subtensor.get_stake_for_coldkey_and_hotkey(
                    coldkey_ss58=wallet.coldkeypub.ss58_address,
                    hotkey_ss58=hotkey_ss58,
                    block_hash=block_hash,
                )
                for hotkey_ss58 in hotkey_ss58s
            ]
        ),
        asyncio.gather(
            *[
                subtensor.get_hotkey_owner(hotkey_ss58, block_hash=block_hash)
                for hotkey_ss58 in hotkey_ss58s
            ]
        ),
    )
    old_balance = old_balance_[wallet.coldkeypub.ss58_address]
    own_hotkeys = [
        (wallet.coldkeypub.ss58_address == hotkey_owner) for hotkey_owner in hotkeys_
    ]

    successful_unstakes = 0
    for idx, (hotkey_ss58, amount, old_stake, own_hotkey) in enumerate(
        zip(hotkey_ss58s, amounts, old_stakes, own_hotkeys)
    ):
        # Covert to bittensor.Balance
        if amount is None:
            # Unstake it all.
            unstaking_balance = old_stake
        else:
            unstaking_balance = (
                amount if isinstance(amount, Balance) else Balance.from_tao(amount)
            )

        # Check enough to unstake.
        stake_on_uid = old_stake
        if unstaking_balance > stake_on_uid:
            logging.error(
                f":cross_mark: [red]Not enough stake[/red]: [green]{stake_on_uid}[/green] to unstake: "
                f"[blue]{unstaking_balance}[/blue] from hotkey: [blue]{wallet.hotkey_str}[/blue]."
            )
            continue

        # If nomination stake, check threshold.
        if not own_hotkey and not await _check_threshold_amount(
            subtensor=subtensor, stake_balance=(stake_on_uid - unstaking_balance)
        ):
            logging.warning(
                ":warning: [yellow]This action will unstake the entire staked balance![/yellow]"
            )
            unstaking_balance = stake_on_uid

        try:
            logging.info(
                f":satellite: [magenta]Unstaking from chain:[/magenta] [blue]{subtensor.network}[/blue] "
                f"[magenta]...[/magenta]"
            )
            staking_response: bool = await __do_remove_stake_single(
                subtensor=subtensor,
                wallet=wallet,
                hotkey_ss58=hotkey_ss58,
                amount=unstaking_balance,
                wait_for_inclusion=wait_for_inclusion,
                wait_for_finalization=wait_for_finalization,
            )

            if staking_response is True:  # If we successfully unstaked.
                # We only wait here if we expect finalization.

                if idx < len(hotkey_ss58s) - 1:
                    # Wait for tx rate limit.
                    tx_rate_limit_blocks = await subtensor.tx_rate_limit()
                    if tx_rate_limit_blocks > 0:
                        logging.info(
                            f":hourglass: [yellow]Waiting for tx rate limit: "
                            f"[white]{tx_rate_limit_blocks}[/white] blocks[/yellow]"
                        )
                        await sleep(tx_rate_limit_blocks * 12)  # 12 seconds per block

                if not wait_for_finalization and not wait_for_inclusion:
                    successful_unstakes += 1
                    continue

                logging.info(":white_heavy_check_mark: [green]Finalized[/green]")

                logging.info(
                    f":satellite: [magenta]Checking Balance on:[/magenta] [blue]{subtensor.network}[/blue] "
                    f"[magenta]...[/magenta]..."
                )
                block_hash = await subtensor.substrate.get_chain_head()
                new_stake = subtensor.get_stake_for_coldkey_and_hotkey(
                    coldkey_ss58=wallet.coldkeypub.ss58_address,
                    hotkey_ss58=hotkey_ss58,
                    block_hash=block_hash,
                )
                logging.info(
                    f"Stake ({hotkey_ss58}): [blue]{stake_on_uid}[/blue] :arrow_right: [green]{new_stake}[/green]"
                )
                successful_unstakes += 1
            else:
                logging.error(":cross_mark: [red]Failed: Unknown Error.[/red]")
                continue

        except NotRegisteredError:
            logging.error(
                f":cross_mark: [red]Hotkey[/red] [blue]{hotkey_ss58}[/blue] [red]is not registered.[/red]"
            )
            continue
        except StakeError as e:
            logging.error(":cross_mark: [red]Stake Error: {}[/red]".format(e))
            continue

    if successful_unstakes != 0:
        logging.info(
            f":satellite: [magenta]Checking Balance on:[/magenta] ([blue]{subtensor.network}[/blue] "
            f"[magenta]...[/magenta]"
        )
        new_balance = subtensor.get_balance(wallet.coldkeypub.ss58_address)
        logging.info(
            f"Balance: [blue]{old_balance}[/blue] :arrow_right: [green]{new_balance}[/green]"
        )
        return True

    return False