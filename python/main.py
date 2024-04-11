import kivy
import time
kivy.require("2.2.1")
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
class B1(Button):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.font_name = "font/font1.ttf"
		self.font_size = 35
class L1(Label):
	def __init__(self, **kwargs):
		self.clr = kwargs.pop('clr', (1, 1, 1, 1))
		super().__init__(**kwargs)
		self.font_name = "font/font1.ttf"
		self.font_size = 55
		with self.canvas.before:
			Color(*self.clr)
			self.rect = Rectangle(size=self.size, pos=self.pos)
	def on_size(self, *args):
		self.rect.size = self.size
		self.rect.pos = self.pos
	def on_pos(self, *args):
		self.rect.pos = self.pos
class main(App):
	def build(self):
		self.TC = lambda n: " : ".join([f"{int(n/60):02d}", f"{int(n%60):02d}", "{:.2f}".format(round(n%60, 2))[-2:]])
		self.event1 = None
		self.timer: list = [300, 300]
		self.tcc:   list = [0, 0]
		self.rt     = [[0, 0], 300]
		self.switch = [0, 0, [0, [60, 1, 60, 1], 0]]
		self.mode   = 0
		self.now    = 0
		self.btn    = ["play", "restart", "setting"]
		self.sound  = [SoundLoader.load('sound/niko.wav'), SoundLoader.load('sound/hhhh.wav')]
		self.G1 = GridLayout(rows=2)
		self.G1_1 = GridLayout(rows=2, size_hint=(1, .85))
		self.G1_2 = GridLayout(cols=3, size_hint=(1, .15))
		self.G1_1_1 = GridLayout(cols=2, size_hint=(1, .90))
		
		self.G1_1_2 = GridLayout(cols=3, size_hint=(1, .10))
		self.b1_1_1 = B1(text="White", size_hint=(1, .825), on_press=lambda *args:self.b1_pressed(1), disabled=True)
		self.b1_1_2 = B1(text="Black", size_hint=(1, .825), on_press=lambda *args:self.b1_pressed(0), disabled=True)
		self.l1_1_1 = L1(text=self.TC(self.timer[0]), size_hint=(.45, 1), color = (0, 0, 0, 1))
		self.l1_1_2 = L1(text=self.TC(self.timer[1]), size_hint=(.45, 1), clr=(0, 0, 0, 1))
		self.l1_1_3 = L1(text=str(self.mode), size_hint=(.1, .175), clr=(.5, .5, .5, 1), color = (0, 1, .3, 1))
		self.buttons = [self.b1_1_1, self.b1_1_2]
		self.labels  = [self.l1_1_1, self.l1_1_2]
		for n in (self.b1_1_1, self.b1_1_2): self.G1_1_1.add_widget(n)
		for n in (self.l1_1_1, self.l1_1_3, self.l1_1_2): self.G1_1_2.add_widget(n)
		for n in (self.G1_1_1, self.G1_1_2): self.G1_1.add_widget(n)
		self.b2_1 = B1(text="<<", on_press=lambda *args: self.move(0))
		self.b2_2 = B1(text="play", on_press=self.logics)
		self.b2_3 = B1(text=">>", on_press=lambda *args: self.move(1))
		for n in (self.b2_1, self.b2_2, self.b2_3):
			self.G1_2.add_widget(n)
		self.G1.add_widget(self.G1_1)
		self.G1.add_widget(self.G1_2)
		return self.G1
	def b_setting1(self, *args):
		self.b2_1.disabled = args[0]
		self.b2_3.disabled = args[1]
	def b_setting2(self, *args):
		self.b1_1_1.disabled = args[0]
		self.b1_1_2.disabled = args[1]
	def logics(self, *args):
		if self.rt[1] == 300:
			self.b1_1_1.disabled = False
		if self.b2_2.text == "play":
			self.now = time.time()
			print(self.rt)
			self.rt = [[self.rt[0][0], self.rt[0][1]], None]
			self.event1 = Clock.schedule_interval(self.update, .05)
			self.b2_2.text = "pause"
			self.b_setting1(True, True)
			self.buttons[self.switch[0]].disabled = False
		elif self.b2_2.text == "pause":
			self.b_setting1(False, False)
			self.rt[0][not self.switch[0]] = (self.now - time.time())
			self.tcc[self.switch[0]] += abs(self.rt[0][self.switch[0]])
			Clock.unschedule(self.event1)
			self.b_setting2(True, True)
			self.b2_2.text = "play"
			self.btn    = ["play", "restart"]
			self.switch[1] = 0
		elif self.b2_2.text == "restart":
			self.btn    = ["play", "restart", "setting"]
			self.switch[1] = 1
			self.tcc    = [0, 0]
			self.rt     = [[0, 0], 300]
			self.switch[0] = 0
			self.b_setting2(True, True)
			self.updates()
		elif self.b2_2.text == "setting":
			self.b_setting2(True, True)
			self.switch[2][2] = 1
			self.b2_2.text, self.b2_1.text, self.b2_3.text = "next", "-1", "+1"
		elif self.b2_2.text == "next":
			self.b_setting2(True, True)
			if self.switch[2][0] > 2:
				self.b2_2.text = "confirm"
			self.switch[2][0] += 1
		elif self.b2_2.text == "confirm":
			self.switch[2][2], self.switch[2][0] = 0, 0
			self.b_setting2(True, True)
			self.b2_2.text, self.b2_1.text, self.b2_3.text = "setting", "<<", ">>"
	def move(self, mv):
		if self.switch[2][2] == 0:
			if mv == 0:
				self.switch[1] += -1
			else :
				self.switch[1] += 1
			self.b2_2.text = self.btn[self.switch[1]%len(self.btn)] if self.b2_2.text != "next" and self.b2_2.text != "confirm" else "confirm" if self.b2_2.text != "next" else "next"
		else :
			if self.switch[2][0] == 4:
				if mv == 0: self.mode += -1
				else: self.mode += 1
				self.l1_1_3.text=str(self.mode)
			else:
				if mv == 0:
					self.timer[0 if self.switch[2][0]<2 else 1] += -self.switch[2][1][self.switch[2][0]]
				else :
					self.timer[0 if self.switch[2][0]<2 else 1] += self.switch[2][1][self.switch[2][0]]
				if self.timer[0 if self.switch[2][0]<2 else 1] < 10:self.timer[0 if self.switch[2][0]<2 else 1] = 10
			self.updates()
	def b1_pressed(self, n):
		self.play_sound(0)
		self.switch[0] = n
		self.b_setting2(n, not n)
	def updates(self, *args):
		for n, i in zip(self.labels, range(len(self.labels))):
			n.text = self.TC(self.timer[i])
	def update(self, *args):
		if self.rt[1] == None:
			self.rt[1] = self.switch[0]
		elif self.rt[1] == self.switch[0]:
			self.rt[0][self.switch[0]] = (self.now - time.time())
		else:
			self.tcc[self.switch[0]] += abs(self.rt[0][self.switch[0]])
			self.tcc[not self.switch[0]] += -self.mode
			self.labels[not self.switch[0]].text = self.TC((self.timer[self.switch[0]]-self.tcc[not self.switch[0]])+self.rt[0][not self.switch[0]])
			self.rt[0][self.switch[0]], self.rt[1] = 0, self.switch[0]
			Time = (self.timer[self.switch[0]]-self.tcc[self.switch[0]])+self.rt[0][self.switch[0]]
			self.now = time.time()
		Time = (self.timer[self.switch[0]]-self.tcc[self.switch[0]])+self.rt[0][self.switch[0]]
		self.labels[self.switch[0]].text = self.TC(Time)
		if Time <= 0:
			for n in range(2):
				self.play_sound(1)
			self.labels[self.switch[0]].text = self.TC(0)
			self.b_setting2(True, True)
			self.b2_2.text = "restart"
			self.btn    = ["restart"]
			self.switch[1] = 0
			self.b_setting1(False, False)
			Clock.unschedule(self.event1)
	def play_sound(self, *args):
		if self.sound[args[0]]:
			self.sound[args[0]].play()
if __name__ == "__main__":
	main().run()
