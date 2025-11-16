"""
Multi-LLM Fusion Engine
Queries multiple LLMs and fuses their responses into a refined output
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
import ollama
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelResponse:
    """Container for individual model response"""
    def __init__(self, model_name: str, response: str, time_taken: float, error: Optional[str] = None):
        self.model_name = model_name
        self.response = response
        self.time_taken = time_taken
        self.error = error
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "model_name": self.model_name,
            "response": self.response,
            "time_taken": round(self.time_taken, 2),
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }


class LLMFusionEngine:
    """Main fusion engine for multi-LLM queries"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.models = [m for m in config['models'] if m.get('enabled', True)]
        self.refiner_model = config.get('refiner_model', 'llama3.2')
        self.fusion_strategy = config.get('fusion_strategy', 'refiner')
        self.generation_params = config.get('generation', {})

        # Initialize Ollama client
        ollama_url = config.get('server', {}).get('ollama_base_url', 'http://localhost:11434')
        self.client = ollama.Client(host=ollama_url)

        logger.info(f"Initialized LLM Fusion Engine with {len(self.models)} models")
        logger.info(f"Fusion strategy: {self.fusion_strategy}")

    async def query_model(self, model_name: str, prompt: str) -> ModelResponse:
        """Query a single model asynchronously"""
        start_time = asyncio.get_event_loop().time()

        try:
            logger.info(f"Querying {model_name}...")

            # Run ollama query in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate(
                    model=model_name,
                    prompt=prompt,
                    options={
                        'temperature': self.generation_params.get('temperature', 0.7),
                        'num_predict': self.generation_params.get('max_tokens', 2000),
                    }
                )
            )

            time_taken = asyncio.get_event_loop().time() - start_time
            response_text = response.get('response', '')

            logger.info(f"{model_name} responded in {time_taken:.2f}s")
            return ModelResponse(model_name, response_text, time_taken)

        except Exception as e:
            time_taken = asyncio.get_event_loop().time() - start_time
            error_msg = f"Error: {str(e)}"
            logger.error(f"{model_name} failed: {error_msg}")
            return ModelResponse(model_name, "", time_taken, error_msg)

    async def query_all_models(self, prompt: str) -> List[ModelResponse]:
        """Query all enabled models in parallel"""
        tasks = [
            self.query_model(model['name'], prompt)
            for model in self.models
        ]

        responses = await asyncio.gather(*tasks)
        return responses

    async def refiner_fusion(self, original_prompt: str, model_responses: List[ModelResponse]) -> str:
        """Use refiner model to synthesize best answer from all responses"""

        # Filter out failed responses
        valid_responses = [r for r in model_responses if not r.error]

        if not valid_responses:
            return "All models failed to respond. Please check your Ollama setup."

        if len(valid_responses) == 1:
            return valid_responses[0].response

        # Construct refinement prompt
        responses_text = "\n\n".join([
            f"=== Response from {r.model_name} ===\n{r.response}"
            for r in valid_responses
        ])

        refiner_prompt = f"""You are an expert at synthesizing multiple AI responses into a single, refined answer.

Original Question:
{original_prompt}

Multiple AI models have provided the following responses:

{responses_text}

Your task:
1. Analyze all the responses above
2. Identify the most accurate and helpful information from each
3. Synthesize a single, comprehensive, refined answer that combines the best insights
4. Remove any contradictions or redundancies
5. Provide the final answer in a clear, well-structured format

Refined Answer:"""

        try:
            logger.info(f"Running refiner model: {self.refiner_model}")
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.generate(
                    model=self.refiner_model,
                    prompt=refiner_prompt,
                    options={
                        'temperature': 0.5,  # Lower temperature for more focused refinement
                        'num_predict': self.generation_params.get('max_tokens', 2000),
                    }
                )
            )

            return response.get('response', 'Refinement failed')

        except Exception as e:
            logger.error(f"Refiner model failed: {str(e)}")
            # Fallback to first valid response
            return f"⚠️ Refinement failed. Returning first model response:\n\n{valid_responses[0].response}"

    async def consensus_fusion(self, model_responses: List[ModelResponse]) -> str:
        """Simple consensus-based fusion (for factual queries)"""
        valid_responses = [r for r in model_responses if not r.error]

        if not valid_responses:
            return "All models failed to respond."

        # For consensus, we return the longest response (assuming more detail = better)
        # In a production system, you might use more sophisticated voting
        best_response = max(valid_responses, key=lambda r: len(r.response))

        return f"""=== Consensus Result ===
Selected response from: {best_response.model_name}
(Based on {len(valid_responses)} model responses)

{best_response.response}
"""

    async def fuse_responses(self, prompt: str) -> Dict[str, Any]:
        """Main fusion method - queries all models and returns fused result"""

        start_time = asyncio.get_event_loop().time()

        # Query all models in parallel
        model_responses = await self.query_all_models(prompt)

        # Apply fusion strategy
        if self.fusion_strategy == "refiner":
            fused_response = await self.refiner_fusion(prompt, model_responses)
        else:
            fused_response = await self.consensus_fusion(model_responses)

        total_time = asyncio.get_event_loop().time() - start_time

        result = {
            "prompt": prompt,
            "fusion_strategy": self.fusion_strategy,
            "individual_responses": [r.to_dict() for r in model_responses],
            "fused_response": fused_response,
            "total_time": round(total_time, 2),
            "models_queried": len(self.models),
            "successful_responses": len([r for r in model_responses if not r.error])
        }

        logger.info(f"Fusion complete in {total_time:.2f}s")
        return result
