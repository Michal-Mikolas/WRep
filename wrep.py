from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty


class MainView(BoxLayout):
	output_sheet = StringProperty("")

	def pressed(self):
		print('pressing...')
		self.output_sheet = "Ahoj"
		# self.output_sheet.text = "Ahoj"
		print('pressed.')


class WrepApp(App):
	def build(self):
		return MainView()


if __name__ == '__main__':
	WrepApp().run()

