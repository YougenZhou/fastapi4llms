import uvicorn, datetime, os
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel

modelName = 'THUDM/chatglm-6b'

if not os.path.exists('../../.cache'):
    raise ValueError(f'{modelName} is not cached.')

tokenizer = AutoTokenizer.from_pretrained(modelName, cache_dir='../../.cache', trust_remote_code=True)
model = AutoModel.from_pretrained(modelName, cache_dir='../../.cache', trust_remote_code=True).half().cuda()


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
    prompt, history, target = chatglm_example(input_text)
    response, _ = model.chat(tokenizer, prompt, history=history)
    res['data'] = {'answer': response}
    return res


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8991, workers=1)

