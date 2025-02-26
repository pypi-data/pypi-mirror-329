"""MLflow wrapper for KIE model."""

import logging
from typing import Any, Dict

import pandas as pd
from mlflow.pyfunc import PythonModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class KIEGroundingModel(PythonModel):
    """MLflow model for KIE grounding."""

    def load_context(self, context) -> None:
        """Load the model artifacts from the context."""
        # pylint: disable=import-outside-toplevel
        import mlflow

        mlflow.set_tracking_uri("databricks")
        mlflow.set_registry_uri("databricks-uc")

    def get_endpoint_context(self):
        """Get appropriate endpoint context based on configuration."""
        # pylint: disable=import-outside-toplevel
        from functools import partial

        from databricks.model_serving.types.pt_endpoint import PayGoEndpoint

        # TODO: let's not hardcode this in the future.
        # I had to do this because currently model specs rely on the
        # existence of pt equivalents which do not exist in all workspaces
        paygo_endpoint_name = 'databricks-meta-llama-3-3-70b-instruct'
        return partial(PayGoEndpoint, paygo_endpoint_name)

    def get_ground_truth_prompt(self, response_format) -> str:
        """Get ground truth prompt for the model."""
        # pylint: disable=import-outside-toplevel
        from databricks.kie.prompt_builder import PromptBuilder
        return PromptBuilder(response_format).build_prompt()

    def generate_responses(self, requests, response_format):
        """Generate responses for requests without expected responses.
        
        Args:
            requests: List of request strings to generate responses for
            response_format: Response format
            
        Returns:
            List of generated response dictionaries
        """
        ground_truth_prompt = self.get_ground_truth_prompt(response_format)

        endpoint_context = self.get_endpoint_context()
        with endpoint_context() as endpoint:
            responses = endpoint.generate_batch(requests,
                                                system_prompt=ground_truth_prompt,
                                                response_format=response_format,
                                                show_progress=False)
        return responses

    def evaluate(self, df: pd.DataFrame, response_format) -> pd.DataFrame:
        """Generate evaluation results."""
        # pylint: disable=import-outside-toplevel
        from databricks.kie.kie_evaluator import OVERALL_SCORE, KIEEvaluator

        eval_class = KIEEvaluator(response_format)

        def process_row(row) -> Dict[str, Any]:
            """Process a single row ensuring all inputs remain as strings."""
            request = str(row['request'])
            response_str = str(row['generated_response'])
            expected_response_str = str(row['expected_response'])

            eval_output_per_key, eval_output_overall = eval_class.evaluate_row(request, expected_response_str,
                                                                               response_str)

            result = {
                'metric/kie/is_schema_match/value': eval_output_overall['is_schema_match'].value,
                'metric/kie/is_schema_match/rationale': eval_output_overall['is_schema_match'].rationale,
                'metric/kie/overall_score/value': eval_output_overall[OVERALL_SCORE].value,
                'metric/kie/overall_score/rationale': eval_output_overall[OVERALL_SCORE].rationale,
            }

            result.update({
                key: value for field_name, assessment in eval_output_per_key.items()
                for key, value in [(f"metric/kie/{field_name}/value",
                                    assessment.value), (f"metric/kie/{field_name}/rationale", assessment.rationale)]
            })

            return result

        df_results = pd.DataFrame(df.apply(process_row, axis=1))
        logger.info(f'Finished generating evaluation results for {len(df_results)} rows')

        return df_results

    def predict(self, context, model_input, params=None):
        """Label KIE grounding samples and return evaluation results."""
        # pylint: disable=import-outside-toplevel
        import json

        # pylint: disable=import-outside-toplevel
        from databricks.kie.kie_schema import ModelFactory

        del context
        if params is None:
            raise ValueError("Expected params to be a dict containing the 'json_schema' for grounding but found None.")

        json_schema = params['json_schema']
        json_schema_dict = json.loads(json_schema)
        logger.info(f"Received json schema: {json_schema_dict}")

        response_format = ModelFactory.from_json_schema(json_schema_dict)

        df = model_input.copy()
        generated_responses = self.generate_responses(df['request'].tolist(), response_format)

        df['generated_response'] = [r.response for r in generated_responses]

        # If the user does not provide an expected response, use the generated response
        df['expected_response'] = df['expected_response'].replace('', pd.NA).fillna(df['generated_response'])
        df['eval_results'] = self.evaluate(df, response_format)

        return df
