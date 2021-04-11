from flask import Flask, render_template, request
import pickle
from pandas import DataFrame
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from feature_engine.encoding import OneHotEncoder
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.preprocessing import MinMaxScaler

###########################################################################################
#preprocessing pipeline
cat_features=['Fuel_Type', 'Seller_Type', 'Transmission']

pipe = Pipeline(steps=[
    
    ('one hot encoder', OneHotEncoder(variables=cat_features)),
    
    ('min max scaler', SklearnTransformerWrapper( variables = ['Kms_Driven'],
                                                 transformer=MinMaxScaler(feature_range=(0, 100) ) ) )
    
])
###########################################################################################
with open("pipe.pkl", "rb") as f:
	preprocessor = pickle.load(f)

with open("best_model.pkl", "rb") as f:
    model = pickle.load(f)
    
def predict_price(ex):
    columns = ['Year','Present_Price','Kms_Driven','Fuel_Type','Seller_Type', 'Transmission','Owner']
    df = DataFrame([ex], columns=columns)
    x = preprocessor.transform(df)
    y = model.predict(x)
    return round(y[0],2)
###################################################################################
app = Flask(__name__)

######################################################
@app.route("/", methods=['GET'])
def home():
   return render_template("home.html")

#######################################################
@app.route("/result", methods = ["GET","POST"])
def predict():
	if request.method == 'POST':
		Year = int(request.form.get('year'))
		Year = 2021 - Year
		Present_Price = float(request.form.get('pr_price'))
		Kms_Driven = float(request.form.get('kms'))
		Fuel_Type = request.form.get('fuel')
		Seller_Type = request.form.get('seller')
		Transmission = request.form.get('trans')
		Owner = int(request.form.get('owner'))

		x = [Year, Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner]
		y = predict_price(x)

		return render_template("result.html", price = y)
	else:
		return render_template("home.html")

#######################################################
if __name__ == '__main__':
	app.run(debug=True)
