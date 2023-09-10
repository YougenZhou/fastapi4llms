import uvicorn, datetime, os
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
from utils import format_example

modelName = 'THUDM/chatglm-6b'

if not os.path.exists('../../.cache'):
    raise ValueError(f'{modelName} is not cached.')

tokenizer = AutoTokenizer.from_pretrained(modelName, cache_dir='../../.cache', trust_remote_code=True)
model = AutoModel.from_pretrained(modelName, cache_dir='../../.cache', trust_remote_code=True).cuda()


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

@app.get('/submitInput')
async def submit_input(requests: Request):
    json_raw = await requests.json()
    input_text = json_raw['inputText']
    prompt, history, target = format_example('ChatGLM', input_text)
    response, _ = model.chat(tokenizer, prompt, history=history)




if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8991, workers=1)

