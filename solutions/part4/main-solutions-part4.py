import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
tracer = trace.get_tracer(__name__)

from flask import Flask, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/test')
def test_it():
    return 'OK'

@app.route('/check')
@tracer.start_as_current_span("credit_check")
def credit_check():
    customerNum = request.args.get('customernum')
    
    # Get Credit Score
    creditScoreReq = requests.get("http://creditprocessorservice:8899/getScore?customernum=" + customerNum)
    creditScore = int(creditScoreReq.text)
    creditScoreCategory = getCreditCategoryFromScore(creditScore)

    # Run Credit Check
    creditCheckReq = requests.get("http://creditprocessorservice:8899/runCreditCheck?customernum=" + str(customerNum) + "&score=" + str(creditScore))
    checkResult = str(creditCheckReq.text)

    return checkResult

@tracer.start_as_current_span("credit_score")
def getCreditCategoryFromScore(score):
    current_span = trace.get_current_span()
    creditScoreCategory = ''
    match score:
        case num if num > 850:
            creditScoreCategory = 'impossible'
        case num if 800 <= num <= 850 :
            creditScoreCategory = 'exceptional'
        case num if 740 <= num < 800 :
            creditScoreCategory = 'very good'
        case num if 670 <= num < 740 :
            creditScoreCategory = 'good'
        case num if 580 <= num < 670 :
            creditScoreCategory = 'fair'
        case num if 300 <= num < 580 :
            creditScoreCategory = 'poor'
        case _:
            creditScoreCategory = 'impossible'
    current_span.set_attribute("creditScoreCat", (creditScoreCategory))
    return creditScoreCategory

if __name__ == '__main__':
    serve(app, port=8888)