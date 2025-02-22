from testing_utils.testing_utils import _round_df_float_columns
from copy import deepcopy


class TestRoundDfFloatColumns:
    def test_round_df_float_columns(
        self,
        rest_queried_dataframe,
    ):
        num_feat = list(rest_queried_dataframe.columns)[1]

        precision = 3

        rest_queried_dataframe[num_feat] = round(
            rest_queried_dataframe[num_feat],
            precision,
        )

        assert _round_df_float_columns(
            df=rest_queried_dataframe,
            precision=3,
        ).equals(rest_queried_dataframe)

    def test_round_df_float_columns_no_float_columns(
        self,
        rest_queried_dataframe,
    ):
        # NOTE: using a df fixture that only has date- and integer-typed columns;
        #       should be returned unchanged by the helper
        df_copy = deepcopy(rest_queried_dataframe)
        assert _round_df_float_columns(
            df_copy,
        ).equals(rest_queried_dataframe)
