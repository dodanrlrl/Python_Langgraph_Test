import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from openai import OpenAI

#서버 인스턴스 생성
app = Flask(__name__)

# <엔드 포인트1>: 입력화면(/in) - 서버 첫번째 요청(request)에서 할 일(response)
@app.route('/in') #URL 판독

#response
def input_page():
    return render_template('in.html')



# <엔드 포인트2>: 출력화면(/out) - 서버 두번째 요청(request)에서 할 일(response)
@app.route('/out')

def ouput_page():
    #1. 사용자가 보낸 URL data를 추출
    urls = request.args.get('urls')
    #2. 링크를 분리한 후에
    urls = urls.split('\n')
    urls = list(map(lambda url: url.strip(), urls))
    #3. 뉴스 기사를 가져와서 내용만 추출 하고
    news_contents = []
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        news_contents.append(soup.select_one('#dic_area').text.strip())

    #4. GPT에게 넘겨서 댓글을 만들어 달라고 하고
    client = OpenAI(
     api_key = os.getenv('OPENAI_API_KEY')
    )
    system_msg = '너는 매우 착한 댓글을 만들어주는 AI야. 기사내용을 보고 긍정적인 댓글을 생성해줘'
    user_msgs = news_contents
    comments = []
    # 메세지들 저장
    for user_msg in user_msgs:
        gpt_res = client.responses.create(
          model = 'gpt-4.1-mini',
          # system message
          instructions = system_msg,
          # user message
          input = user_msg
        )
        comments.append(gpt_res.output_text)

    #5. out.html 에 넣어서 보여준다
    results = comments
    return render_template('out.html', results = results)


#서버 돌리기
app.run(debug=True)