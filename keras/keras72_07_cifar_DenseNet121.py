# 실습
# cifar10과 cifar100 으로 모델을 만들것
# Trainable=True, False
# FC로 만든것과 Avarge Pooling으로 만들것 비교

# 결과출력
# 1. cifar 10
# trainable = True, FC : loss=?, acc=?
# trainable = True, pool : loss=?, acc=?
# trainable = False, FC : loss=?, acc=?
# trainable = False, pool : loss=?, acc=?

# 1. cifar 100
# trainable = True, FC : loss=?, acc=?
# trainable = True, pool : loss=?, acc=?
# trainable = False, FC : loss=?, acc=?
# trainable = False, pool : loss=?, acc=?

from tensorflow.keras.datasets import cifar10, cifar100
from tensorflow.keras.applications import DenseNet121
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D
import time

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

ecd = OneHotEncoder()
y_train = ecd.fit_transform(y_train).toarray()
y_test = ecd.fit_transform(y_test).toarray()

denseNet121 = DenseNet121(weights='imagenet', include_top=False, input_shape=(32,32,3))
denseNet121.trainable = True

model = Sequential()
model.add(denseNet121)
model.add(GlobalAveragePooling2D())
# model.add(Flatten())
model.add(Dense(10, activation='softmax'))

model.summary()

from tensorflow.keras.callbacks import EarlyStopping

es = EarlyStopping(monitor='val_loss', mode='auto', patience=5)

start_time = time.time()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
model.fit(x_train, y_train, epochs=100, batch_size=32, validation_split=0.25, verbose=1, callbacks=[es])
end_time = time.time() - start_time

loss, acc = model.evaluate(x_test, y_test)

print("loss :", loss)
print("acc :", acc)
print("걸린 시간 :", end_time)

'''
cifar 10
FC/trainable : False
loss :  1.2393006086349487 accuracy :  0.5717999935150146
GAP/trainable : False
loss :  1.2407950162887573 accuracy :  0.5705000162124634
FC/trainable : True
loss :  0.6601503491401672 accuracy :  0.8762000203132629
GAP/trainable : True
loss :  0.7333699464797974 accuracy :  0.8772000074386597
cifar100
FC/trainable : False
loss :  2.9139232635498047 accuracy :  0.28600001335144043
GAP/trainable : False
loss :  2.9828567504882812 accuracy :  0.2597000002861023
FC/trainable : True
loss :  2.069634199142456 accuracy :  0.5989000201225281
GAP/trainable : True
loss :  2.1894586086273193 accuracy :  0.635699987411499
'''