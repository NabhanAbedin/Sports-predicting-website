from flask import Flask, jsonify, request, render_template
from Predictor import Predictor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    data = request.get_json()
    predictor = Predictor(data['league'])

    print(f'Recieved Data: {data}')
    print('data:', data['league'])
    

    matches_rolling, predictors, new_cols = predictor.preprocess_data()

    combined, precision = predictor.make_predictions(matches_rolling, predictors + new_cols)

    final_df = predictor.create_final_df(combined,matches_rolling)
    

    df_html = final_df.to_html(classes='table table-stripped', index=False)

    for column in final_df:
        df_html = df_html.replace(f'<td>{column}</td>', 
                          f'<td data-label="{column}">{column}</td>')
        
    for result in ['W', 'D', 'L']:
        df_html = df_html.replace(f'<td>{result}</td>', 
                          f'<td data-value="{result}">{result}</td>')
    
    return jsonify({'wins': str(df_html), 'precision': str(precision)})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)