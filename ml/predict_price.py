import sklearn
import sys
import pickle

def predict_price(pred_dist, pred_date, pred_beds, pred_baths):
    # load the model from disk
    filename = 'finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    loaded_model.predict([[pred_dist, pred_date, pred_beds, pred_baths]])

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    predict_price(*sys.argv[1:])