from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

# method=get (ex> ?filter=강남구)
@app.route('/demo')
def read_excel():
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import font_manager, rc

    font_path = "static/gulim.ttc"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    file_path = "static/sample.xlsx"
    df = pd.read_excel(file_path, engine='openpyxl')
    df.dropna(subset=['소재지전체주소'], axis=0, inplace=True)

    select = request.args.get('filter', default = "*", type = str)
    
    def select_gu(x, a):
        k = x.split(' ')
        if k[1] == a:
            return True
        else:
            return False

    mask = df['소재지전체주소'].apply(select_gu, a=select)
    df_data = df.loc[mask, :]

    def select_gu(x):
        a = x.split(' ')
        return a[2]

    df_data = df_data['소재지전체주소'].apply(select_gu)
    df_count = df_data.value_counts()
    #print(df_count)
    
    plt.style.use('fast')
    plt.figure(figsize=(16, 10))
    plt.bar(df_count.index, df_count.values)
    plt.title("서울시 "+select+"내 동별 통닭집 현황")

    plt.savefig('static/c'+select+'.png') # save .png
    return render_template('chart.html', name="서울시 "+select+"내 동별 통닭집 현황", url='static/c'+select+'.png')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # threaded=True: multiple plot available
    app.run(port='5000', threaded=True)
