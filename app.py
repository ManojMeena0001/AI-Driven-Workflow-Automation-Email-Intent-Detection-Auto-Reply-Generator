# app.py
import argparse
import pandas as pd
import os

# Import modules from your src folder
from src.utils import ensure_dirs, load_raw_data
from src.preprocess import prepare_text_column
from src.predict import IntentPredictor
from src.auto_reply import generate_reply

def run_automation_pipeline(input_csv: str, output_csv: str, conf_threshold: float = 0.7):
    """
    Runs the end-to-end email intent detection and auto-reply generation pipeline.
    """
    # 1. Setup
    ensure_dirs()
    
    # 2. Data Ingestion
    df_raw = load_raw_data(input_csv)
    if df_raw.empty:
        print("[ERROR] Input data frame is empty. Exiting.")
        return

    # 3. Text Preprocessing
    df_processed = prepare_text_column(df_raw, text_col='text')
    
    # 4. Model Loading and Prediction
    try:
        predictor = IntentPredictor() # Loads intent_pipeline.joblib
        clean_texts = df_processed['text_clean'].tolist()
        predictions = predictor.predict(clean_texts)
    except FileNotFoundError as e:
        print(f"[FATAL ERROR] {e}")
        print("Please ensure 'intent_pipeline.joblib' is in the 'model/' directory.")
        return

    # 5. Auto-Reply Generation and Review Logic
    output_rows = []
    
    for index, row in df_processed.iterrows():
        pred = predictions[index]
        intent = pred["intent"]
        confidence = pred["confidence"]
        
        # Determine if human review is needed (Automation Safety Check)
        needs_review = confidence < conf_threshold
        
        # Generate the automated response
        # Using the 'from' column as the 'name' placeholder
        sender_name = str(row.get('from', '')) 
        
        reply = generate_reply(
            intent=intent, 
            name=sender_name.split('@')[0] if '@' in sender_name else sender_name,
            issue_id=f"TICKET-{index+1}" # Simple dummy ID for support tickets
        )
        
        output_rows.append({
            'id': row.get('id', index),
            'from': row.get('from'),
            'subject': row.get('subject'),
            'intent': intent,
            'confidence': f"{confidence:.2f}",
            'needs_review': needs_review,
            'auto_reply_text': reply
        })

    # 6. Save Output
    df_output = pd.DataFrame(output_rows)
    df_output.to_csv(output_csv, index=False)
    print(f"\n[SUCCESS] Pipeline finished. Processed {len(df_output)} emails.")
    print(f"[SUCCESS] Results saved to: {output_csv}")
    print(f"[INFO] Emails needing human review (Confidence < {conf_threshold}): {df_output['needs_review'].sum()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run AI Email Intent Detection and Auto-Reply Automation Pipeline."
    )
    parser.add_argument(
        "--input", "-i", 
        type=str, 
        required=True, 
        help="Path to the input CSV file containing emails (with subject/body columns)."
    )
    parser.add_argument(
        "--output", "-o", 
        type=str, 
        default="data/processed_output.csv", 
        help="Path where the final processed CSV should be saved."
    )
    parser.add_argument(
        "--threshold", "-t", 
        type=float, 
        default=0.7, 
        help="Confidence threshold below which emails are flagged for human review."
    )
    
    args = parser.parse_args()
    run_automation_pipeline(args.input, args.output, args.threshold)