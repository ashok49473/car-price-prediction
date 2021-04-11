from flask import Flask, render_template, request
import pickle
from pandas import DataFrame
from sklearn.base import BaseEstimator

#add NO of years attribute
class AtributeAdder(BaseEstimator):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        temp = X.copy()
        temp.loc[:, 'No_of_Yrs'] = 2021 - X.Year
        temp.drop('Year', axis=1, inplace=True)
        return temp

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
