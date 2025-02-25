from decimal import Decimal

import pandas as pd
from django.db.models import Q, QuerySet
from wbfdm.enums import MarketData
from wbfdm.models import (
    Classification,
    Exchange,
    Instrument,
    InstrumentClassificationThroughModel,
    InstrumentListThroughModel,
)

from wbportfolio.pms.typing import Portfolio, Position
from wbportfolio.rebalancing.base import AbstractRebalancingModel
from wbportfolio.rebalancing.decorators import register


@register("Market Capitalization Rebalancing")
class MarketCapitalizationRebalancing(AbstractRebalancingModel):
    TARGET_CURRENCY: str = "USD"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instruments = self._get_instruments(**kwargs)
        self.market_cap_df = pd.DataFrame(
            instruments.dl.market_data(
                values=[MarketData.MARKET_CAPITALIZATION],
                from_date=self.last_effective_date,
                to_date=self.trade_date,
                target_currency=self.TARGET_CURRENCY,
            )
        )
        self.exchange_df = pd.DataFrame(
            instruments.values_list("id", "exchange"), columns=["id", "exchange"]
        ).set_index("id")
        try:
            self.market_cap_df = self.market_cap_df[
                ["valuation_date", "market_capitalization", "instrument_id"]
            ].pivot_table(index="valuation_date", columns="instrument_id", values="market_capitalization")
            # self.market_cap_df = df.iloc[-1, :].transpose()
        except (IndexError, KeyError):
            self.market_cap_df = pd.DataFrame()

    def _get_instruments(
        self,
        classification_ids: list[int] | None = None,
        instrument_ids: list[int] | None = None,
        instrument_list_id: int | None = None,
    ) -> QuerySet[Instrument]:
        """
        Use the provided kwargs to return a list of instruments as universe.
        - If classifications are given, we returns all the instrument linked to these classifications
        - Or directly from a static list of instrument ids
        - fallback to the last effective portfolio underlying instruments list
        """
        if not instrument_ids:
            instrument_ids = []
        if classification_ids:
            classifications = set()
            for classification in Classification.objects.filter(id__in=classification_ids):
                for children in classification.get_descendants(include_self=True):
                    classifications.add(children)
            instrument_ids.extend(
                list(
                    InstrumentClassificationThroughModel.objects.filter(
                        classification__in=classifications
                    ).values_list("id", flat=True)
                )
            )
        if instrument_list_id:
            instrument_ids.extend(
                list(
                    InstrumentListThroughModel.objects.filter(instrument_list_id=instrument_list_id).values_list(
                        "instrument", flat=True
                    )
                )
            )

        if not instrument_ids:
            instrument_ids = list(
                self.portfolio.assets.filter(date=self.last_effective_date).values_list(
                    "underlying_instrument", flat=True
                )
            )

        return Instrument.objects.filter(id__in=instrument_ids).filter(
            (Q(delisted_date__isnull=True) | Q(delisted_date__gt=self.trade_date))
        )

    def is_valid(self) -> bool:
        if not self.market_cap_df.empty:
            trade_date_mktp_cap = (
                self.market_cap_df.loc[self.trade_date, :].transpose().rename("market_capitalization")
            )
            df = pd.concat(
                [trade_date_mktp_cap, self.exchange_df], axis=1
            )  # if we are missing any market cap for not-delisted instrument, we consider the rebalancing not valid
            df = df.groupby("exchange", dropna=False)["market_capitalization"].any()
            missing_exchanges = Exchange.objects.filter(id__in=df[~df].index.to_list())
            if missing_exchanges.exists():
                setattr(
                    self,
                    "_validation_errors",
                    f"Couldn't find any market capitalization for exchanges {', '.join([str(e) for e in missing_exchanges])}",
                )
            return df.all()
        return False

    def get_target_portfolio(self) -> Portfolio:
        positions = []
        market_cap_df = self.market_cap_df.ffill().loc[self.trade_date, :].transpose()
        total_market_cap = market_cap_df.sum()

        for underlying_instrument, market_cap in market_cap_df.to_dict().items():
            positions.append(
                Position(
                    underlying_instrument=underlying_instrument,
                    weighting=Decimal(market_cap / total_market_cap),
                    date=self.trade_date,
                )
            )
        return Portfolio(positions=tuple(positions))
