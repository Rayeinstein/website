import pickle

Desktop="/Users/QTD0277/Desktop/"
Save_file="g_logs.pkl"

def pickle_load(filename):
	"loads data from a desktop pickle file. returns the data"
	with open(Desktop+filename,'rb') as f:  # Python 3: open(..., 'rb')
	    loaded = pickle.load(f)
	    print("loaded data from: ",filename)
	return loaded

#data=pickle_load(Save_file)
