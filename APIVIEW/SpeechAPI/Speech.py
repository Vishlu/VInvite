# import speech_recognition as sr
# import pyttsx3

# # Initialize the recognizer
# r = sr.Recognizer()

# # Function to convert text to
# # speech
# def SpeakText(command):
	
# 	# Initialize the engine
# 	engine = pyttsx3.init()
# 	engine.say(command)
# 	engine.runAndWait()
	
	
# # Loop infinitely for user to
# # speak

# while(True):
	
# 	# Exception handling to handle
# 	# exceptions at the runtime
# 	try:
		
# 		# use the microphone as source for input.
# 		with sr.Microphone() as source2:
			
# 			# wait for a second to let the recognizer
# 			# adjust the energy threshold based on
# 			# the surrounding noise level
# 			r.adjust_for_ambient_noise(source2)
			
# 			#listens for the user's input
# 			audio2 = r.listen(source2)
			
# 			# Using google to recognize audio
# 			MyText = r.recognize_google(audio2)
# 			MyText = MyText.lower()

# 			print("Did you say ",MyText)
# 			SpeakText(MyText)
			
# 	except sr.RequestError as e:
# 		print("Could not request results; {0}".format(e))
		
# 	except sr.UnknownValueError:
# 		print("unknown error occurred")





# import speech_recognition as sr

# # Initialize recognizer class (for recognizing the speech)

# r = sr.Recognizer()

# # Reading Microphone as source
# # listening the speech and store in audio_text variable

# with sr.Microphone() as source:
#     print("Talk")
#     audio_text = r.listen(source)
#     print("Time over, thanks")
# # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    
#     try:
#         # using google speech recognition
#         print("Text: "+r.recognize_google(audio_text))
#     except:
#          print("Sorry, I did not get that")


# import speech_recognition as sr

# r = sr.Recognizer()

# with sr.Microphone() as source:
# 	print("Speak: ")
# 	user_text = r.listen(source)
# 	print("Time over")
# 	speak = r.recognize_google(user_text)
# 	print(speak)


import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.say("hello vishal ")
engine.runAndWait()