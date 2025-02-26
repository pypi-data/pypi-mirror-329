from altrustworthyai.glassbox import LogisticRegression
from six import raise_from

from .tutils import assert_valid_explanation, synthetic_classification


def test_import_demo_extension_classes():
    try:
        from altrustworthyai.ext.blackbox import ExampleBlackboxExplainer  # noqa
        from altrustworthyai.ext.greybox import ExampleGreyboxExplainer  # noqa
        from altrustworthyai.ext.glassbox import ExampleGlassboxExplainer  # noqa
        from altrustworthyai.ext.data import ExampleDataExplainer  # noqa
        from altrustworthyai.ext.perf import ExamplePerfExplainer  # noqa
        from altrustworthyai.ext.provider import ExampleVisualizeProvider  # noqa
    except ImportError as import_error:
        raise_from(
            Exception(
                "Failure in demo while trying "
                "to load example explainers through extension_utils",
                import_error,
            ),
            None,
        )


def test_demo_blackbox_explainer():
    from altrustworthyai.ext.blackbox import ExampleBlackboxExplainer
    from altrustworthyai.ext.data import ExampleDataExplainer
    from altrustworthyai.ext.glassbox import ExampleGlassboxExplainer
    from altrustworthyai.ext.greybox import ExampleGreyboxExplainer
    from altrustworthyai.ext.perf import ExamplePerfExplainer

    data = synthetic_classification()
    blackbox = LogisticRegression()
    blackbox.fit(data["train"]["X"], data["train"]["y"])
    predict_fn = lambda x: blackbox.predict_proba(x)  # noqa: E731

    explainer = ExampleBlackboxExplainer(predict_fn, data["train"]["X"])
    explanation = explainer.explain_local(
        data["test"]["X"].head(), data["test"]["y"].head()
    )
    assert_valid_explanation(explanation)

    explainer = ExampleGreyboxExplainer(blackbox, data["train"]["X"])
    explanation = explainer.explain_local(
        data["test"]["X"].head(), data["test"]["y"].head()
    )
    assert_valid_explanation(explanation)

    explainer = ExampleGlassboxExplainer()
    explainer.fit(data["train"]["X"], data["train"]["y"])
    explainer.predict(data["test"]["X"].head())
    explanation = explainer.explain_local(
        data["test"]["X"].head(), data["test"]["y"].head()
    )
    assert_valid_explanation(explanation)

    explainer = ExampleDataExplainer()
    explanation = explainer.explain_data(
        data["test"]["X"].head(), data["test"]["y"].head()
    )
    assert_valid_explanation(explanation)

    explainer = ExamplePerfExplainer(predict_fn)
    explanation = explainer.explain_perf(
        data["test"]["X"].head(), data["test"]["y"].head()
    )
    assert_valid_explanation(explanation)
