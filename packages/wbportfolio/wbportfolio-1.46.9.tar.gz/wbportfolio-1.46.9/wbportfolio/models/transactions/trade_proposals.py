import logging
from contextlib import suppress
from datetime import date, timedelta
from decimal import Decimal
from typing import TypeVar

from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django_fsm import FSMField, transition
from pandas._libs.tslibs.offsets import BDay
from wbcompliance.models.risk_management.mixins import RiskCheckMixin
from wbcore.contrib.icons import WBIcon
from wbcore.enums import RequestType
from wbcore.metadata.configs.buttons import ActionButton
from wbcore.models import WBModel
from wbfdm.models.instruments.instruments import Instrument

from wbportfolio.models.roles import PortfolioRole
from wbportfolio.pms.trading import TradingService
from wbportfolio.pms.typing import Portfolio as PortfolioDTO
from wbportfolio.pms.typing import TradeBatch as TradeBatchDTO

from .. import AssetPosition
from .trades import Trade

logger = logging.getLogger("pms")

SelfTradeProposal = TypeVar("SelfTradeProposal", bound="TradeProposal")


class TradeProposal(RiskCheckMixin, WBModel):
    trade_date = models.DateField(verbose_name="Trading Date")

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMIT = "SUBMIT", "Submit"
        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"
        FAILED = "FAILED", "Failed"

    comment = models.TextField(default="", verbose_name="Trade Comment", blank=True)
    status = FSMField(default=Status.DRAFT, choices=Status.choices, verbose_name="Status")
    rebalancing_model = models.ForeignKey(
        "wbportfolio.RebalancingModel",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="trade_proposals",
        verbose_name="Rebalancing Model",
        help_text="Rebalancing Model that generates the target portfolio",
    )
    portfolio = models.ForeignKey(
        "wbportfolio.Portfolio", related_name="trade_proposals", on_delete=models.PROTECT, verbose_name="Portfolio"
    )
    creator = models.ForeignKey(
        "directory.Person",
        blank=True,
        null=True,
        related_name="trade_proposals",
        on_delete=models.PROTECT,
        verbose_name="Owner",
    )

    class Meta:
        verbose_name = "Trade Proposal"
        verbose_name_plural = "Trade Proposals"
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "trade_date"],
                name="unique_trade_proposal",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.trade_date and self.portfolio.assets.exists():
            self.trade_date = (self.portfolio.assets.latest("date").date + BDay(1)).date()
        if not self.rebalancing_model and (rebalancer := getattr(self.portfolio, "automatic_rebalancer", None)):
            self.rebalancing_model = rebalancer.rebalancing_model
        super().save(*args, **kwargs)

    def _get_checked_object_field_name(self) -> str:
        """
        Mandatory function from the Riskcheck mixin that returns the field (aka portfolio), representing the object to check the rules against.
        """
        return "portfolio"

    @cached_property
    def validated_trading_service(self) -> TradingService:
        """
        This property holds the validated trading services and cache it.This property expect to be set only if is_valid return True
        """
        return TradingService(
            self.trade_date,
            effective_portfolio=self.portfolio._build_dto(self.trade_date),
            trades_batch=self._build_dto(),
        )

    @cached_property
    def last_effective_date(self) -> date:
        try:
            return self.portfolio.assets.filter(date__lt=self.trade_date).latest("date").date
        except AssetPosition.DoesNotExist:
            return (self.trade_date - BDay(1)).date()

    @property
    def previous_trade_proposal(self) -> SelfTradeProposal | None:
        future_proposals = TradeProposal.objects.filter(portfolio=self.portfolio).filter(
            trade_date__lt=self.trade_date, status=TradeProposal.Status.APPROVED
        )
        if future_proposals.exists():
            return future_proposals.latest("trade_date")
        return None

    @property
    def next_trade_proposal(self) -> SelfTradeProposal | None:
        future_proposals = TradeProposal.objects.filter(portfolio=self.portfolio).filter(
            trade_date__gt=self.trade_date, status=TradeProposal.Status.APPROVED
        )
        if future_proposals.exists():
            return future_proposals.earliest("trade_date")
        return None

    @property
    def base_assets(self) -> dict[int, Decimal]:
        """
        Return a dictionary representation (instrument_id: target weight) of this trade proposal
        Returns:
            A dictionary representation

        """
        return {
            v["underlying_instrument"]: v["target_weight"]
            for v in self.trades.all()
            .annotate_base_info()
            .filter(status=Trade.Status.EXECUTED)
            .values("underlying_instrument", "target_weight")
        }

    def __str__(self) -> str:
        return f"{self.portfolio.name}: {self.trade_date} ({self.status})"

    def _build_dto(self) -> TradeBatchDTO:
        """
        Data Transfer Object
        Returns:
            DTO trade object
        """
        return (
            TradeBatchDTO(tuple([trade._build_dto() for trade in self.trades.all()])) if self.trades.exists() else None
        )

    # Start tools methods
    def clone(self, **kwargs) -> SelfTradeProposal:
        """
        Method to clone self as a new trade proposal. It will automatically shift the trade date if a proposal already exists
        Args:
            **kwargs: The keyword arguments
        Returns:
            The cloned trade proposal
        """
        trade_date = kwargs.get("trade_date", self.trade_date)

        # Find the next valid trade date
        while TradeProposal.objects.filter(portfolio=self.portfolio, trade_date=trade_date).exists():
            trade_date += timedelta(days=1)

        trade_proposal_clone = TradeProposal.objects.create(
            trade_date=trade_date,
            comment=kwargs.get("comment", self.comment),
            status=TradeProposal.Status.DRAFT,
            rebalancing_model=self.rebalancing_model,
            portfolio=self.portfolio,
            creator=self.creator,
        )
        return trade_proposal_clone

    def normalize_trades(self):
        """
        Call the trading service with the existing trades and normalize them in order to obtain a total sum target weight of 100%
        The existing trade will be modified directly with the given normalization factor
        """
        service = TradingService(self.trade_date, trades_batch=self._build_dto())
        service.normalize()
        leftovers_trades = self.trades.all()
        total_target_weight = Decimal("0.0")
        for underlying_instrument_id, trade_dto in service.trades_batch.trades_map.items():
            with suppress(Trade.DoesNotExist):
                trade = self.trades.get(underlying_instrument_id=underlying_instrument_id)
                trade.weighting = round(trade_dto.delta_weight, 6)
                trade.shares = self.estimate_shares(trade)
                trade.save()
                total_target_weight += trade._target_weight
                leftovers_trades = leftovers_trades.exclude(id=trade.id)
        leftovers_trades.delete()
        # we handle quantization error due to the decimal max digits. In that case, we take the biggest trade (highest weight) and we remove the quantization error
        if quantize_error := (total_target_weight - Decimal("1.0")):
            biggest_trade = self.trades.latest("weighting")
            biggest_trade.weighting -= quantize_error
            biggest_trade.save()

    def _get_target_portfolio(self, **kwargs) -> PortfolioDTO:
        if self.rebalancing_model:
            params = {}
            if rebalancer := getattr(self.portfolio, "automatic_rebalancer", None):
                params.update(rebalancer.parameters)
            params.update(kwargs)
            return self.rebalancing_model.get_target_portfolio(
                self.portfolio, self.trade_date, self.last_effective_date, **params
            )
        # Return the current portfolio by default
        return self.portfolio._build_dto(self.last_effective_date)

    def reset_trades(self, target_portfolio: PortfolioDTO | None = None):
        """
        Will delete all existing trades and recreate them from the method `create_or_update_trades`
        """
        if self.status != TradeProposal.Status.DRAFT:
            raise ValueError("Cannot reset non-draft trade proposal. Revert this trade proposal first.")
        # delete all existing trades
        self.trades.all().delete()
        last_effective_date = self.last_effective_date
        # Get effective and target portfolio
        effective_portfolio = self.portfolio._build_dto(last_effective_date)
        if not target_portfolio:
            target_portfolio = self._get_target_portfolio()
        # if not effective_portfolio:
        #     effective_portfolio = target_portfolio
        service = TradingService(
            self.trade_date,
            effective_portfolio=effective_portfolio,
            target_portfolio=target_portfolio,
        )
        service.normalize()
        service.is_valid()

        for trade_dto in service.validated_trades:
            instrument = Instrument.objects.get(id=trade_dto.underlying_instrument)
            currency_fx_rate = instrument.currency.convert(
                last_effective_date, self.portfolio.currency, exact_lookup=True
            )
            trade = Trade(
                underlying_instrument=instrument,
                transaction_subtype=Trade.Type.BUY if trade_dto.delta_weight > 0 else Trade.Type.SELL,
                currency=instrument.currency,
                value_date=last_effective_date,
                transaction_date=self.trade_date,
                trade_proposal=self,
                portfolio=self.portfolio,
                weighting=trade_dto.delta_weight,
                status=Trade.Status.DRAFT,
                currency_fx_rate=currency_fx_rate,
            )
            trade.shares = self.estimate_shares(trade)
            trade.save()

    def replay(self):
        last_trade_proposal = self
        while last_trade_proposal and last_trade_proposal.status == TradeProposal.Status.APPROVED:
            logger.info(f"Replaying trade proposal {last_trade_proposal}")
            last_trade_proposal.portfolio.assets.filter(
                date=last_trade_proposal.trade_date
            ).delete()  # we delete the existing position and we reapply the trade proposal
            if not last_trade_proposal.portfolio.assets.filter(date=last_trade_proposal.trade_date).exists():
                if last_trade_proposal.status == TradeProposal.Status.APPROVED:
                    logger.info("Reverting trade proposal ...")
                    last_trade_proposal.revert()
                if last_trade_proposal.status == TradeProposal.Status.DRAFT:
                    logger.info("Submitting trade proposal ...")
                    last_trade_proposal.submit()
                if last_trade_proposal.status == TradeProposal.Status.SUBMIT:
                    logger.info("Approving trade proposal ...")
                    last_trade_proposal.approve()
                last_trade_proposal.save()
            next_trade_proposal = last_trade_proposal.next_trade_proposal
            next_trade_date = (
                next_trade_proposal.trade_date - timedelta(days=1) if next_trade_proposal else date.today()
            )
            overriding_trade_proposal = last_trade_proposal.portfolio.batch_portfolio(
                last_trade_proposal.trade_date, next_trade_date
            )
            last_trade_proposal = overriding_trade_proposal or next_trade_proposal

    def estimate_shares(self, trade: Trade) -> Decimal | None:
        if not self.portfolio.only_weighting and (quote := trade.underlying_quote_price):
            trade_total_value_fx_portfolio = (
                self.portfolio.get_total_asset_value(trade.value_date) * trade._target_weight
            )
            price_fx_portfolio = quote.net_value * trade.currency_fx_rate
            if price_fx_portfolio:
                return trade_total_value_fx_portfolio / price_fx_portfolio

    # Start FSM logics

    @transition(
        field=status,
        source=Status.DRAFT,
        target=Status.SUBMIT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.SEND.icon,
                key="submit",
                label="Submit",
                action_label="Submit",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def submit(self, by=None, description=None, **kwargs):
        self.trades.update(comment="", status=Trade.Status.DRAFT)
        for trade in self.trades.all():
            trade.submit()
            trade.save()
        self.evaluate_active_rules(
            self.trade_date, self.validated_trading_service.target_portfolio, asynchronously=True
        )

    def can_submit(self):
        errors = dict()
        errors_list = []
        if self.trades.exists() and self.trades.exclude(status=Trade.Status.DRAFT).exists():
            errors_list.append("All trades need to be draft before submitting")
        service = self.validated_trading_service
        try:
            service.is_valid(ignore_error=True)
            # if service.trades_batch.totat_abs_delta_weight == 0:
            #     errors_list.append(
            #         "There is no change detected in this trade proposal. Please submit at last one valid trade"
            #     )
            if len(service.validated_trades) == 0:
                errors_list.append("There is no valid trade on this proposal")
            if service.errors:
                errors_list.extend(service.errors)
            if errors_list:
                errors["non_field_errors"] = errors_list
        except ValidationError:
            errors["non_field_errors"] = service.errors
            with suppress(KeyError):
                del self.__dict__["validated_trading_service"]
        return errors

    @property
    def can_be_approved_or_denied(self):
        return self.has_no_rule_or_all_checked_succeed and self.portfolio.is_manageable

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.APPROVED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.can_be_approved_or_denied,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.APPROVE.icon,
                key="approve",
                label="Approve",
                action_label="Approve",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def approve(self, by=None, description=None, synchronous=False, **kwargs):
        # We validate trade which will create or update the initial asset positions
        if not self.portfolio.can_be_rebalanced:
            raise ValueError("Non-Rebalanceable portfolio cannot be traded manually.")
        self.trades.update(status=Trade.Status.SUBMIT)
        self.portfolio.assets.filter(date=self.trade_date).delete()  # we delete position to avoid having leftovers
        for trade in self.trades.all():
            trade.execute()
            trade.save()
        self.portfolio.change_at_date(self.trade_date)
        # replay_as_task.delay(self.id)

    def can_approve(self):
        errors = dict()
        if not self.portfolio.can_be_rebalanced:
            errors["non_field_errors"] = "The portfolio does not allow manual rebalanced"
        if self.trades.exclude(status=Trade.Status.SUBMIT).exists():
            errors["non_field_errors"] = "At least one trade needs to be submitted to be able to approve this proposal"
        if not self.portfolio.can_be_rebalanced:
            errors["portfolio"] = (
                "The portfolio needs to be a model portfolio in order to approve this trade proposal manually"
            )
        if self.has_assigned_active_rules and not self.has_all_check_completed_and_succeed:
            errors["non_field_errors"] = "The pre trades rules did not passed successfully"
        return errors

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DENIED,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.can_be_approved_or_denied,
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.DENY.icon,
                key="deny",
                label="Deny",
                action_label="Deny",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def deny(self, by=None, description=None, **kwargs):
        self.trades.all().delete()
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]

    def can_deny(self):
        errors = dict()
        if self.trades.exclude(status=Trade.Status.SUBMIT).exists():
            errors["non_field_errors"] = "At least one trade needs to be submitted to be able to deny this proposal"
        return errors

    @transition(
        field=status,
        source=Status.SUBMIT,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        )
        and instance.has_all_check_completed,  # we wait for all checks to succeed before proposing the back to draft transition
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.UNDO.icon,
                key="backtodraft",
                label="Back to Draft",
                action_label="backtodraft",
                # description_fields="<p>Start: {{start}}</p><p>End: {{end}}</p><p>Title: {{title}}</p>",
            )
        },
    )
    def backtodraft(self, **kwargs):
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]
        self.trades.update(status=Trade.Status.DRAFT)
        self.checks.delete()

    def can_backtodraft(self):
        pass

    @transition(
        field=status,
        source=Status.APPROVED,
        target=Status.DRAFT,
        permission=lambda instance, user: PortfolioRole.is_portfolio_manager(
            user.profile, portfolio=instance.portfolio
        ),
        custom={
            "_transition_button": ActionButton(
                method=RequestType.PATCH,
                identifiers=("wbportfolio:tradeproposal",),
                icon=WBIcon.REGENERATE.icon,
                key="revert",
                label="Revert",
                action_label="revert",
                description_fields="<p>Unapply trades and move everything back to draft (i.e. The underlying asset positions will change like the trades were never applied)</p>",
            )
        },
    )
    def revert(self, **kwargs):
        with suppress(KeyError):
            del self.__dict__["validated_trading_service"]
        for trade in self.trades.filter(status=Trade.Status.EXECUTED):
            trade.revert()
            trade.save()
        # replay_as_task.delay(self.id)

    def can_revert(self):
        errors = dict()
        if not self.portfolio.can_be_rebalanced:
            errors["portfolio"] = (
                "The portfolio needs to be a model portfolio in order to revert this trade proposal manually"
            )
        return errors

    # End FSM logics

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbportfolio:tradeproposal"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbportfolio:tradeproposalrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{_portfolio.name}} ({{trade_date}})"


@shared_task(queue="portfolio")
def replay_as_task(trade_proposal_id):
    trade_proposal = TradeProposal.objects.get(id=trade_proposal_id)
    trade_proposal.replay()
