from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from datetime import date, timedelta
import re
import math
# import numpy


class MainView(BoxLayout):
	input_sheet = ObjectProperty(None)
	output_sheet = ObjectProperty(None)
	output_headline = ObjectProperty(None)

	def pressed(self):
		self.update_output_headline()
		self.update_output_sheet()

	def update_output_headline(self):
		today = date.today()
		day = int(today.strftime('%w'))

		mon_now = today - timedelta(days=(day-1))
		fri_next = today + timedelta(days=(7+5-day))

		self.output_headline.text = "%d.%d-%d.%d" % (mon_now.day, mon_now.month, fri_next.day, fri_next.month)

	def update_output_sheet(self):
		#
		# 1) Generate statistics
		#
		lines = self.input_sheet.text.split('\n')

		stats = {}
		for line in lines:
			# Parse line
			line = line.strip()
			if line == '':
				break

			columns = line.split('\t')
			id = columns[6]

			if id not in stats:
				stats[id] = {
					'name': '',
					'tasks': [],
					'hours': 0.0,
				}

				# Stats: Category name
				stats[id]['name'] = id.strip()

			# Stats: Hours
			hours = str(columns[3]).replace(',', '.')
			hours = float(hours)
			stats[id]['hours'] += hours

			# Stats: Tasks
			tasks = re.split(';\s*', columns[7].strip('; '))
			stats[id]['tasks'] += tasks
			stats[id]['tasks'] = list(set(stats[id]['tasks']))  # remove duplicates
			# or?: stats[id]['tasks'] = numpy.unique(stats[id]['tasks'])  # remove duplicates
			# or?: uniq = []; [uniq.append(x) for x in array if x not in uniq]

		#
		# 2) Render
		#
		output = u''
		for stat_name in stats:
			stat = stats[stat_name]
			output += stat['name'] + '\t'
			output += "; ".join(stat['tasks']) + '\t'
			output += '\t'  # Status
			output += str(math.ceil(stat['hours'] * 10) / 10) + '\n'

		self.output_sheet.text = output


class WrepApp(App):
	def build(self):
		return MainView()


if __name__ == '__main__':
	WrepApp().run()

