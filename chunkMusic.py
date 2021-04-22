from pydub.utils import make_chunks

def main(myaudio, filename):
        
        chunks = make_chunks(myaudio, 50000)

        #Export all of the individual chunks as wav files

        for i, chunk in enumerate(chunks):
            chunk_name = "audio/{1}_{0}.wav".format(i, filename)
            print ("exporting " + chunk_name)
            chunk.export(chunk_name, format="wav")
        
        return len(chunks)