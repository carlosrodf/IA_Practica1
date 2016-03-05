import spade
import time

class Tempus(spade.Agent.Agent):
	class ReceiveBehav(spade.Behaviour.Behaviour):
		"""This behaviour will receive all kind of messages"""
		contador = 0
		receiver = spade.AID.aid(name="master@127.0.0.1", addresses=["xmpp://master@127.0.0.1"])

		def _setup(self):
			print "iniciando"

		def _process(self):
			self.msg = None			
			self.msg = self._receive()			
			if self.msg == None:
				#print "no me llego nada"
				self.contador = self.contador + 2
				if self.contador == 30:
					print "espera"
					self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
					self.msg.setPerformative("inform")        # Set the "inform" FIPA performative
					self.msg.setOntology("myOntology")        # Set the ontology of the message content
					self.msg.setLanguage("OWL-S")	          # Set the language of the message content
					self.msg.addReceiver(self.receiver)            # Add the message receiver
					self.msg.setContent("espera")        # Set the message content
			
					# Third, send the message with the "send" method of the agent
					self.myAgent.send(self.msg)	
				else:
					if self.contador == 60:
						print "standby"
						self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
						self.msg.setPerformative("inform")        # Set the "inform" FIPA performative
						self.msg.setOntology("myOntology")        # Set the ontology of the message content
						self.msg.setLanguage("OWL-S")	          # Set the language of the message content
						self.msg.addReceiver(self.receiver)            # Add the message receiver
						self.msg.setContent("standby")        # Set the message content
			
						# Third, send the message with the "send" method of the agent
						self.myAgent.send(self.msg)	

					else:
						print self.contador
			else:
				print "si me llego algo: "+ self.msg.content
				self.contador = 0
			time.sleep(2)
			
		
	def _setup(self):
		# Add the "ReceiveBehav" as the default behaviour
		rb = self.ReceiveBehav()
		self.setDefaultBehaviour(rb)				

if __name__ == "__main__":
	a = Tempus("tempus@127.0.0.1", "secret")
	a.start()
