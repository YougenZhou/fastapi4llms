import uvicorn, datetime
import requests

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# 设置允许跨域请求的来源
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",  # 如果需要，可以添加更多允许的来源
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/')
async def load_model(request: Request):
    json_post_raw = await request.json()
    print(json_post_raw)

    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    }
    answer = requests.post('http://101.132.187.81:5000/chat', headers=headers, json=json_post_raw).text

    print(answer)

    response = {
        'response': answer,
        'status': 200,
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return response


@app.get('/webapi/loadModel')
async def load_model(model_name, param_size):
    print(model_name, param_size)
    response = {
        'msg': '模型加载完成',
        'status': 200
    }
    return response

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=994, workers=1)
