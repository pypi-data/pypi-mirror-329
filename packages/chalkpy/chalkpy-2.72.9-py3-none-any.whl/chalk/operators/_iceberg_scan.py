from __future__ import annotations

from typing_extensions import final

from chalk import StaticOperator
from chalk.integrations.catalogs.base_catalog import BaseCatalog


@final
class IcebergScanOperator(StaticOperator):
    _chalk__operator_name = StaticOperator._chalk__operator_prefix + "iceberg_scan"

    def __init__(self, target: str | None, catalog: BaseCatalog, column_names: tuple[str, ...]) -> None:
        super().__init__(target=target, catalog=catalog, column_names=column_names, parent=None)
        self._target = target
        self._catalog = catalog
        self.column_names = column_names
