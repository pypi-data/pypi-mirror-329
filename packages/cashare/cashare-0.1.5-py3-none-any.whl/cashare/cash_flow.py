from cashare.common.dname import url1

from cashare.common.get_data import _retry_get
def cash_flow(sk_code,token,period='annual'):
    li = handle_url(sk_code=sk_code,period=period,token=token)
    r =_retry_get(li,timeout=100)
    return r

def handle_url(sk_code,period,token):
    g_url=url1+'/cash_flow/'+sk_code+'/'+period+'/'+token
    # print(g_url)
    return g_url
if __name__ == '__main__':
    df = cash_flow(sk_code='AAPL',period='annual',token='se1e7c9f1de6f161970e05ed1c10dfd2838')
    # df.to_csv('cash_flow.csv')
    print(df)
    pass




