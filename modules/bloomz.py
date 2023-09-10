import uvicorn, datetime
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

modelName = 'bigscience/bloomz-7b1-mt'

if not os.path.exists('../../.cache'):
    raise ValueError(f'{modelName} is not cached!')


tokenizer = AutoTokenizer.from_pretrained(modelName, cache_dir='../../.cache')
model = AutoModelForCausalLM.from_pretrained(modelName, cache_dir='../../.cache', torch_dtype="auto", device_map="auto")


def bloom_example(raw_data):
    inputs, target = raw_data[:-1], raw_data[-1]
    prompt = '你是一个中文心理咨询自动化助手，下面是一些关于心理诊断的真是对话，你将通过提问引导对患者进行诊断。'
    for utterance in inputs:
        prompt += utterance['speaker'] + '：' + utterance['content']
    prompt += target['speaker'] + '：'
    return prompt, target


app = FastAPI()

res = {
    'msg': '',
    'code': 200,
    'time': ''
}


@app.get('/index')
async def index():
    if model:
        res['msg'] = '模型加载完成'
    else:
        res['msg'] = '模型加载失败'
        res['code'] = 400
    res['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return res


@app.post('/submitInput')
async def submit_input(requests: Request):
    json_raw = await requests.json()
    input_text = json_raw['inputText']
    prompt, target = bloom_example(input_text)
    prompt = tokenizer.encode(prompt, return_tensor='pt').to('cuda')
    max_new_token = 256
    response = model.generate(prompt, do_sample=True, temperature=0.2, top_p=0.8, max_new_tokens=max_new_token)
    response = tokenizer.decode(response[0])
    response_str = response.split('doctor：')[-1].strip('</s>')
    res['data'] = {'answer': response_str}
    return res


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8993, workers=1)

