import json
import os

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "data/raw_qa.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data/train.jsonl")


def format_instruction(question, answer, context=""):
    system_prompt = "You are the official IIT Delhi AI Assistant. Answer questions accurately based on campus guidelines."
    user_content = f"Context: {context}\n\nQuestion: {question}" if context else question

    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": answer}
        ]
    }


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Sample dataset template if raw data doesn't exist yet
    sample_data = [
        {
            "question": "What is the grading system at IIT Delhi?",
            "answer": "IIT Delhi uses a 10-point CGPA scale ranging from A (10) to E/F (Failing grades).",
            "context": "IIT Delhi Academic Rules"
        },
        {
            "question": "Where is the Central Library located in IIT Delhi?",
            "answer": "The Central Library is located near the academic block, opposite the Senate House.",
            "context": "Campus Location Guide"
        }
    ]

    raw_items = sample_data
    if os.path.exists(RAW_DATA_PATH):
        with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
            raw_items = json.load(f)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in raw_items:
            formatted = format_instruction(
                item.get("question", ""),
                item.get("answer", ""),
                item.get("context", "")
            )
            f.write(json.dumps(formatted, ensure_ascii=False) + "\n")

    print(f"Dataset successfully prepared: {len(raw_items)} samples written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
