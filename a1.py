import spade
import time
import RPi.GPIO as GPIO
import os
from os import path
import speech_recognition as sr

wavFile = path.join(path.dirname(path.realpath(__file__)), "record.wav")

D1 = 15 
D2 = 18

I1 = 23
I2 = 24

r = sr.Recognizer()


class MasterCrack(spade.Agent.Agent):
	standby=True

	class MyBehav(spade.Behaviour.Behaviour):
		receiver = spade.AID.aid(name="tempus@127.0.0.1", addresses=["xmpp://tempus@127.0.0.1"])
		#pal2="inicio"
		def onStart(self):
			print "Starting MyBehav . . ."
			self.counter = 0

		def _process(self):			
			os.system("timeout 4 sox -t alsa default ./record.wav")
			with sr.WavFile(wavFile) as source:
				audio = r.record(source)
						
			try:				
				palabra=r.recognize_google(audio, language = "es-GT").lower()
				print("Google Speech Recognition thinks you said " + palabra)				
				if "comencemos" in palabra:
					os.system("play ./Respuesta_Inicio.wav")
					print "saliendo de stand by, empezando a contar tiempo..."
					self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message					
					self.msg.addReceiver(self.receiver)            # Add the message receiver
					self.msg.setContent("inicio")        # Set the message content										
					self.myAgent.send(self.msg)
					#self.myAgent.standby=False
					#print "standby = " + self.myAgent.standby
					#self.pal2="asdf"
				else:
					if "embestir" in palabra or "escapar" in palabra or "confusi" in palabra:
						self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message					
						self.msg.addReceiver(self.receiver)            # Add the message receiver
						self.msg.setContent("moviendo")
						self.myAgent.send(self.msg)
						if "embestir" in palabra:
							os.system("play ./Respuesta_Acercamiento.wav")
							i = GPIO.PWM(I1,10)
							d = GPIO.PWM(D1,10)
							i.start(80)
							d.start(80)
							time.sleep(1)
							i.stop()
							d.stop()											
						if "escapar" in palabra:
							os.system("play ./Respuesta_Huida.wav")
							#Ahora si escapa
							i = GPIO.PWM(I1,8)
							d = GPIO.PWM(D2,8)
							i.start(80)
							d.start(80)
							time.sleep(1)
							i.stop()
							d.stop()
							time.sleep(1)
							i = GPIO.PWM(I2,10)
							d = GPIO.PWM(D2,10)
							i.start(80)
							d.start(80)
							time.sleep(1)
							i.stop()
							d.stop()													
						if "confusi" in palabra:
							os.system("play ./Respuesta_Panico.wav")
							i = GPIO.PWM(I1,10)
							d = GPIO.PWM(D2,10)
							i.start(80)
							d.start(80)
							time.sleep(2)
							i.stop()
							d.stop()
					else:
						os.system("play ./Error.wav")
						print "El robot no entiende "+ palabra
			except sr.UnknownValueError:
				print("Google Speech Recognition no entiende")
			except sr.RequestError as e:
				print("No funciono nada; {0}".format(e))
			
			time.sleep(2)
			
	class ReceiveBehav(spade.Behaviour.Behaviour):
		"""receptor de mensajes"""
		contador = 0
		receiver = spade.AID.aid(name="tempus@127.0.0.1", addresses=["xmpp://tempus@127.0.0.1"])
		
		def _process(self):
			self.msg = None
			# Blocking receive for 10 seconds
			self.msg = self._receive()
			# Check wether the message arrived
			if self.msg == None:
				print "no me llego nada"
			else:
				if self.msg.content=="standby":
					#self.myAgent.standby=True
					print "standby: "+ self.myAgent.standby
				#print "llego: "+self.msg.content
			time.sleep(5)

	def _setup(self):
		print "MasterCrack starting . . ."
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		GPIO.setup(D1,GPIO.OUT)
		GPIO.setup(D2,GPIO.OUT)
		
		GPIO.setup(I1,GPIO.OUT)
		GPIO.setup(I2,GPIO.OUT)
		rb = self.ReceiveBehav()
		mb = self.MyBehav()
		self.setDefaultBehaviour(mb)
		self.addBehaviour(rb,None)

if __name__ == "__main__":
	a = MasterCrack("master@127.0.0.1", "secret")
	a.start()
