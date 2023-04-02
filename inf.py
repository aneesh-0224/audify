from flask import Flask
from flask import Flask, render_template, flash, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import SubmitField
import os
from audio import run


app=Flask(__name__)
app.config['SECRET_KEY']='568325235'

picFolder= os.path.join('static','pics')
app.config['UPLOAD_FOLDER']=picFolder

class audioForm(FlaskForm):
    p_audio = FileField(label='Input an Audio file',validators=[FileAllowed(['wav'])])
    submit = SubmitField(label='Submit')

def save_audio(audio):
    audio_name='target.wav'
    audio_path=os.path.join(app.root_path,'static/input',audio_name)
    audio.save(audio_path)
    return audio_name

@app.route('/',methods=['GET','POST'])
def home_page():
    form = audioForm()
    if form.validate_on_submit():
        try:
            img_file_name=save_audio(form.p_audio.data)
            #calling the model here and saving its result in static/pics
            [audio_list,music_list]=run()
            pics_temp=os.listdir('C:/Users/Aneesh Kulkarni/Desktop/audify/static/pics')
            pics=[]
            for i in range(len(pics_temp)):
                # print(os.listdir('C:/Users/Aneesh Kulkarni/web_dev/flask projects/web page for yolo/static/pics'))
                pics.append(os.path.join(app.config['UPLOAD_FOLDER'],pics_temp[i]))

            print(pics)
            return render_template('show.html',path=app.root_path,user_imgs=pics,length=len(pics),audio_list=audio_list,music_list=music_list)
        except:
            print("wtf")
            flash('Please put in an image in valid format','error')
            return render_template('homepage.html',form=form)

    if(form.p_audio.data is not None):
        flash('Please select an image only','error')  
    return render_template('homepage.html',form=form)

if __name__=="__main__":
    app.run()