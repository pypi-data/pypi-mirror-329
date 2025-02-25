from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from wbportfolio.pms.typing import Portfolio, Position
from wbportfolio.rebalancing.base import AbstractRebalancingModel
from wbportfolio.rebalancing.decorators import register


@register("Composite Rebalancing")
class CompositeRebalancing(AbstractRebalancingModel):
    @property
    def base_assets(self) -> dict[int, Decimal]:
        try:
            latest_trade_proposal = self.portfolio.trade_proposals.filter(
                status="APPROVED", trade_date__lte=self.trade_date
            ).latest("trade_date")
            return latest_trade_proposal.base_assets
        except ObjectDoesNotExist:
            return dict()

    def is_valid(self) -> bool:
        return len(self.base_assets.keys()) > 0

    def get_target_portfolio(self) -> Portfolio:
        positions = []
        for underlying_instrument, weighting in self.base_assets.items():
            positions.append(
                Position(underlying_instrument=underlying_instrument, weighting=weighting, date=self.trade_date)
            )
        return Portfolio(positions=tuple(positions))
