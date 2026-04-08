from __future__ import annotations


def profit_estimate(revenue: float, cost_ratio: float = 0.55) -> dict:
    """
    Dummy profit analyzer.

    TODO: incorporate fabric costs, labor, shipping, payment gateway fees, refunds, payouts.
    """
    cost = revenue * cost_ratio
    profit = revenue - cost
    return {"revenue": round(revenue, 2), "estimated_cost": round(cost, 2), "estimated_profit": round(profit, 2)}

