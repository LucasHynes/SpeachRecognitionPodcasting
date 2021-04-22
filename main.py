import speech_recognition as sr
import pydub
pydub.AudioSegment.ffmpeg = "C:/FFmpeg"
import os
import chunkMusic
import team_setter
import pandas as pd
import players as p

basepath = "SpeachRecognitionPodcasting/"

def match_team(team, line_to_check):
    return any(item in line_to_check for item in team[1])
    
def count_true(results):
    count = 0
    for i in results:
        if i == True:
            count+=1
    return count

with os.scandir(basepath) as entries:
    for item in entries:
        if(item.name.endswith(".mp3")):
            src = basepath + item.name
            
            #sound = pydub.AudioSegment.from_mp3(src)
            #sound.export("audio/{0}".format(item.name).split(".")[0] + ".wav", format="wav")

            AUDIO_FILE = "audio/{0}.wav".format(item.name.split(".")[0])

            teams = team_setter.get_teams()

            counter = {
                'Team': teams,
                'Num_words': [0 for i in range(len(teams))],
                'Checking': [False for i in range(len(teams))]
            }
            
            data = pd.DataFrame(counter, columns=['Team','Num_words','Checking'])
            
            count = chunkMusic.main(pydub.AudioSegment.from_file(AUDIO_FILE), AUDIO_FILE.split('.')[0].split('/')[1])

            for i in range(count):
                r = sr.Recognizer()
                with sr.AudioFile(AUDIO_FILE.split(".")[0] + "_" + str(i) + ".wav") as source:
                    audio = r.record(source)

                    result = (r.recognize_google(audio))
                    print(result)
                    result = result.split()

                    for team_count in range(len(teams)):
                        for word in result:
                        
                            if word in (data['Team'].tolist())[team_count][1] or word in p.dict_players[" ".join(teams[team_count][0].split(" ")[:-1])]:
                                data.at[team_count, 'Checking'] = True
                                data.at[team_count, 'Num_words'] += 1
                            elif data.at[team_count, 'Checking']:
                                if count_true(data['Checking'].tolist()) > 1:
                                    data.at[team_count, 'Checking'] = False
                                else:
                                    data.at[team_count, 'Num_words'] += 1


                    print("Done with file {0} of {1}".format(i, count))
                data.to_csv("test.csv".format(i))