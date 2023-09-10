import uvicorn, datetime
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

modelName = 'bigscience/bloomz-7b1-mt'

if not os.path.exists('../../.cache'):
    raise ValueError(f'{modelName} is not cached!')


tokenizer = AutoTokenizer.from_pretrained(modelName, cache_dir='../../.cache')
model = AutoModelForCausalLM.from_pretrained(modelName, cache_dir='../../.cache', torch_dtype="auto", device_map="auto")


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


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8993, workers=1)

