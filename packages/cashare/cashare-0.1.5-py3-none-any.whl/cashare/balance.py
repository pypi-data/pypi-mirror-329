from cashare.common.dname import url1

from cashare.common.get_data import _retry_get
def balance(sk_code,token,period='annual'):
    li = handle_url(sk_code=sk_code,token=token,period=period)
    r =_retry_get(li,timeout=100)
    return r

def handle_url(sk_code,period,token):
    g_url=url1+'/balance/'+sk_code+'/'+period+'/'+token
    # print(g_url)
    return g_url
if __name__ == '__main__':
    df = balance(sk_code='AAPL',token='se1e7c9f1de6f161970e05ed1c10dfd2838')
    # df.to_csv('balance.csv')
    print(df)
    pass




