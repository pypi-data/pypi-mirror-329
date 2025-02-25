import pytest


@pytest.mark.skip(reason="TODO")
def test_perfect_r2():
    pass


# @pytest.mark.skip(reason="TODO")
# def test_bad_r2():
#     n_samples = 400
#     n_targets = len(config.data.output_keys)
#     np.zeros((n_samples, config.data.n_dimensions, n_targets))
#     np.ones((n_samples, config.data.n_dimensions, n_targets))
#     scores = r2_from_arrays(y_pred, y_true)
#
#     arr = (
#         scores.melt(
#             id_vars=["region", "year"],
#             value_vars=config.data.output_keys,
#             variable_name="target",
#             value_name="r2",
#         )
#         .with_row_index()
#         .get_column("r2")
#         .to_numpy()
#     )
#     assert np.all(arr == 0.0), "r2 score should have been zero"
#     i = 5
#     target = sorted(config.data.output_keys)[i]
#     y_pred[:, :, i] = 1.0
#     scores = r2_from_arrays(y_pred, y_true)
#     perfect = scores.select(target)[:, 0].to_numpy()
#     assert np.all(perfect == 1.0), f"r2 of {target} should have been 1.0"
