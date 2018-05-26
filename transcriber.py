import wave
import audioop
import gspeech

def convert_secs(x):
    secs = x % 60
    x /= 60
    mins = x % 60
    x /= 60
    hrs = x % 24
    return str(hrs) + ":" + str(mins) + ":" + str(secs)

class WAVTranscriber:

    def __init__(self, infile, language="en-IN"):
        # Check format
        fmt = infile[infile.rfind("."):]
        if fmt != ".wav":
            raise AttributeError("File is not in WAVE format")
        self.infile = infile
        self.language = language
        # Open the wave file
        self._wvau = wave.open(infile, "r")
        # Check whether file has proper parameters for Google Speech or not
        channels, sampwidth, framerate, framecount, comptype, compname = self._wvau.getparams()
        if sampwidth != 2:
            raise AttributeError("Sample width is not 16 bit")
        # Set params for transcribing
        self._quantumsize = 30
        self._elapsed = 0
        self._framecount = self._wvau.getnframes()
        self._framesperquantum = (self._quantumsize * self._wvau.getframerate())
        self._duration = int(round(self._framecount / self._wvau.getframerate()))

    def getwavparams(self):
        return self._wvau.getparams()
        
    def getelapsedseconds(self):
        return self._elapsed

    def getquantumsize(self):
        return self._quantumsize

    def getelapsedpercentage(self):
        return float(self._elapsed) / float(self._duration) * 100

    def getduration(self):
        return self._duration

    def __iter__(self):
        return self

    def next(self):
        if self._framecount == 0:
            self._wvau.close()
            raise StopIteration
        lindata = self._wvau.readframes(self._framesperquantum)
        # Convert this data to ulaw
        data = audioop.lin2ulaw(lindata, 2)
        # Transcribe using Google Speech API
        result = gspeech.transcribe_audio(data, self._wvau.getframerate(), self.language, None)
        if self._framecount < self._framesperquantum:
            self._framecount = 0
            timestring = "From " + convert_secs(self._elapsed) + " to " + convert_secs(self._duration) + "\n"
            self._elapsed = self._duration
        else:
            self._framecount -= self._framesperquantum
            timestring = "From " + convert_secs(self._elapsed) + " to " + convert_secs(self._elapsed+self._quantumsize) + "\n"
            self._elapsed += self._quantumsize
        return timestring+result
