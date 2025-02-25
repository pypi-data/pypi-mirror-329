
from dssatlm.envs import DEFAULT_LLM_PARAMS
from langchain_core.rate_limiters import InMemoryRateLimiter


LANGCHAIN_RATE_LIMITER = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

class LanguageModel:
    def __init__(
            self, 
            model_id, 
            max_tokens=DEFAULT_LLM_PARAMS['max_tokens'], 
            temperature=DEFAULT_LLM_PARAMS['temperature'], 
            top_p=DEFAULT_LLM_PARAMS['top_p'],
            inference_type='api', 
            **kwargs
        ):
        self.model_id = model_id
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.inference_type = inference_type
        self.params = kwargs
        self.model_provider = self.setup_model_provider()
        self.model = self.setup_model()

    def setup_model_provider(self):
        if self.model_id.startswith('llama') or 'llama' in self.model_id:
            return 'groq'
        elif self.model_id.startswith('gpt'):
            return 'openai'
        else:
            return None # it will be infered by langchain automatically

    def setup_model(self):
        if self.inference_type == 'api':
            return self.setup_model_as_api()
        elif self.inference_type == 'local':
            return self.setup_model_as_local()
        else:
            raise ValueError(f"Invalid inference type: {self.inference_type}. Must be either 'api' or 'local'.")

    def setup_model_as_api(self):
        from langchain.chat_models import init_chat_model
        return init_chat_model(
            model = self.model_id, 
            model_provider=self.model_provider,
            max_tokens=self.max_tokens, 
            temperature=self.temperature, top_p=self.top_p, 
            rate_limiter=LANGCHAIN_RATE_LIMITER , 
            **self.params
        )

    def setup_model_as_local(self):
        raise NotImplementedError("Local inference is not yet supported.")

    def __repr__(self):
        return f"LanguageModel(model_id={self.model_id}, max_tokens={self.max_tokens}, temperature={self.temperature}, top_p={self.top_p}, params={self.params})"

