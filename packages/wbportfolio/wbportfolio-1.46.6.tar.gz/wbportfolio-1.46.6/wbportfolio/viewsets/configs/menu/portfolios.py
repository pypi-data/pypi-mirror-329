from wbcore.menus import ItemPermission, MenuItem

from wbportfolio.permissions import is_portfolio_manager

PortfolioMenuItem = MenuItem(
    label="Portfolios",
    endpoint="wbportfolio:portfolio-list",
    permission=ItemPermission(method=is_portfolio_manager, permissions=["wbportfolio.view_portfolio"]),
)


ModelPortfolioMenuItem = MenuItem(
    label="Managed Portfolios",
    endpoint="wbportfolio:portfolio-list",
    endpoint_get_parameters={"is_manageable": True},
    permission=ItemPermission(method=is_portfolio_manager, permissions=["wbportfolio.view_portfolio"]),
)
