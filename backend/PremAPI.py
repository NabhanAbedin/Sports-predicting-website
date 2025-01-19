from flask import Flask, jsonify, request, render_template
from PremierLeaguePred import Predictor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    data = request.get_json()
    predictor = Predictor(data['league'])

    print(f'Recieved Data: {data}')
    print('data:', data['league'])
    
    global matches_rolling, predictors, new_cols
    matches_rolling, predictors, new_cols = predictor.preprocess_data()

    combined, precision = predictor.make_predictions(matches_rolling, predictors + new_cols)

    final_df = predictor.create_final_df(combined,matches_rolling)
    df_html = final_df.to_html(classes='table table-stripped', index=False)
    
    return jsonify({'wins': str(df_html)})

    #return render_template('soccerPrediction.html', table=df_html)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=80)