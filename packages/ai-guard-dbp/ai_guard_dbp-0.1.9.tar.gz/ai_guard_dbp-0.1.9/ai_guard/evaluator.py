# ai_guard/evaluator.py

import pandas as pd
from presidio_analyzer import AnalyzerEngine
from transformers import pipeline
from bert_score import score
from rouge_score import rouge_scorer
from config import RAGASS_THRESHOLD, BERTSCORE_THRESHOLD, ROUGEL_THRESHOLD

# Initialize necessary tools
analyzer = AnalyzerEngine()
toxic_classifier = pipeline("text-classification", model="unitary/toxic-bert")
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

def health_check():
    return "yes!"

def analyze_entities(text):
    results = analyzer.analyze(
        text=text,
        entities=['PERSON', 'EMAIL_ADDRESS', 'PHONE_NUMBER', 'GPE', 'LOCATION'],
        language='en'
    )
    return results

def detect_profanity(text):
    result = toxic_classifier(text)
    for res in result:
        if res['label'] == 'toxic' and res['score'] > 0.9:
            return True
    return False

def calculate_ragass(retrieved_docs, relevant_docs):
    common_docs = set(retrieved_docs).intersection(set(relevant_docs))
    ragass_score = len(common_docs) / len(relevant_docs)
    return ragass_score >= RAGASS_THRESHOLD, ragass_score

def calculate_bertscore(reference, generated):
    P, R, F1 = score([generated], [reference], lang="en")
    bert_score = F1.mean().item()
    return bert_score >= BERTSCORE_THRESHOLD, bert_score

def calculate_rougel(reference, generated):
    scores = scorer.score(reference, generated)
    rougel_score = scores["rougeL"].fmeasure
    return rougel_score >= ROUGEL_THRESHOLD, rougel_score

def evaluate_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    # Ensure the CSV has the required columns
    if 'reference' not in df.columns or 'generated' not in df.columns:
        raise ValueError("CSV must contain 'reference' and 'generated' columns")
    
    results = []  # List to store evaluation results

    for index, row in df.iterrows():
        # Extract reference and generated columns
        reference = row['reference']
        generated = row['generated']
        
        # Apply the evaluation functions
        bert_score_passed, bert_score = calculate_bertscore(reference, generated)
        rougel_passed, rougel_score = calculate_rougel(reference, generated)
        ragass_passed, ragass_score = calculate_ragass([generated], [reference])  # Example retrieval task
        
        # Optionally: Perform profanity check and entity extraction
        is_toxic, toxicity_score = detect_profanity(generated)
        entities = analyze_entities(generated)
        sensitive_entities = [entity.entity_type for entity in entities if entity.entity_type in ['EMAIL_ADDRESS', 'PHONE_NUMBER']]

        # Store the results for the current row
        results.append({
            'index': index,
            'reference': reference,
            'generated': generated,
            'bert_score': bert_score,
            'rougel_score': rougel_score,
            'ragass_score': ragass_score,
            'bert_score_passed': bert_score_passed,
            'rougel_score_passed': rougel_passed,
            'ragass_score_passed': ragass_passed,
            'is_toxic': is_toxic,
            'toxicity_score': toxicity_score,
            'sensitive_entities': ', '.join(sensitive_entities) if sensitive_entities else None
        })

    # Convert results list into a DataFrame
    results_df = pd.DataFrame(results)

    # Optionally: Save the results to a new CSV file
    results_df.to_csv('evaluation_results.csv', index=False)

    return results_df

# Guardrail Check Function
def guardrail_check(query):
    # 1. Profanity Check
    is_toxic, toxicity_score = detect_profanity(query)
    if is_toxic:
        return False, f"Query is toxic with a score of {toxicity_score:.2f}"

    # 2. Entity Extraction Check (Sensitive info like email, phone number)
    entities = analyze_entities(query)
    sensitive_entities = [entity for entity in entities if entity.entity_type in ['EMAIL_ADDRESS', 'PHONE_NUMBER']]
    if sensitive_entities:
        return False, f"Query contains sensitive information: {', '.join([e.entity_type for e in sensitive_entities])}"

    return True, "Query passed all checks"

# Example usage of `guardrail_check`
def process_query(query):
    is_valid, message = guardrail_check(query)
    if not is_valid:
        return f"Query failed: {message}"

    # Proceed with further operations if the query is valid
    return "Query passed guardrail check. Proceeding with further evaluation."
