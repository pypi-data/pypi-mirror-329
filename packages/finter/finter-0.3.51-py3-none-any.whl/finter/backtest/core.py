from typing import Optional, Tuple

import numpy as np
from numba import njit
from typing_extensions import Literal


@njit
def update_target_volume_v0(
    weight: np.ndarray,
    prev_aum: float,
    prev_price: np.ndarray,
    weight_before: np.ndarray,
    target_volume_before: np.ndarray,
    is_first_day: bool = False,
    rebalancing_method: Literal["auto", "W", "M", "Q", "by_position"] = "auto",
    rebalancing_mask: int = 0,
) -> np.ndarray:
    if is_first_day:
        return np.nan_to_num(weight * prev_aum / prev_price)

    elif rebalancing_method == "auto":
        return np.nan_to_num(weight * prev_aum / prev_price)

    elif rebalancing_method == "by_position":
        # ISSUE
        if (np.abs(weight_before - weight) > 1e-10).any():
            return np.nan_to_num(weight * prev_aum / prev_price)
        else:
            return target_volume_before

    elif rebalancing_method in ["W", "M", "Q"]:
        if rebalancing_mask:
            return np.nan_to_num(weight * prev_aum / prev_price)
        else:
            return target_volume_before

    else:
        raise ValueError(f"Invalid rebalancing method: {rebalancing_method}")


@njit
def update_target_volume(
    weight: np.ndarray,
    prev_aum: float,
    prev_price: np.ndarray,
    weight_before: np.ndarray,
    target_volume_before: np.ndarray,
    auto_rebalance: bool = True,
    is_first_day: bool = False,
    rebalancing_mask: int = 0,
) -> np.ndarray:
    if rebalancing_mask:
        return np.nan_to_num(weight * prev_aum / prev_price)
    if auto_rebalance or (np.abs(weight_before - weight) > 1e-10).any() or is_first_day:
        return np.nan_to_num(weight * prev_aum / prev_price)
    else:
        return target_volume_before


@njit
def apply_volume_cap(target_volume: np.ndarray, volume_capacity: np.ndarray):
    return np.minimum(target_volume, volume_capacity)


@njit
def calculate_buy_sell_volumes(
    target_volume: np.ndarray,
    prev_actual_holding_volume: np.ndarray,
    available_sell_volume: Optional[np.ndarray] = None,
    volume_capacity: Optional[np.ndarray] = None,
) -> tuple:
    target_buy_volume = np.maximum(target_volume - prev_actual_holding_volume, 0)
    target_sell_volume = np.maximum(prev_actual_holding_volume - target_volume, 0)

    if volume_capacity is not None:
        target_buy_volume = apply_volume_cap(target_buy_volume, volume_capacity)
        target_sell_volume = apply_volume_cap(target_sell_volume, volume_capacity)

    if available_sell_volume is not None:
        actual_sell_volume = np.minimum(available_sell_volume, target_sell_volume)
    else:
        actual_sell_volume = target_sell_volume

    return target_buy_volume, target_sell_volume, actual_sell_volume


@njit
def execute_transactions(
    actual_sell_volume: np.ndarray,
    buy_price: np.ndarray,
    buy_fee_tax: float,
    sell_price: np.ndarray,
    sell_fee_tax: float,
    prev_cash: float,
    target_buy_volume: np.ndarray,
    actual_sell_amount: Optional[np.ndarray] = None,
    settlement_days: int = 0,
    current_index: int = 0,
) -> Tuple:
    actual_sell_amount_current = np.nan_to_num(
        actual_sell_volume * sell_price * (1 - sell_fee_tax)
    )
    available_buy_amount_non_settled = prev_cash + actual_sell_amount_current.sum()
    if actual_sell_amount is None:
        available_buy_amount = available_buy_amount_non_settled
    else:
        available_buy_amount = calculate_available_buy_amount(
            prev_cash,
            actual_sell_amount,
            settlement_days,
            current_index,
        )

    target_buy_amount = np.nan_to_num(target_buy_volume * buy_price * (1 + buy_fee_tax))
    target_buy_amount_sum = target_buy_amount.sum()
    if target_buy_amount_sum > 0:
        available_buy_volume = np.nan_to_num(
            (target_buy_amount / target_buy_amount_sum)
            * (available_buy_amount / (buy_price * (1 + buy_fee_tax)))
        )
        actual_buy_volume = np.minimum(available_buy_volume, target_buy_volume)
        actual_buy_amount = np.nan_to_num(
            actual_buy_volume * buy_price * (1 + buy_fee_tax)
        )
    else:
        actual_buy_volume = np.zeros_like(target_buy_volume)
        actual_buy_amount = np.zeros_like(target_buy_volume)
    return (
        actual_sell_amount_current,
        available_buy_amount_non_settled,
        actual_buy_volume,
        actual_buy_amount,
    )


@njit
def update_valuation_and_cash(
    prev_actual_holding_volume: np.ndarray,
    actual_buy_volume: np.ndarray,
    actual_sell_volume: np.ndarray,
    price: np.ndarray,
    available_buy_amount: float,
    actual_buy_amount: np.ndarray,
) -> tuple:
    actual_holding_volume = (
        prev_actual_holding_volume + actual_buy_volume - actual_sell_volume
    )
    valuation = np.nan_to_num(actual_holding_volume * price)
    cash = available_buy_amount - actual_buy_amount.sum()
    return actual_holding_volume, valuation, cash


@njit
def update_valuation_and_cash_v0(
    prev_actual_holding_volume: np.ndarray,
    prev_valuation: np.ndarray,
    actual_buy_volume: np.ndarray,
    actual_sell_volume: np.ndarray,
    price: np.ndarray,
    available_buy_amount: float,
    actual_buy_amount: np.ndarray,
    dividend_ratio: Optional[np.ndarray] = None,
    drip: Literal[None, "cash", "reinvest"] = None,
    dividend_tax: float = 0.0,
) -> tuple:
    actual_holding_volume = (
        prev_actual_holding_volume + actual_buy_volume - actual_sell_volume
    )
    # TODO: settle dividend, dividend_tax
    if drip == "reinvest":
        dividend = np.nan_to_num(prev_valuation * dividend_ratio) * (1 - dividend_tax)
        cash = available_buy_amount - actual_buy_amount.sum() + dividend.sum()
    elif drip == "cash":
        dividend = np.nan_to_num(prev_valuation * dividend_ratio) * (1 - dividend_tax)
        cash = available_buy_amount - actual_buy_amount.sum()
    else:
        dividend = np.zeros_like(prev_valuation)
        cash = available_buy_amount - actual_buy_amount.sum()

    valuation = np.nan_to_num(actual_holding_volume * price)
    return actual_holding_volume, valuation, cash, dividend


@njit
def update_aum(
    cash: float,
    valuation: np.ndarray,
    money_flow: float = 0.0,
) -> Tuple[float, float]:
    cash = cash + money_flow
    return cash, cash + valuation.sum()


@njit
def calculate_available_sell_volume(
    actual_holding_volume: np.ndarray,
    actual_sell_volume: np.ndarray,
    i: int,
    settlement_days: int,
) -> np.ndarray:
    if i < settlement_days:
        return np.zeros_like(actual_holding_volume[i])
    else:
        available_sell_volume = actual_holding_volume[i - settlement_days]
        for j in range(settlement_days - 1, 0, -1):
            available_sell_volume -= actual_sell_volume[i - j]

    return available_sell_volume


@njit
def calculate_available_buy_amount(
    prev_cash: float,
    actual_sell_amount: np.ndarray,
    settlement_days: int,
    current_index: int,
) -> float:
    if current_index < settlement_days:
        return prev_cash

    settled_cash = prev_cash
    for i in range(settlement_days - 1, 0, -1):
        settled_cash -= actual_sell_amount[current_index - i].sum()
    return settled_cash
