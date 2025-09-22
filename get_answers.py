from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import pandas as pd
from processing import *

model_name_tokenizer = "facebook/mbart-large-50"
model_name = "Dropdead072/mbart-large-50-spaces"

tokenizer = AutoTokenizer.from_pretrained(model_name_tokenizer)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(
    torch.device("cuda" if torch.cuda.is_available() else "cpu")
)

def predict_spaces(text: str) -> str:
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", max_length=32, truncation=True, padding=True).to(model.device)
    outputs = model.generate(**inputs, max_length=32)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def main() -> None:
    restorer = SpaceRestorer()
    local_path = input("Input the path to the dataset (must be coma separated txt file)\n")
    df_submit = read_and_split_file(local_path)
    df_submit['preprocessed'] = df_submit['text_no_spaces'].apply(restorer.restore_spaces)
    df_submit['predicted_positions'] = df_submit['preprocessed'].apply(predict_spaces)
    df_submit['predicted_positions'] = df_submit['predicted_positions'].apply(find_space_indices)
    df_submit.drop('preprocessed', axis=1, inplace=True)

    save_path = input("Input path to the dir to save the output csv (must be path/name.csv)\n")
    df_submit.to_csv(save_path)
    print('Data saved and ready!')
    return


if __name__=='__main__':
    main()