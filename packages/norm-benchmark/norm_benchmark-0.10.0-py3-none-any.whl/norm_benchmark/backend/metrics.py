import abc

import numpy as np
import scipy
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from sentence_transformers.util import cos_sim
from sklearn.metrics import accuracy_score, f1_score
from tqdm import tqdm

from norm_benchmark.backend.prompts import (labor_grouping_template,
                                  product_grouping_template)
from norm_benchmark.constants import CONFIDENCE_INTERVAL, ELASTICITY


class Metric(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


class TotalCostScore(Metric):
    def __call__(
        self,
        expert_estimate,
        model_estimate,
        ELASTICITY=ELASTICITY,
        CONFIDENCE_INTERVAL=CONFIDENCE_INTERVAL,
    ):
        if self.is_model_within_distribuition(
            model_estimate, expert_estimate, CONFIDENCE_INTERVAL, ELASTICITY
        ):
            return np.abs(expert_estimate - model_estimate) / expert_estimate
        return 0

    def __repr__(self):
        return "TotalCostScore()"

    @staticmethod
    def is_model_within_distribuition(
        estimate, expert_estimate, CONFIDENCE_INTERVAL, ELASTICITY
    ):
        lower, upper = scipy.stats.norm.interval(
            CONFIDENCE_INTERVAL, expert_estimate, expert_estimate * ELASTICITY
        )
        return lower <= estimate <= upper


class SectionScore(Metric):
    def __call__(self, encoder, expert_sections: list, model_sections: list):
        # expert_dict = {section: estimate for section, estimate in expert_sections}
        # model_dict = {section: estimate for section, estimate in model_sections}
        expert_dict = expert_sections
        model_dict = model_sections
        all_sections = list(set(expert_dict.keys()) | set(model_dict.keys()))
        y_true, y_pred = [], []
        estimate_diffs = []

        matched_expert, matched_model = set(), set()

        for section in all_sections:
            found_expert, found_model = False, False

            for expert_section in expert_dict:
                if self.is_similar(encoder, section, expert_section):
                    y_true.append(1)
                    matched_expert.add(expert_section)
                    found_expert = True
                    break
            if not found_expert:
                y_true.append(0)

            for model_section in model_dict:
                if self.is_similar(encoder, section, model_section):
                    y_pred.append(1)
                    matched_model.add(model_section)
                    found_model = True

                    if found_expert:
                        expert_estimate = expert_dict[expert_section]
                        model_estimate = model_dict[model_section]
                        estimate_diffs.append(
                            abs(expert_estimate - model_estimate) / expert_estimate
                        )

                    break
            if not found_model:
                y_pred.append(0)

        # Compute metrics
        f1 = f1_score(y_true, y_pred)
        mape = np.mean(estimate_diffs) if estimate_diffs else None

        return f1, mape

    def __repr__(self):
        return "SectionScore()"

    @staticmethod
    def is_similar(encoder, s1, s2, threshold=0.7):
        if s1 == s2:
            return True

        return cos_sim(encoder.encode(s1), encoder.encode(s2)) >= threshold


class GroupingScore(Metric):
    def __call__(self, encoder, material_data, labor_data, threshold=0.3):

        material_output = []
        for preds in tqdm(material_data):
            for material in preds:
                s1 = product_grouping_template.format(material["product"])
                s2 = labor_grouping_template.format(material["sectionName"])
                material_output.append(
                    int(cos_sim(encoder.encode(s1), encoder.encode(s2)) >= threshold)
                )

        labor_output = []
        for preds in tqdm(labor_data):
            for labor in preds:
                s1 = labor_grouping_template.format(labor["activity"])
                s2 = labor_grouping_template.format(labor["sectionName"])
                labor_output.append(
                    int(cos_sim(encoder.encode(s1), encoder.encode(s2)) >= threshold)
                )

        return sum(material_output) / len(material_output), sum(labor_output) / len(
            labor_output
        )

    def __repr__(self):
        return "GroupingScore()"
