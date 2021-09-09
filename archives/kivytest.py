from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar

class ConverterApp(MDApp):
	def flip(self):
		print('working....')

	def build(self):
		screen = MDScreen()

		#top toolbar
		self.toolbar = MDToolbar(title="Binary to Decimal")
		self.toolbar.pos_hint = {"top": 1}
		self.toolbar.right_action_items = [['rotate-3d-variant', lambda x: self.flip()]]
		screen.add_widget(self.toolbar)

		self.input=MDTextField(
			text = 'Enter a binerary number',
			halign ='center',
			size_hint =(0.8,1),
			pos_hint = {'center_x': 0.5, 'center_y':0.45},
			font_size = 22
			)
		screen.add_widget(self.input)
		return screen

if __name__ == '__main__':
    ConverterApp().run()