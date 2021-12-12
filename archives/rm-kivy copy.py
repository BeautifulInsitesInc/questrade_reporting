import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget

class MyGridLayout(Widget):
    # Initialize infinite keyworlds
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 1
       
        # Create a second grid layout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        # Add widgets
        self.top_grid.add_widget(Label(text="Name: ",
            
        # Add Input Box
        self.name = TextInput(multiline=False)
        self.top_grid.add_widget(self.name)
       
        self.top_grid.add_widget(Label(text="Somthing: "))
        self.something = TextInput(multiline=False)
        self.top_grid.add_widget(self.something)

        self.add_widget(self.top_grid)

        # Create a submit button
        self.submit = Button(text="Submit", 
            font_size=32,
            size_hint_y = None,
            height=50,
            size_hint_x= None,
            width=200
            )
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        name = self.name.text
        print('my name is :',name)

        # Print to the screen
        self.top_grid.add_widget(Label(text=f"myname is :{name}"))


  

class MainAdmin(App):
    def build(self):
        #return Label(text="Hello World")
        return MyGridLayout()


if __name__ == '__main__':
    main_dashboard().run()

