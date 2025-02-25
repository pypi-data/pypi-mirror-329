import rstr
from faker import Faker
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from wbcore.contrib.io.resources import FilterModelResource
from wbfdm.models import Instrument

from wbportfolio.models import Trade, TradeProposal

fake = Faker()


class TradeProposalTradeResource(FilterModelResource):
    """
    Trade Resource class to use to import trade from the trade proposal
    """

    def __init__(self, **kwargs):
        self.trade_proposal = TradeProposal.objects.get(pk=kwargs["trade_proposal_id"])
        super().__init__(**kwargs)

    def before_import(self, dataset, **kwargs):
        Trade.objects.filter(trade_proposal=self.trade_proposal).delete()

    def get_or_init_instance(self, instance_loader, row):
        try:
            return Trade.objects.get(
                trade_proposal=self.trade_proposal, underlying_instrument=row["underlying_instrument"]
            )
        except Trade.DoesNotExist:
            return Trade(
                trade_proposal=self.trade_proposal,
                underlying_instrument=row["underlying_instrument"],
                transaction_subtype=Trade.Type.BUY if row["weighting"] > 0 else Trade.Type.SELL,
                currency=row["underlying_instrument"].currency,
                transaction_date=self.trade_proposal.trade_date,
                portfolio=self.trade_proposal.portfolio,
                weighting=row["weighting"],
                status=Trade.Status.DRAFT,
            )

    DUMMY_FIELD_MAP = {
        "underlying_instrument": lambda: rstr.xeger("([A-Z]{2}[A-Z0-9]{9}[0-9]{1})"),
        "weighting": 1.0,
        "shares": 1000.2536,
        "comment": lambda: fake.sentence(),
        "order": 1,
    }
    underlying_instrument = fields.Field(
        column_name="underlying_instrument",
        attribute="underlying_instrument",
        widget=ForeignKeyWidget(Instrument, field="isin"),
    )

    class Meta:
        import_id_fields = ("underlying_instrument",)
        fields = (
            "id",
            "underlying_instrument",
            "weighting",
            "shares",
            "comment",
            "order",
        )
        export_order = fields
        model = Trade
