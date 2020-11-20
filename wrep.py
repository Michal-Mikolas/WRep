from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from datetime import date, timedelta
import re


class MainView(BoxLayout):
	input_sheet = ObjectProperty(None)
	output_sheet = ObjectProperty(None)
	output_headline = ObjectProperty(None)

	def pressed(self):
		self.update_output_headline()
		# self.update_output_sheet()

	def update_output_headline(self):
		today = date.today()
		day = int(today.strftime('%w'))

		mon_now = today - timedelta(days=(day-1))
		fri_next = today + timedelta(days=(7+5-day))

		self.output_headline.text = "%d.%d-%d.%d" % (mon_now.day, mon_now.month, fri_next.day, fri_next.month)

	def update_output_sheet(self):
		lines = self.input_sheet.text.split('\n')

		stats = {}
		for line in lines:
			line = line.strip()
			if line == '':
				break

			columns = line.split('\t')

			if columns[6] not in stats:
				stats[columns[6]] = {'name': columns[6], 'tasks': [], 'hours': 0.0}

			# Hours
			stats[columns[6]]['hours'] += float(columns[3])

			# Tasks
			tasks = re.split(';\s*', columns[7])
			stats[columns[6]]['tasks'] += columns[7]


		self.output_sheet.text = self.input_sheet.text


class WrepApp(App):
	def build(self):
		return MainView()


if __name__ == '__main__':
	WrepApp().run()

