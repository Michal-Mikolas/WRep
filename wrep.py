from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from datetime import date, timedelta
import re
import math


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

			if columns[6] not in stats:
				stats[columns[6]] = {
					'name': '',
					'tasks': [],
					'hours': 0.0,
				}

				# Stats: Category name
				stats[columns[6]]['name'] = columns[6].strip()

			# Stats: Hours
			stats[columns[6]]['hours'] += float(columns[3])

			# Stats: Tasks
			tasks = re.split(';\s*', columns[7].strip('; '))
			stats[columns[6]]['tasks'] += tasks
			stats[columns[6]]['tasks'] = list(set(stats[columns[6]]['tasks']))  # remove duplicates
			# or: uniq = []; [uniq.append(x) for x in array if x not in uniq]

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

