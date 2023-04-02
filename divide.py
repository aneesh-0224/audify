from pydub import AudioSegment
t1 =0 #Works in milliseconds
t2 =3000
newAudio = AudioSegment.from_wav("101848-9-0-3.wav")
newAudio = newAudio[t1:t2]
newAudio.export('newSong.wav', format="wav")