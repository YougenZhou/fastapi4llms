import uvicorn, datetime
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# import torch
# from transformers import AutoConfig, AutoTokenizer, AutoModelForCausalLM
# from accelerate import init_empty_weights, load_checkpoint_and_dispatch


MODEL_PATH = {
    'ChatGLM-6B': 'ChatGLM',
    'LLaMA-7B': 'LLaMA'
}

tokenizer = None
model = None


def _init(num_gpus, model_name):
    global tokenizer, model

    model_path = MODEL_PATH[model_name]
    # config = AutoConfig.from_pretrained(model_path, cache_dir='./packages')
    # tokenizer = AutoTokenizer.from_pretrained(model_path, cache_dir='./packages')
    tokenizer = model_path

    if num_gpus > 1:
        # with init_empty_weights():
        #     raw_model = AutoModelForCausalLM._from_config(config, torch_dtype=torch.float16)
        # raw_model.tie_weights()
        # model = load_checkpoint_and_dispatch(
        #     raw_model, model_path, device_map="auto", no_split_module_classes=["MossBlock"], dtype=torch.float16
        # )
        pass
    else:  # on a single gpu
        # model = AutoModelForCausalLM.from_pretrained(model_path).half().cuda()
        model = model_path


app = FastAPI()

# 设置允许跨域请求的来源
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/webapi/getAnswer')
async def get_answer(request: Request):
    json_raw = await request.json()

    response = {
        'msg': '模型的回复',
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return response


@app.get('/webapi/loadModel')
async def load_model(model_name, param_size):
    response = {
        'msg': '',
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    model_name = model_name + '-' + param_size
    if model_name not in MODEL_PATH:
        response['msg'] = '模型不存在！'
        response['status'] = 500
    else:
        model_path = MODEL_PATH[model_name]
        model = model_path

        response['msg'] = model_name + '已加载完成！'
        response['status'] = 200

    return response


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
    _init(1, 'ChatGLM-6B')
    uvicorn.run(app, host='0.0.0.0', port=994, workers=1)
