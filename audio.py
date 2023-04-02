
def run():
    import numpy as np

    # pd.plotting.register_matplotlib_converters()
    import matplotlib.pyplot as plt

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, Dropout

    import tensorflow as tf
    import librosa
    import librosa.display

    input_dim = (16, 8, 1)

    model = Sequential()
    model.add(Conv2D(64, (3, 3), padding = "same", activation = "tanh", input_shape = input_dim))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Conv2D(128, (3, 3), padding = "same", activation = "tanh"))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))
    model.add(Flatten())
    model.add(Dense(1024, activation = "tanh"))
    model.add(Dense(10, activation = "softmax"))

    model.load_weights('audify_weights.hdf5')

    sound=['air_conditioner','car_horn','children_playing','dog_bark','drilling','engine_idling','gun_shot','jackhammer','siren','street_music']
    genre_arr=['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

    filename='C:/Users/Aneesh Kulkarni/Desktop/audify/static/input/target.wav'
    x, sample_rate = librosa.load(filename, res_type='kaiser_fast') 
    mels_specific = np.mean(librosa.feature.melspectrogram(y=x, sr=sample_rate).T,axis=0)
    img=librosa.amplitude_to_db(np.abs(librosa.stft(x)), ref=np.max)
    ans=librosa.display.specshow(img, y_axis='linear')
    plt.savefig("static/pics/out.jpg")
    plt.show()

    single_in=mels_specific.reshape(1,16,8,1)
    audio_list=[]
    pred2=model.predict(single_in)
    print(pred2.shape)
    print(sound[np.argmax(pred2)])
    f=0
    for i,s in enumerate(pred2[0]):
        print(i,s)
        if(s>1e-4):
            if(sound[i]=='street_music'):
                f=1
            audio_list.append(sound[i])

    # audio_list.append(sound[np.argmax(pred2)])
    music_list=[]

    if(f==1):
        model_genre = Sequential()
        model_genre.add(Conv2D(64, (3, 3), padding = "same", activation = "tanh", input_shape = input_dim))
        model_genre.add(MaxPool2D(pool_size=(2, 2)))
        model_genre.add(Conv2D(128, (3, 3), padding = "same", activation = "tanh"))
        model_genre.add(MaxPool2D(pool_size=(2, 2)))
        model_genre.add(Dropout(0.1))
        model_genre.add(Flatten())
        model_genre.add(Dense(1024, activation = "tanh"))
        model_genre.add(Dense(10, activation = "softmax"))

        model_genre.load_weights('audify_weights_genre.hdf5')
        genre_pred=model_genre.predict(single_in)
        print(genre_arr[np.argmax(genre_pred)])
        music_list.append(genre_arr[np.argmax(genre_pred)])
    
    print(audio_list,music_list)
    return [audio_list,music_list]

run()