import uvicorn, datetime
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from utils import read_json, read_csv, save_csv

modelAPI = {
    'ChatGLM': 'http://localhost:8991',
    'LLaMA': 'http://localhost:8992',
    'Bloomz': 'http://localhost:8993',
    'ChatGPT': 'http://localhost:8894'
}

dataPath = {
    'D4-Dialogue': './data/d4/raw_data.json',
    'Case-QA': ''
}

modelGroup = {
    'ChatGLMLLaMA': 1,
    'LLaMAChatGLM': 1,
    'ChatGLMBloomz': 2,
    'BloomzChatGLM': 2,
    'ChatGLMChatGPT': 3,
    'ChatGPTChatGLM': 3,
    'LLaMABloomz': 4,
    'BloomzLLaMA': 4,
    'LLaMAChatGPT': 5,
    'ChatGPTLLaMA': 5,
    'BloomzChatGPT': 6,
    'ChatGPTBloomz': 6
}

user = 'zyg'
process = None


app = FastAPI()

res = {
    'msg': '',
    'code': 200,
    'time': ''
}

# 设置允许跨域请求的来源
origins = [
    "*",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('webapi/login')
def login(user_name, password):
    user_list = read_csv()


@app.get('/webapi/loadModel')
def load_model(model_a, model_b, data_source):
    response1 = requests.get(f'{modelAPI[model_a]}/index').json()
    response2 = requests.get(f'{modelAPI[model_b]}/index').json()

    data_path = dataPath[data_source]
    raw_data = read_json(data_path)

    process = read_csv('./outputs/process.csv')
    process_id = process[process['username'] == user]['process_id'].item()
    res['data'] = raw_data[process_id]

    if response1['code'] == 200 and response2['code'] == 200 and raw_data:
        res['msg'] = '模型加载完成'
    else:
        res['code'] = 400
        res['msg'] = '模型加载失败'
    res['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return res


@app.get('/webapi/nextIndex')
def next_index():

    data_source = process[process['username'] == user]['process_item'].item()
    data_path = dataPath[data_source]
    raw_data = read_json(data_path)

    process_id = process[process['username'] == user]['process_id'].item() + 1
    res['data'] = raw_data[process_id]

    process.loc[process['username'] == user, 'process_id'] = process_id
    save_csv(process, './outputs/process.csv')
    return res


@app.post('/webapi/submitInput')
async def submit_input(request: Request):
    json_raw = await request.json()
    session = read_csv('./outputs/session.csv')
    session = session[session['userName'] == user]
    modelAnswer1 = requests.post(f'{modelAPI[session["model1"].item()]}/submitInput', json=json_raw).json()
    modelAnswer2 = requests.post(f'{modelAPI[session["model2"].item()]}/submitInput', json=json_raw).json()
    print(modelAnswer1)
    res['data'] = {
        'answer1': modelAnswer1,
        'answer2': modelAnswer2
    }
    return res


@app.post('/webapi/submitResult')
async def re_write_answer(request: Request):
    json_raw = await request.json()
    model_group = json_raw['modelA'] + json_raw['modelB']
    model_group = modelGroup[model_group]
    print(model_group)
    response = {
        'msg': '已经提交完成',
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8990, workers=1)
