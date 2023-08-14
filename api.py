import uvicorn, datetime
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# import torch
# from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
# from accelerate import init_empty_weights, load_checkpoint_and_dispatch

modelAPI = {
    'ChatGLM': 'http://localhost:8991',
    'LLaMA': 'http://localhost:8992',
    'Bloomz': 'http://localhost:8993'
}

dataPath = {
    'D4-Dialogue': '',
    'Case-QA': ''
}


app = FastAPI()

res = {
    'msg': '',
    'code': 200,
    'time': ''
}

# 设置允许跨域请求的来源
origins = [
    "http://49.52.10.178:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/webapi/loadModel')
def load_model(model_a, model_b, data_source):
    response1 = requests.get(f'{modelAPI[model_a]}/index').json()
    if response1['code'] == 200:
        res['msg'] = '模型加载完成'
    else:
        res['code'] = 400
        res['msg'] = '模型加载失败'
    res['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return res


@app.get('/webapi/getRightAnswer')
def get_right_answer(prompt):
    print(prompt)
    response = {
        'msg': '这是参考答案',
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return response


@app.post('/webapi/reWriteAnswer')
async def re_write_answer(request: Request):
    json_raw = await request.json()

    response = {
        'msg': '已经提交完成',
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8990, workers=1)
