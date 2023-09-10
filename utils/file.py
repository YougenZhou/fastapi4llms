import json
import pandas as pd


def read_json(data_path):
    with open(data_path, 'r', encoding='utf-8') as data_file:
        raw_data = json.load(data_file)
        data_file.close()
    return raw_data


def read_csv(data_path):
    return pd.read_csv(data_path)


def save_csv(csv, data_path):
    csv.to_csv(data_path)


def format_example(model, raw_data):
    if model not in ['ChatGLM', 'LLaMA', 'Bloom', 'ChatGPT']:
        raise ValueError(f'{model} is unknown model.')
    if model == 'ChatGLM':
        return chatglm_example(raw_data)


def chatglm_example(raw_data):
    inputs, target, prompt = raw_data[:-2], raw_data[-1], raw_data[-2]
    history = [('你是一个中文心理咨询自动化助手，下面是一些关于心理诊断的真实对话，你将通过提问引导对患者进行诊断。',
                '好的，我会通过提问对用户进行心理诊断。')]
    h = []
    for utterance in inputs:
        if utterance['speaker'] == 'patient':
            h.append(utterance['content'])
        else:
            h.append(utterance['content'])
            history.append((h[0], h[1]))
            h = []
    return prompt['content'], history, target
