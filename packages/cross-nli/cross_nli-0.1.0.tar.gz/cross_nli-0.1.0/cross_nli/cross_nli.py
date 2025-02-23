import os
import torch
import json
import numpy as np
import re
from tqdm import tqdm
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    GenerationConfig,
)
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("cross_nli.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ],
)


class Cross_NLI:
    def __init__(self, data_path):
        self.path = data_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.nli_id = "cross-encoder/nli-deberta-base"
        self.llm_id = "meta-llama/Meta-Llama-3-8B-Instruct"

        self.tokenizer_nli = AutoTokenizer.from_pretrained(self.nli_id)
        self.model_nli = AutoModelForSequenceClassification.from_pretrained(self.nli_id).to(self.device)

        self.tokenizer_llm = AutoTokenizer.from_pretrained(self.llm_id, trust_remote_code=True)
        self.tokenizer_llm.pad_token = self.tokenizer_llm.eos_token
        self.tokenizer_llm.padding_side = "right"

        self.model_llm = AutoModelForCausalLM.from_pretrained(
            self.llm_id,
            device_map=self.device,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )

        self.generation_config = GenerationConfig.from_pretrained(
            self.llm_id,
            best_of=1,
            presence_penalty=0.0,
            frequency_penalty=1.0,
            top_p=0.9,
            temperature=1e-10,
            do_sample=True,
            stop=["###", self.tokenizer_llm.eos_token, self.tokenizer_llm.pad_token],
            use_beam_search=False,
            max_new_tokens=600,
            logprobs=5,
            pad_token_id=self.tokenizer_llm.eos_token_id,
        )

    def atomic_unit_extraction(self, datum):
        """Extracts atomic text units from input text using LLM."""
        prompt = """
                **
                IMPORTANT: 
                 - Extract only factual truths from the text.
                 - Do not include any prior knowledge or interpretations.
                 - Take the text at face value when extracting facts.
                 - Ensure each unit is concise and represents the smallest possible factual statement.
                 - Do not include any introductory or explanatory text. Only output the numbered list of atomic units.
                **
        """
    
        messages = [
            {"role": "user", "content": f"Break down the following text into independent atomic text units: {prompt} {datum}"},
        ]
        
        inputs = self.tokenizer_llm.apply_chat_template(messages, return_tensors="pt").to(self.device)

        generated_ids = self.model_llm.generate(inputs, self.generation_config)
        decoded = self.tokenizer_llm.batch_decode(generated_ids[:, inputs.shape[1]:], skip_special_tokens=True)

        return decoded

    def extract_numbered_text(self, text):
        """Extracts numbered list items from a text string."""
        return re.findall(r"\d+\.\s(.*)", text)

    def evaluation(self):
       

        """Evaluates hallucination and coverage using NLI model."""
        data = [json.loads(line) for line in open(self.path, "r", encoding="utf-8")]
        total_coverage = 0
        total_hallucination = 0

       
        
        for i, datum in enumerate(data):
            logging.info(f"Evaluating {i+1} of {len(data)}")
            golden = self.extract_numbered_text(self.atomic_unit_extraction(datum["golden"])[0])
            generated = self.extract_numbered_text(self.atomic_unit_extraction(datum["generated"])[0])

            halucination = np.zeros((len(generated), len(golden)))
            caverage = np.zeros((len(golden), len(generated)))

            # Calculate Hallucination
            for i in range(len(generated)):
                for j in range(len(golden)):
                    input_ids = self.tokenizer_nli(golden[j], generated[i], truncation=True, return_tensors="pt")["input_ids"]
                    output = self.model_nli(input_ids.to(self.device))
                    logits = torch.softmax(output["logits"][0], -1).tolist()
                    halucination[i][j] = logits[0]

            halucination_score = np.sum(np.min(halucination, axis=1)) / len(halucination)
            total_hallucination +=halucination_score
            logging.info(f"Hallucination score: {halucination_score}")

            # Calculate Coverage
            for i in range(len(golden)):
                for j in range(len(generated)):
                    input_ids = self.tokenizer_nli(generated[j], golden[i], truncation=True, return_tensors="pt")["input_ids"]
                    output = self.model_nli(input_ids.to(self.device))
                    logits = torch.softmax(output["logits"][0], -1).tolist()
                    caverage[i][j] = logits[1]

            caverage_score = np.sum(np.max(caverage, axis=1)) / len(caverage)
            total_coverage +=caverage_score
            logging.info(f"Coverage score: {caverage_score}")
            logging.info(f"**"*20)

        logging.info("Evaluation process complete.")    
        logging.info(f"Total Hallucination: {halucination_score/len(data)}")  
        logging.info(f"Total Caverage: {total_coverage/len(data)}")    

        return halucination_score/len(data), total_coverage/len(data)
