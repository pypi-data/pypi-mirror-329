import os
from multiprocessing import Process
from pathlib import Path

import streamlit as st

from biofefi.components.experiments import experiment_selector, model_selector
from biofefi.components.forms import fi_options_form
from biofefi.components.images.logos import sidebar_logo
from biofefi.components.logs import log_box
from biofefi.components.plots import plot_box
from biofefi.feature_importance import feature_importance, fuzzy_interpretation
from biofefi.machine_learning.data import DataBuilder
from biofefi.options.enums import (
    ExecutionStateKeys,
    FeatureImportanceStateKeys,
    FuzzyStateKeys,
    ViewExperimentKeys,
)
from biofefi.options.execution import ExecutionOptions
from biofefi.options.fi import FeatureImportanceOptions
from biofefi.options.file_paths import (
    biofefi_experiments_base_dir,
    execution_options_path,
    fi_options_path,
    fi_plot_dir,
    fuzzy_options_path,
    fuzzy_plot_dir,
    log_dir,
    ml_model_dir,
    plot_options_path,
)
from biofefi.options.fuzzy import FuzzyOptions
from biofefi.options.plotting import PlottingOptions
from biofefi.services.configuration import (
    load_execution_options,
    load_plot_options,
    save_options,
)
from biofefi.services.experiments import (
    delete_previous_fi_results,
    find_previous_fi_results,
    get_experiments,
)
from biofefi.services.logs import get_logs
from biofefi.services.ml_models import load_models_to_explain
from biofefi.utils.logging_utils import Logger, close_logger
from biofefi.utils.utils import cancel_pipeline, set_seed


def build_configuration() -> (
    tuple[FuzzyOptions | None, FeatureImportanceOptions, ExecutionOptions, str, list]
):
    """Build the configuration objects for the pipeline.

    Returns:
        tuple[
            FuzzyOptions | None,
            FeatureImportanceOptions,
            ExecutionOptions,
            str,
            list
        ]: The configuration for fuzzy, FI and ML pipelines, the experiment name
        and the list of models to explain.
    """
    biofefi_base_dir = biofefi_experiments_base_dir()
    experiment_name = st.session_state[ExecutionStateKeys.ExperimentName]

    # Load plotting options
    path_to_plot_opts = plot_options_path(biofefi_base_dir / experiment_name)
    plotting_options = load_plot_options(path_to_plot_opts)

    # Load executuon options
    path_to_exec_opts = execution_options_path(biofefi_base_dir / experiment_name)
    exec_opt = load_execution_options(path_to_exec_opts)

    # Set up fuzzy options
    fuzzy_opt = None
    if st.session_state.get(FuzzyStateKeys.FuzzyFeatureSelection, False):
        fuzzy_opt = FuzzyOptions(
            fuzzy_feature_selection=st.session_state[
                FuzzyStateKeys.FuzzyFeatureSelection
            ],
            number_fuzzy_features=st.session_state[
                FuzzyStateKeys.NumberOfFuzzyFeatures
            ],
            granular_features=st.session_state[FuzzyStateKeys.GranularFeatures],
            number_clusters=st.session_state[FuzzyStateKeys.NumberOfClusters],
            cluster_names=st.session_state.get(FuzzyStateKeys.ClusterNames, "").split(
                ", "
            ),
            number_rules=st.session_state[FuzzyStateKeys.NumberOfTopRules],
            save_fuzzy_set_plots=plotting_options.save_plots,
            fuzzy_log_dir=str(
                log_dir(
                    biofefi_base_dir
                    / st.session_state[ViewExperimentKeys.ExperimentName]
                )
                / "fuzzy"
            ),
        )

    # Set up feature importance options
    fi_opt = FeatureImportanceOptions(
        num_features_to_plot=st.session_state[
            FeatureImportanceStateKeys.NumberOfImportantFeatures
        ],
        permutation_importance_scoring=st.session_state[
            FeatureImportanceStateKeys.ScoringFunction
        ],
        permutation_importance_repeat=st.session_state[
            FeatureImportanceStateKeys.NumberOfRepetitions
        ],
        shap_reduce_data=st.session_state[
            FeatureImportanceStateKeys.ShapDataPercentage
        ],
        save_feature_importance_plots=plotting_options.save_plots,
        fi_log_dir=str(
            log_dir(
                biofefi_base_dir / st.session_state[ViewExperimentKeys.ExperimentName]
            )
            / "fi"
        ),
        save_feature_importance_options=st.session_state[
            FeatureImportanceStateKeys.SaveFeatureImportanceOptions
        ],
        save_feature_importance_results=st.session_state[
            FeatureImportanceStateKeys.SaveFeatureImportanceResults
        ],
        local_importance_methods=st.session_state[
            FeatureImportanceStateKeys.LocalImportanceFeatures
        ],
        feature_importance_ensemble=st.session_state[
            FeatureImportanceStateKeys.EnsembleMethods
        ],
        global_importance_methods=st.session_state[
            FeatureImportanceStateKeys.GlobalFeatureImportanceMethods
        ],
    )

    return (
        fuzzy_opt,
        fi_opt,
        exec_opt,
        plotting_options,
        experiment_name,
        st.session_state[FeatureImportanceStateKeys.ExplainModels],
    )


def pipeline(
    fuzzy_opts: FuzzyOptions,
    fi_opts: FeatureImportanceOptions,
    exec_opts: ExecutionOptions,
    plot_opts: PlottingOptions,
    experiment_name: str,
    explain_models: list,
):
    """This function actually performs the steps of the pipeline. It can be wrapped
    in a process it doesn't block the UI.

    Args:
        fuzzy_opts (FuzzyOptions): Options for fuzzy feature importance.
        fi_opts (FeatureImportanceOptions): Options for feature importance.
        exec_opts (ExecutionOptions): Options for pipeline execution.
        plot_opts (PlottingOptions): Options for plotting.
        experiment_name (str): The experiment name.
        explain_models (list): The models to analyse.
    """
    biofefi_base_dir = biofefi_experiments_base_dir()
    seed = exec_opts.random_state
    set_seed(seed)
    fi_logger_instance = Logger(Path(fi_opts.fi_log_dir))
    fi_logger = fi_logger_instance.make_logger()

    data = DataBuilder(
        data_path=exec_opts.data_path,
        random_state=exec_opts.random_state,
        normalization=exec_opts.normalization,
        n_bootstraps=exec_opts.n_bootstraps,
        logger=fi_logger,
        data_split=exec_opts.data_split,
        problem_type=exec_opts.problem_type,
    ).ingest()

    # Models will already be trained before feature importance
    trained_models = load_models_to_explain(
        ml_model_dir(biofefi_base_dir / experiment_name), explain_models
    )

    # Feature importance
    (
        gloabl_importance_results,
        local_importance_results,
        ensemble_results,
    ) = feature_importance.run(
        fi_opt=fi_opts,
        exec_opt=exec_opts,
        plot_opt=plot_opts,
        data=data,
        models=trained_models,
        logger=fi_logger,
    )

    # Fuzzy interpretation
    if fuzzy_opts is not None and fuzzy_opts.fuzzy_feature_selection:
        fuzzy_logger_instance = Logger(Path(fuzzy_opts.fuzzy_log_dir))
        fuzzy_logger = fuzzy_logger_instance.make_logger()
        fuzzy_interpretation.run(
            fuzzy_opt=fuzzy_opts,
            fi_opt=fi_opts,
            exec_opt=exec_opts,
            plot_opt=plot_opts,
            data=data,
            models=trained_models,
            ensemble_results=ensemble_results,
            logger=fuzzy_logger,
        )
        close_logger(fuzzy_logger_instance, fuzzy_logger)

    # Close the fi logger
    close_logger(fi_logger_instance, fi_logger)


# Set page contents
st.set_page_config(
    page_title="Feature Importance",
    page_icon=sidebar_logo(),
)


st.header("Feature Importance")
st.write(
    """
    This page provides options for exploring and customising feature importance and
    interpretability methods in the trained machine learning models.
    You can configure global and local feature importance techniques,
    select ensemble approaches, and apply fuzzy feature selection.
    Options include tuning scoring functions, setting data percentages
    for SHAP analysis, and configuring rules for fuzzy synergy analysis
    to gain deeper insights into model behaviour.
    """
)


choices = get_experiments()
experiment_name = experiment_selector(choices)
base_dir = biofefi_experiments_base_dir()


if experiment_name:

    previous_results_exist = find_previous_fi_results(
        biofefi_experiments_base_dir() / experiment_name
    )

    if previous_results_exist:
        st.warning("You have run feature importance in this experiment previously.")
        st.checkbox(
            "Would you like to rerun feature importance? This will overwrite the existing results.",
            value=True,
            key=FuzzyStateKeys.RerunFI,
        )
    else:
        st.session_state[FuzzyStateKeys.RerunFI] = True

    if st.session_state[FuzzyStateKeys.RerunFI]:

        st.session_state[ExecutionStateKeys.ExperimentName] = experiment_name

        model_choices = os.listdir(ml_model_dir(base_dir / experiment_name))
        model_choices = [x for x in model_choices if x.endswith(".pkl")]

        explain_all_models = st.toggle(
            "Explain all models", key=FeatureImportanceStateKeys.ExplainAllModels
        )

        if explain_all_models:
            st.session_state[FeatureImportanceStateKeys.ExplainModels] = model_choices
        else:
            model_selector(model_choices)

        if model_choices := st.session_state.get(
            FeatureImportanceStateKeys.ExplainModels
        ):
            fi_options_form()

            if st.button("Run Feature Importance", type="primary"):
                delete_previous_fi_results(base_dir / experiment_name)
                config = build_configuration()
                # save FI options
                fi_options_file = fi_options_path(base_dir / experiment_name)
                save_options(fi_options_file, config[1])
                # save Fuzzy options if configured
                if config[0] is not None:
                    fuzzy_options_file = fuzzy_options_path(base_dir / experiment_name)
                    save_options(fuzzy_options_file, config[0])

                process = Process(target=pipeline, args=config, daemon=True)
                process.start()
                cancel_button = st.button(
                    "Cancel", on_click=cancel_pipeline, args=(process,)
                )
                with st.spinner(
                    "Feature Importance pipeline is running in the background. "
                    "Check the logs for progress."
                ):
                    # wait for the process to finish or be cancelled
                    process.join()
                try:
                    st.session_state[FeatureImportanceStateKeys.FILogBox] = get_logs(
                        log_dir(base_dir / experiment_name) / "fi"
                    )
                    st.session_state[FuzzyStateKeys.FuzzyLogBox] = get_logs(
                        log_dir(base_dir / experiment_name) / "fuzzy"
                    )
                    log_box(
                        box_title="Feature Importance Logs",
                        key=FeatureImportanceStateKeys.FILogBox,
                    )
                    log_box(box_title="Fuzzy FI Logs", key=FuzzyStateKeys.FuzzyLogBox)
                except NotADirectoryError:
                    pass
                fi_plots = fi_plot_dir(base_dir / experiment_name)
                if fi_plots.exists():
                    plot_box(fi_plots, "Feature importance plots")
                fuzzy_plots = fuzzy_plot_dir(base_dir / experiment_name)
                if fuzzy_plots.exists():
                    plot_box(fuzzy_plots, "Fuzzy plots")

    else:
        st.success(
            "You have chosen not to rerun the feature importance experiments. "
            "You can proceed to see the experiment results."
        )
