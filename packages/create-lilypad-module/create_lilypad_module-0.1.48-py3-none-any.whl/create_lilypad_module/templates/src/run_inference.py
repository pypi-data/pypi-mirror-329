import os
import sys
import traceback
import json

# TODO: Update ../requirements.txt
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def run_job(input, model, tokenizer):
    """
    Run the job
    """
    try:
        inputs = tokenizer(
            input,
            return_tensors="pt",
            truncation=True,
            padding=True,
        )

        output = {
            "input": input,
            "output": model(**inputs),
        }

        return output

    except Exception as error:
        print(
            f"❌ Error running job: {error}",
            file=sys.stderr,
            flush=True,
        )
        traceback.print_exc(file=sys.stderr)
        raise


def main():
    print("Starting inference...")

    input = os.environ.get("INPUT", "Default input value")

    # `/app` directory aligns with the `WORKDIR` specified in the `Dockerfile`
    model_directory = "/app/models"

    output = {"input": input, "status": "error"}

    try:
        # TODO: Initialize `model` and `tokenizer`
        # model = AutoModelForSeq2SeqLM.from_pretrained(model_directory)
        # tokenizer = AutoTokenizer.from_pretrained(model_directory)

        output = run_job(input, model, tokenizer)
        output.update(
            {
                "status": "success",
            }
        )

    except Exception as error:
        print("❌ Error during processing:", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        output["error"] = str(error)

    os.makedirs("/outputs", exist_ok=True)
    output_path = "/outputs/result.json"

    try:
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)
        print(
            f"✅ Successfully wrote output to {output_path}",
        )
    except Exception as error:
        print(f"❌ Error writing output file: {error}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)


if __name__ == "__main__":
    main()
