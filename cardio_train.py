from zeroone_ai import MLPRegressor

dataset = 'cardio_train.csv'
input_data = ['age','gender','height','weight','ap_hi','ap_lo','cholesterol','gluc','smoke','alco','active']
label = 'cardio'
model = MLPRegressor(dataset,input_data,label)

hidden_layer_sizes = [20,20,10]
model.train(hidden_layer_sizes)

print(model.accuracy())

length = 20
model.plot(length)