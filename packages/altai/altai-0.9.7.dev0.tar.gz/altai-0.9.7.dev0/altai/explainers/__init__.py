"""
The 'altai.explainers' module includes feature importance, counterfactual and anchor-based explainers.
"""

from altai.utils.missing_optional_dependency import import_optional
from altai.explainers.ale import ALE, plot_ale
from altai.explainers.anchors.anchor_text import AnchorText
from altai.explainers.anchors.anchor_tabular import AnchorTabular
from altai.explainers.anchors.anchor_image import AnchorImage
from altai.explainers.cfrl_base import CounterfactualRL
from altai.explainers.cfrl_tabular import CounterfactualRLTabular
from altai.explainers.partial_dependence import PartialDependence, TreePartialDependence, plot_pd
from altai.explainers.pd_variance import PartialDependenceVariance, plot_pd_variance
from altai.explainers.permutation_importance import PermutationImportance, plot_permutation_importance
from altai.explainers.similarity.grad import GradientSimilarity


DistributedAnchorTabular = import_optional(
    'altai.explainers.anchors.anchor_tabular_distributed',
    names=['DistributedAnchorTabular'])

CEM = import_optional(
    'altai.explainers.cem',
    names=['CEM'])

CounterfactualProto, CounterFactualProto = import_optional(
    'altai.explainers.cfproto',
    names=['CounterfactualProto', 'CounterFactualProto'])  # TODO: remove in an upcoming release

Counterfactual, CounterFactual = import_optional(
    'altai.explainers.counterfactual',
    names=['Counterfactual', 'CounterFactual'])  # TODO: remove in an upcoming release

IntegratedGradients = import_optional(
    'altai.explainers.integrated_gradients',
    names=['IntegratedGradients'])

KernelShap, TreeShap = import_optional(
    'altai.explainers.shap_wrappers',
    names=['KernelShap', 'TreeShap'])

__all__ = [
    "ALE",
    "AnchorTabular",
    "DistributedAnchorTabular",
    "AnchorText",
    "AnchorImage",
    "CEM",
    "Counterfactual",
    "CounterfactualProto",
    "CounterfactualRL",
    "CounterfactualRLTabular",
    "plot_ale",
    "PartialDependence",
    "TreePartialDependence",
    "PartialDependenceVariance",
    "PermutationImportance",
    "plot_pd",
    "plot_pd_variance",
    "plot_permutation_importance",
    "IntegratedGradients",
    "KernelShap",
    "TreeShap",
    "GradientSimilarity"
]
