import os
import pandas as pd
import groq
import openai
import wandb

from langchain_community.callbacks import get_openai_callback
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from typing import Optional

from dssatlm.llm import LanguageModel

from dssatlm.envs import (
    SYS_PROMPT_TEMPLATE_AS_PARSER_FPATH,
    USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH,
    SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH,
    USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH,
    SYS_PROMPT_TEMPLATE_AS_PARSER_FOR_Q2S_FPATH,
    DEFINITIONS_BANK_FPATH,
    QUESTIONS_BANK_FPATH,
    SAMPLE_DEFN_N_QUESTIONS_COVERED_FPATH,
    LLM_IDS_CONSIDERED,
    API_KEYS_REQUIRED,
    DEFAULT_WANDB_PROJECT_PARAMS,
    TMP_DIR,
    MISSING_OR_NA_REPR,
    WAITING_TIME_FOR_GROQ_FREEMIUM_API_CALL,
    REQUIRED_DSSATSIM_OUTPUT_KEYS,
    UNWANTED_SUB_KEYS_FROM_SIMULATOR_OUTPUT,
)

from dssatlm.structured_responses import (
    DssatLMInterpreterResponseBatch, 
    DssatLMParserResponse, 
    DssatLMInterpreterResponseSingle,
    default_questions_missing
)

from dssatlm.structured_components import FARM_COMPONENTS_TO_STRUCT_MAP

from dssatlm.utils import (
    get_current_time, 
    get_schema_dict_from_pydanticmodel, 
    dict_to_json_file,
    extract_json_from_llama_like_llms,
    JsonOutputParserWithPostProcessing,
)

from dssatsim import run_dssat_exp_cli


class DSSATAnyLMPipeline:
    def __init__(
            self, 
            parser_model_id, 
            interpreter_model_id, 
            parser_params=None, 
            interpreter_params=None, 
            wandb_params=DEFAULT_WANDB_PROJECT_PARAMS
        ):

        self.setup_api_keys()
        self.wandb_run = self.set_up_wandb(wandb_params)

        parser_params = parser_params or {}
        interpreter_params = interpreter_params or {}

        self.parser_model_id = parser_model_id
        self.interpreter_model_id = interpreter_model_id
        self.ensure_llm_ids_are_valid()
        self.set_llm_ids_full()
        self.parser = LanguageModel(self.parser_model_id_full, **parser_params)
        self.interpreter = LanguageModel(self.interpreter_model_id_full, **interpreter_params)
        self.simulator = None

        self.dssatlm_simulator_response = {"simulation_results": "impossible"}
        self.simulation_is_possible = False
        self.missing_value_id = "missing"
        self.default_empty_answer_for_farmer = "Sorry, your answer cannot be answered at the moment."

        self.pipeline_logs, self.execution_errors_list = self.setup_pipeline_logs()
        

    def answer_query(self, farmer_input_query):
        """
        Answer a query using the DSSAT LLM pipeline
        """
        try:
            dssatlm_parser_response = self.parse_querry_to_simulator_structure(farmer_input_query)

            dssatlm_simulator_response = self.run_dssat_simulation(dssat_input_json=dssatlm_parser_response)

            if "llama" in self.interpreter_model_id:
                import time
                time.sleep(WAITING_TIME_FOR_GROQ_FREEMIUM_API_CALL)

            if "llama" in self.interpreter_model_id:
                interpreter_function = self.interpret_simulation_results_for_farmer_llama
            else:
                interpreter_function = self.interpret_simulation_results_for_farmer
 
            dssatlm_interpreter_response = interpreter_function(
                question_statements=dssatlm_parser_response["question_statements"], 
                sim_outputs_json=dssatlm_simulator_response
            )
            
            _ = self.create_final_outputs(
                sim_outputs_json=dssatlm_simulator_response, 
                question_statements_parsed=dssatlm_interpreter_response["questions"]
            )


        except Exception as e:
            # because this must be some unaccounted error
            if str(e) not in self.execution_errors_list:
                self.pipeline_logs["pipeline_ran_successfully"] = False
            else:
                print(f"Pipeline ran as expected but some warning : {str(e)}")
        
        self.save_logs()
        self.close_wandb()

        # return self.get_logs(subkey="dssatlm_interpreter_response")
        return self.get_logs(subkey="outputs")
        
    
    # ================== PARSER ==================

    def generate_prompt_for_parser(self, system_template_fpath=None, user_template_fpath=None):

        if system_template_fpath is None:
            system_template_fpath = SYS_PROMPT_TEMPLATE_AS_PARSER_FPATH
        if user_template_fpath is None:
            user_template_fpath = USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH

        with open(system_template_fpath, 'r') as f:
            sys_prompt_template_as_parser = f.read()

        with open(user_template_fpath, 'r') as f:
            user_prompt_template_for_parser = f.read()

        if self.parser_model_id == "dsr1-llama-70b":
            sys_prompt_template = ""
            user_prompt_template = f"{sys_prompt_template_as_parser}\n{user_prompt_template_for_parser}"
        else:
            sys_prompt_template = sys_prompt_template_as_parser
            user_prompt_template = user_prompt_template_for_parser

        instructions_prompt_template =  ChatPromptTemplate.from_messages([
            ("system", sys_prompt_template),
            ("user", user_prompt_template)
        ])

        return instructions_prompt_template
    

    def parse_query_to_struture(self, farmer_input_query, farm_component):

        instructions_prompt_template = self.generate_prompt_for_parser(
            system_template_fpath=SYS_PROMPT_TEMPLATE_AS_PARSER_FOR_Q2S_FPATH,
            user_template_fpath=USR_PROMPT_TEMPLATE_FOR_PARSER_FPATH
        )

        if farm_component not in FARM_COMPONENTS_TO_STRUCT_MAP:
            raise ValueError(f"Farm component {farm_component} is not in the list of supported farm components: {FARM_COMPONENTS_TO_STRUCT_MAP.keys()}")
        
        query_json_structure = FARM_COMPONENTS_TO_STRUCT_MAP[farm_component]

        json_parser = JsonOutputParserWithPostProcessing()
        q2s_parser_chain = instructions_prompt_template | self.parser.model | json_parser

        try:
            with get_openai_callback() as cb:
                parsed_response = q2s_parser_chain.invoke({
                    "QUERY_JSON_STRUCTURE": query_json_structure,
                    "FARMER_INPUT_QUERY": farmer_input_query
                })


                # if self.parser_model_id == "dsr1-llama-70b":
                #     parsed_response = extract_json_from_deepseek(parsed_response)

                return parsed_response
            
        except Exception as e:
            err_msg = f"Error while parsing query to structure: {str(e)}"
            return {"error": err_msg}



    def parse_querry_to_simulator_structure(self, farmer_input_query):
        
        parser_output_cmd = PydanticOutputParser(pydantic_object=DssatLMParserResponse)
        instructions_prompt_template = self.generate_prompt_for_parser()
        parser_chain = instructions_prompt_template | self.parser.model | parser_output_cmd

        # Format the prompt with the given variables
        formatted_prompt = instructions_prompt_template.format_prompt(
            format_instructions=parser_output_cmd.get_format_instructions(),
            FARMER_INPUT_QUERY=farmer_input_query
        )
        self.pipeline_logs["prompt_provided_to_llm_as_parser"] = formatted_prompt.to_string()

        model_name_as_role = f"{self.parser_model_id}_as_parser"
        error_type = self.execution_errors_list[0]
        try:
            with get_openai_callback() as cb:
                parsed_response = parser_chain.invoke({
                    "format_instructions": parser_output_cmd.get_format_instructions(),
                    "FARMER_INPUT_QUERY": farmer_input_query
                })

                dssatlm_parser_response = self.unpack_parser_output(parsed_response)
                self.pipeline_logs["dssatlm_parser_response"] = dssatlm_parser_response
                self.pipeline_logs["question_statements_parsed"] = dssatlm_parser_response["question_statements"]
                self.pipeline_logs["dssatlm_parser_response_metadata"] = self.record_api_usage(model_name_as_role, cb)
                print("Step 1: Successfully parsed the query to simulator structure.")
                return dssatlm_parser_response
            
        except groq.APIStatusError as e:
            self.handle_groq_api_error(e, error_type, model_name_as_role, "Step 1")

        except openai.AuthenticationError as e:
            self.handle_open_api_error()

        except Exception as e:
            self.handle_generic_error(e, error_type, model_name_as_role, "Step 1 (parsing query to simulator structure (question and input.json))")
        

    def unpack_parser_output(self, parsed_response: DssatLMParserResponse = None) -> dict:
        parsed_response = parsed_response if parsed_response else DssatLMParserResponse()
        parser_output = {**get_schema_dict_from_pydanticmodel(parsed_response)}
        return parser_output


    # ================== SIMULATOR ==================

    def is_simulation_possible(self, dssat_input_json):
        self.simulation_is_possible = run_dssat_exp_cli.is_simulation_possible(dssat_input_json)
        self.pipeline_logs["simulation_is_possible"] = self.simulation_is_possible
        return self.simulation_is_possible
    
    def was_simulation_successful(self, dssatlm_simulator_response):
        simulation_is_successful = REQUIRED_DSSATSIM_OUTPUT_KEYS <= set(dssatlm_simulator_response.keys())
        self.pipeline_logs["simulation_is_successful"] = simulation_is_successful
        return simulation_is_successful
    
    def get_primary_simulation_outputs(self, simulator_response):
        primary_outputs = {key: simulator_response[key] for key in REQUIRED_DSSATSIM_OUTPUT_KEYS if key in simulator_response}
        for key in primary_outputs:
            primary_outputs[key] = {sub_key: value for sub_key, value in primary_outputs[key].items() if sub_key not in UNWANTED_SUB_KEYS_FROM_SIMULATOR_OUTPUT}
        
        return primary_outputs

    def run_dssat_simulation(self, dssat_input_json):
        """
        Run DSSAT simulation with the required inputs
        """
        error_type = self.execution_errors_list[1]
        try:

            if not self.is_simulation_possible(dssat_input_json):
                self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: Simulation is not possible due to missing required inputs."
                raise ValueError(error_type)
            
            else:
                _, simulator_response = run_dssat_exp_cli.exec(input_file=dssat_input_json)
                self.dssatlm_simulator_response = self.get_primary_simulation_outputs(simulator_response)

                if not self.was_simulation_successful(self.dssatlm_simulator_response):
                    self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: Simulation run but was not successful. Required SUMMARY.OUT's output keys are missing."
                    raise ValueError(error_type)
                
                self.pipeline_logs["dssatlm_simulator_response"] = self.dssatlm_simulator_response
                print("Step 2: Successfully ran DSSAT simulation")
                return self.dssatlm_simulator_response

        except Exception as e:
            self.pipeline_logs["execution_errors"][error_type] += f"\n At {get_current_time()}: (while running DSSAT simulation): {str(e)}"
            raise ValueError(error_type)
        

    # ================== INTERPRETER ==================

    def generate_prompt_for_interpreter(self):

        with open(SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH, 'r') as f:
            sys_prompt_template_as_interpreter = f.read()

        with open(USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH, 'r') as f:
            user_prompt_template_for_interpreter = f.read()

        instructions_prompt_template =  ChatPromptTemplate([
            ("system", sys_prompt_template_as_interpreter),
            ("user", user_prompt_template_for_interpreter)
        ])

        return instructions_prompt_template
    

    def interpret_simulation_results_for_farmer_llama(
            self,
            question_statements: list,
            sim_outputs_json: dict,
            definitions_bank: Optional[str] = None,
            questions_bank: Optional[str] = None
        ):

        model_name_as_role = f"{self.interpreter_model_id}_as_interpreter"
        error_type = self.execution_errors_list[2]

        question_statements_as_str = ""
        for i, q in enumerate(question_statements, 1):
            question_statements_as_str += f"Question {i}: {q}\n"

        print("The question statements are: ", question_statements_as_str)

        if definitions_bank is None:
            with open(DEFINITIONS_BANK_FPATH, 'r') as f: definitions_bank = f.read()
        if questions_bank is None:
            with open(QUESTIONS_BANK_FPATH, 'r') as f: questions_bank = f.read()

        # instructions_prompt_template = self.generate_prompt_for_interpreter()
        with open(SYS_PROMPT_TEMPLATE_AS_INTERPRETER_FPATH, 'r') as f:
            sys_prompt_template_as_interpreter = f.read()

        with open(USR_PROMPT_TEMPLATE_FOR_INTERPRETER_FPATH, 'r') as f:
            user_prompt_template_for_interpreter = f.read()


        questions_dict_empty_default = {
            f"question_{i+1}":  default_questions_missing(question_statements[i])
            for i in range(len(question_statements))
        }
        self.pipeline_logs["dssatlm_interpreter_response"] = questions_dict_empty_default
        self.pipeline_logs["outputs"] = questions_dict_empty_default

        instructions_prompt_template = f"{sys_prompt_template_as_interpreter}\n{user_prompt_template_for_interpreter}"

        # Create parser
        output_parser = PydanticOutputParser(pydantic_object=DssatLMInterpreterResponseBatch)
        
        # Create prompt
        prompt = PromptTemplate(
            template=instructions_prompt_template,
            input_variables=[
                "DEFINITIONS_BANK",
                "QUESTIONS_BANK", 
                "SIMULATION_OUTCOMES_IN_JSON",
                "FARMER_QUESTION_STATEMENTS",
                "format_instructions"
            ]
        )
        
        # Create chain
        formatted_prompt = prompt.format_prompt(
            format_instructions=output_parser.get_format_instructions(),
            SIMULATION_OUTCOMES_IN_JSON=sim_outputs_json,
            FARMER_QUESTION_STATEMENTS=question_statements_as_str,
            DEFINITIONS_BANK=definitions_bank,
            QUESTIONS_BANK=questions_bank
        )
        
        try:
            # Get response
            response = self.interpreter.model.predict(formatted_prompt.to_string())

        except groq.APIStatusError as e:
            self.handle_groq_api_error(e, error_type, model_name_as_role, "Step 3")
            return
    
        # Parse response
        try:
            # First check if the response is valid JSON
            import json
            try:
                json_response = extract_json_from_llama_like_llms(response)

            except json.JSONDecodeError as e:
                err = f"Invalid JSON response: {e}. Raw response: {response}"
                print(err)
                self.handle_generic_error(e, error_type, model_name_as_role, f"Step 3 (interpreting simulation results for farmer). More details: {err}")
            
            # Convert JSON to DssatLMInterpreterResponseBatch
            try:

                # First validate the questions dict
                questions_dict = {}
                if "questions" not in json_response:
                    json_response = {"questions": {**json_response}}
                    
                for q_id, q_data in json_response["questions"].items():
                    single_response = DssatLMInterpreterResponseSingle(
                        question_statement=q_data.get("question_statement", "Missing"),
                        matched_question_found=q_data.get("matched_question_found", "Not Found"),
                        retrieved_answer=q_data.get("retrieved_answer", "Not Found"),
                        answer_for_farmer=q_data.get("answer_for_farmer", "Sorry, your question cannot be answered at the moment.")
                    )
                    questions_dict[q_id] = single_response

                # Create final DssatLMInterpreterResponseBatch
                parsed_response = DssatLMInterpreterResponseBatch(questions=questions_dict)

            except Exception as e:
                err = f"Error converting JSON to DssatLMInterpreterResponseBatch: {e}\nJSON response: {json_response}"
                print(err)
                self.handle_generic_error(e, error_type, model_name_as_role, f"Step 3 (interpreting simulation results for farmer). More details: {err}")
            
            # Verify we have responses for all questions
            expected_questions = {f"question_{i+1}" for i in range(len(question_statements))}
            actual_questions = set(parsed_response.questions.keys())
            if expected_questions != actual_questions:
                print(f"Missing responses for questions: {expected_questions - actual_questions}")

            self.pipeline_logs["dssatlm_interpreter_response"] = self.unpack_interpreter_output(parsed_response)
            print("Step 3: Successfully interpreted simulation results for farmer.")
            
            return self.pipeline_logs["dssatlm_interpreter_response"]
        
        except Exception as e:
            err = f"Error parsing response: {e}. Raw response: {response}"
            self.handle_generic_error(e, error_type, model_name_as_role, f"Step 3 (interpreting simulation results for farmer). More details: {err}")

    
    def interpret_simulation_results_for_farmer(
            self, 
            question_statements, 
            sim_outputs_json, 
            definitions_bank=None, 
            questions_bank=None
        ):
        
        question_statements_as_str = ""
        for i, q in enumerate(question_statements, 1):
            question_statements_as_str += f"Question {i}: {q}\n"

        interpreter_output_cmd = PydanticOutputParser(pydantic_object=DssatLMInterpreterResponseBatch)


        if definitions_bank is None:
            with open(DEFINITIONS_BANK_FPATH, 'r') as f: definitions_bank = f.read()
        if questions_bank is None:
            with open(QUESTIONS_BANK_FPATH, 'r') as f: questions_bank = f.read()

        instructions_prompt_template = self.generate_prompt_for_interpreter()

        # option1. old way that works for GPT models
        interpreter_chain = instructions_prompt_template | self.interpreter.model | interpreter_output_cmd

        formatted_prompt = instructions_prompt_template.format_prompt(
            format_instructions=interpreter_output_cmd.get_format_instructions(),
            SIMULATION_OUTCOMES_IN_JSON=sim_outputs_json,
            FARMER_QUESTION_STATEMENTS=question_statements_as_str,
            DEFINITIONS_BANK=definitions_bank,
            QUESTIONS_BANK=questions_bank
        )
        self.pipeline_logs["prompt_provided_to_llm_as_interpreter"] = formatted_prompt.to_string()
        
        model_name_as_role = f"{self.interpreter_model_id}_as_interpreter"
        error_type = self.execution_errors_list[2]

        try:
            with get_openai_callback() as cb:
                interpreted_response = interpreter_chain.invoke({
                    "format_instructions": interpreter_output_cmd.get_format_instructions(),
                    "SIMULATION_OUTCOMES_IN_JSON": sim_outputs_json,
                    "FARMER_QUESTION_STATEMENTS": question_statements_as_str,
                    'DEFINITIONS_BANK': definitions_bank,
                    'QUESTIONS_BANK': questions_bank
                })

                self.pipeline_logs["dssatlm_interpreter_response"] = self.unpack_interpreter_output(interpreted_response)
                self.pipeline_logs["dssatlm_interpreter_response_metadata"] = self.record_api_usage(model_name_as_role, cb)
                print("Step 3: Successfully interpreted simulation results for farmer.")
                
                return self.pipeline_logs["dssatlm_interpreter_response"]
            
        except groq.APIStatusError as e:
            self.handle_groq_api_error(e, error_type, model_name_as_role, "Step 3")

        except openai.error.AuthenticationError as e:
            self.handle_open_api_error()
        
        except Exception as e:
            self.handle_generic_error(e, error_type, model_name_as_role, "Step 3 (interpreting simulation results for farmer)")


    def create_final_outputs(self, sim_outputs_json, question_statements_parsed):
        """
        Create a formulaic ground truth answer for the farmer
        """
        final_outputs = {}
        for q_key, info_match_for_q in question_statements_parsed.items():
            # matched_question_found = info_match_for_q.get("matched_question_found", MISSING_OR_NA_REPR)
            matched_question_found = info_match_for_q["matched_question_found"]
            expert_like_answer = self.form_expert_like_answer(sim_outputs_json, matched_question_found)
            info_match_for_q["expert_like_answer"] = expert_like_answer
            final_outputs[q_key] = info_match_for_q

        self.pipeline_logs["outputs"] = final_outputs
        return final_outputs


    def form_expert_like_answer(self, sim_outputs_json, question_statement):
        sample_dfn_n_questions_df = pd.read_csv(SAMPLE_DEFN_N_QUESTIONS_COVERED_FPATH)

        if question_statement not in sample_dfn_n_questions_df["QUESTIONS"].values:
            answer_statement = MISSING_OR_NA_REPR
        else:
            df_ = sample_dfn_n_questions_df[sample_dfn_n_questions_df["QUESTIONS"] == question_statement]
            category_definition = df_["CATEGORY_DEFINITIONS"].values[0]
            category_type = df_["CATEGORY-TYPE"].values[0]
            category = df_["CATEGORY"].values[0]
            answer_value = sim_outputs_json[category_type][category]
            answer_statement = f"The {category} is {answer_value}. Here is more definition: {category_definition}"

        return answer_statement


    def unpack_interpreter_output(self, interpreted_response: DssatLMInterpreterResponseBatch = None) -> dict:
        interpreted_response = interpreted_response if interpreted_response else DssatLMInterpreterResponseBatch()
        interpreted_output = {**get_schema_dict_from_pydanticmodel(interpreted_response)}
        return interpreted_output

   
    # ================== MISC & HELPERS ==================

    def handle_wandb_api_error(self):
        raise ValueError("WandB API key is invalid.")
    
    def handle_open_api_error(self):
        raise ValueError("OpenAI API key is invalid.")
    
    def handle_groq_api_error(self, e, error_type, model_name_as_role, context):
        if e.status_code == 413:
            nice_error_message = f"{context}: Failed because the LLM is unable to process this payload. The input to the LLM is too large (according to the API provider service), and thus must be reduced."
        elif e.status_code == 401:
            nice_error_message = f"{context}: Failed because the API key is invalid."
            raise ValueError("GROQ API key is invalid.")
        elif e.status_code == 429:
            nice_error_message = f"{context}: Failed because the API rate limit has been exceeded."
        else:
            nice_error_message = f"{context}: Failed due to an API status error."

        print(nice_error_message)
        self.pipeline_logs["execution_errors"][error_type] += f"\n At {self.get_current_time()}: {nice_error_message}. More details: {str(e)} | {model_name_as_role}"
        raise ValueError(error_type)

    def handle_generic_error(self, e, error_type, model_name_as_role, context):
        self.pipeline_logs["execution_errors"][error_type] += f"\n At {self.get_current_time()}: (while {context}): {str(e)} | {model_name_as_role}"
        raise ValueError(error_type)

    def record_api_usage(self, model_name_as_role, chain_callback=None) -> dict:
        # see https://python.langchain.com/docs/how_to/llm_token_usage_tracking/
        return {
            f"{model_name_as_role} - Total Tokens" : chain_callback.total_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Prompt Tokens": chain_callback.prompt_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Completion Tokens": chain_callback.completion_tokens if chain_callback else self.missing_value_id,
            f"{model_name_as_role} - Total Cost (USD)": chain_callback.total_cost if chain_callback else self.missing_value_id,
        }

    def set_up_wandb(self, wandb_params):
        self.wandb_params = wandb_params
        try:
            return wandb.init(**wandb_params, settings=wandb.Settings(start_method="thread"))

        except wandb.errors.AuthenticationError as e:
            self.handle_wandb_api_error()
        except Exception as e:
            raise ValueError(f"Error while setting up WandB: {str(e)}")
        

    def close_wandb(self):
        self.wandb_run.finish()

    def setup_pipeline_logs(self):
        log = {
            "simulation_is_possible": self.simulation_is_possible,
            "simulation_is_successful": False,
            "pipeline_ran_successfully": True,
            "question_statements_parsed": [],
            "dssatlm_parser_response": self.unpack_parser_output(parsed_response=None),
            "dssatlm_parser_response_metadata": self.record_api_usage(f"{self.parser_model_id}_as_parser", chain_callback=None),
            "dssatlm_simulator_response": self.dssatlm_simulator_response,
            "dssatlm_simulator_ground_truth_answer": None,
            "outputs": self.unpack_interpreter_output(interpreted_response=None),
            "dssatlm_interpreter_response": self.unpack_interpreter_output(interpreted_response=None),
            "dssatlm_interpreter_response_metadata": self.record_api_usage(f"{self.interpreter_model_id}_as_interpreter", chain_callback=None),
            "prompt_provided_to_llm_as_parser": None,
            "prompt_provided_to_llm_as_interpreter": None,
            "execution_errors": {
                "Error occured in step 1 (Parsing)": "",
                "Error occured in step 2 (Simulation)": "",
                "Error occured in step 3 (Interpreting)": "",
            },
        }
        execution_errors_list = list(log["execution_errors"].keys())
        return log, execution_errors_list
    
    def get_logs(self, subkey=None):
        if subkey:
            return self.pipeline_logs[subkey] if subkey in self.pipeline_logs else None
        return self.pipeline_logs
    
    def save_logs(self, output_dir=TMP_DIR):
        prefix = "dssatlm_logs"
        if 'name' in self.wandb_params:
            fname = self.wandb_params["name"].replace("run", prefix)
        else:
            fname = f"{prefix}_{get_current_time()}".replace(" ", "_").replace(":", "-")

        file_path = os.path.join(TMP_DIR, f"{fname}.json")

        dict_to_json_file(self.pipeline_logs, file_path)
        self.save_wandb_artifact(file_path, os.path.basename(file_path), "logs")
        print(f"Logs saved at: {file_path}. And also saved as a WandB artifact.")

    def save_wandb_artifact(self,  artifact_file_path, artifact_name, artifact_type='dataset'):
        artifact = wandb.Artifact(artifact_name, type=artifact_type)
        artifact.add_file(artifact_file_path)
        self.wandb_run.log_artifact(artifact)

    
    def setup_api_keys(self):
        for api_key in API_KEYS_REQUIRED:
            if not os.environ.get(api_key):
                raise ValueError(f"{api_key} is required but not found in the environment variables. Please set it before instantiating the pipeline.")

        
    def ensure_llm_ids_are_valid(self):
        if self.parser_model_id not in LLM_IDS_CONSIDERED:
            raise ValueError(f"Parser model ID {self.parser_model_id} is not in the list of considered LLM IDs: {LLM_IDS_CONSIDERED.keys()}")
        if self.interpreter_model_id not in LLM_IDS_CONSIDERED:
            raise ValueError(f"Interpreter model ID {self.interpreter_model_id} is not in the list of considered LLM IDs: {LLM_IDS_CONSIDERED.keys()}")

    def set_llm_ids_full(self):
        self.parser_model_id_full = LLM_IDS_CONSIDERED[self.parser_model_id]
        self.interpreter_model_id_full = LLM_IDS_CONSIDERED[self.interpreter_model_id]

    def __repr__(self):
        return f"DSSATAnyLMPipeline(parser={self.parser}, interpreter={self.interpreter})"
    

