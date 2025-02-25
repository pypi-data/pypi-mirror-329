import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd
import pint_pandas
from radioactivedecay import Nuclide, Inventory, InventoryHP
from scipy.constants import N_A
from typing import Optional, Union


ACCESSOR_NAME: str = "nucs"

logger = logging.getLogger(__name__)


@dataclass
class NuclideConfig:
    """Configuration of nuclides module."""

    col_nuc: str = "nuclide"
    col_elem: str = "element"
    col_z: str = "Z"
    col_a: str = "A"
    col_a_mass: str = "atomic_mass"
    col_half_life: str = "half_life"
    col_spec_act: str = "specific_activity"


@pd.api.extensions.register_series_accessor(ACCESSOR_NAME)
class NuclideSeriesAccessor:
    """Custom nuclide series accessor.

    Series must contain nuclide strings, e.g.:
    pd.Series(['U-233', 'U-234', 'U-235', 'U-236', 'U-238'])

    Acts as kind of wrapper for radioactivedecay.Nuclide objects.
    For further information check its documentation:
    https://radioactivedecay.github.io/nuclide.html?highlight=nuclide#id1
    """

    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj
        self._nucs = self._obj.apply(Nuclide)
        self._cfg = NuclideConfig()

    @staticmethod
    def _validate(obj):
        """Verify that strings are interpretated as nuclides."""

        def is_valid_nuclide(nuclide: str) -> bool:
            try:
                Nuclide(nuclide)
                return True
            except Exception:
                return False

        invalid = obj[~obj.apply(lambda x: isinstance(x, str) and is_valid_nuclide(x))]
        if len(invalid) == len(obj):
            raise AttributeError("Series does not contain nuclide strings.")
        elif not invalid.empty:
            raise ValueError(
                f"Series contains invalid nuclides strings: {', '.join(invalid.tolist())}"
            )

    def __repr__(self) -> str:
        return f"NuclideSeriesAccessor, {self.decay_data}"

    @property
    def decay_data(self) -> str:
        """Returns radioactive decay dataset description."""
        return self._nucs[0].decay_data

    @property
    def Z(self) -> pd.Series:
        """Returns series with Z."""
        s = self._nucs.apply(lambda x: x.Z)
        s.name = self._cfg.col_z
        return s

    @property
    def A(self) -> pd.Series:
        """Returns series with A."""
        s = self._nucs.apply(lambda x: x.A)
        s.name = self._cfg.col_a
        return s

    @property
    def element(self) -> pd.Series:
        """Returns categorical series with element symbols, ordered by Z."""
        s = self._nucs.apply(lambda x: x.nuclide.split("-")[0])
        s.name = self._cfg.col_elem
        ordered_elems = (
            self.categorical.dtype.categories.to_series()
            .apply(lambda x: x.split("-")[0])
            .unique()
        )
        cat = pd.Categorical(s, categories=ordered_elems, ordered=True)
        return pd.Series(cat, name=s.name, index=self._obj.index)

    @property
    def categorical(self) -> pd.Series:
        """Returns series with categorical datatype, ordered by Z and A."""
        clean_nucs = self._nucs.apply(lambda x: x.nuclide)
        df = pd.DataFrame([self.Z, self.A]).T.set_index(clean_nucs)
        ordered_nucs = df.sort_values([self._cfg.col_z, self._cfg.col_a]).index.unique()
        cat = pd.Categorical(clean_nucs, categories=ordered_nucs, ordered=True)
        return pd.Series(cat, name=self._cfg.col_nuc, index=self._obj.index)

    @property
    def atomic_mass(self) -> pd.Series:
        """Returns series with atomic masses in g/mol."""
        values = self._nucs.apply(lambda x: x.atomic_mass)
        return pd.Series(values, dtype="pint[g/mol]", name=self._cfg.col_a_mass)

    @property
    def half_life(self) -> pd.Series:
        """Returns series with half life in defined unit."""
        unit = "s"
        values = self._nucs.apply(lambda x: x.half_life(units=unit))
        return pd.Series(values, dtype=f"pint[{unit}]", name=self._cfg.col_half_life)

    @property
    def specific_activity(self) -> pd.Series:
        """Returns series with specific activities in 'Bq/g'.

        Uses Avogadro constant (`N_A`) from `SciPy`:
        https://docs.scipy.org/doc/scipy/reference/constants.html#physical-constants
        """
        n_a = pd.Series([N_A], dtype="pint[1/mol]")[0]
        specific_activity = np.log(2) / self.half_life * n_a / self.atomic_mass
        specific_activity.name = self._cfg.col_spec_act
        return specific_activity.pint.to("Bq/g")

    @property
    def properties(self) -> pd.DataFrame:
        """Returns DataFrame contain nuclide property Series."""
        props = [
            self.element,
            self.categorical,
            self.Z,
            self.A,
            self.atomic_mass,
            self.half_life,
            self.specific_activity,
        ]
        return pd.concat(props, axis=1)


def inventory_from_df(
    df: pd.DataFrame,
    col_nuc: str = NuclideConfig().col_nuc,
    col_mass: str = "mass",
    HP: bool = True,
) -> Union[Inventory, InventoryHP]:
    """Create a radioactiveday Inventory object from a DataFrame.

    col_nuc: str (default: from cfg), nuclide column name
    col_mass: str (default: 'mass'), mass column name
    HP: bool (default: True), returns rd.InventoryHP object if True,
        otherwise an ordinary rd.Inventory object is returned
    """
    mass_unit = f"{df[col_mass].pint.units:~P}"
    mass_dct = df.set_index(col_nuc)[col_mass].pint.to(mass_unit).pint.m.to_dict()
    if HP:
        return InventoryHP(mass_dct, units=mass_unit)
    return Inventory(mass_dct, units=mass_unit)


def remove_incompatible_nuclides_from_pd_obj(
    obj: pd.DataFrame | pd.Series, col_nuc: Optional[str] = None
) -> Union[pd.DataFrame, pd.Series]:
    """Strip incompatible nuclides from a Pandas DataFrame or Series.

    Incompatible nuclides are nuclides that raise a ``ValueError`` during initialisation
    as ``radioactivedecay.Nuclide`` object. If a DataFrame is provided, ``col_nuc``
    must correspond to the column name of the column containing the nuclide strings.
    If a Series is provided, it is assumed that it contains only nuclide strings.
    """
    if isinstance(obj, pd.Series):
        nuclide_series = obj
    elif isinstance(obj, pd.DataFrame):
        if col_nuc is None:
            raise ValueError("No nuclide column name ('col_nuc') provided.")
        elif col_nuc not in obj.columns:
            raise ValueError(
                f"Column '{col_nuc}' does not exist in the provided DataFrame."
            )
        nuclide_series = obj[col_nuc]
    else:
        raise AttributeError(
            f"Invalid object, removal of incompatible nuclides requires pandas Series or DataFrame object, not {type(obj)!r}."
        )

    try:
        nuclide_series.nucs.categorical
        return obj
    except ValueError as e:
        error_message = str(e)
        if "Series contains invalid nuclides strings" in error_message:
            # Extract the list of invalid nuclides from the error message
            invalid_nuclides_str = error_message.split(": ")[1]
            invalid_nuclides_lst = invalid_nuclides_str.split(", ")
            logger.warning(f"Removing incompatible nuclides: {invalid_nuclides_str}")

            valid_mask = ~nuclide_series.isin(invalid_nuclides_lst)
            return obj[valid_mask]
        else:
            # Re-raise the exception if it's not the expected one
            raise
