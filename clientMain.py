from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

class NetworkSender(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.input = TextInput(hint_text='Type your message here')
        self.add_widget(self.input)
        send_button = Button(text='Send')
        send_button.bind(on_press=self.send_message)
        self.add_widget(send_button)

    def send_message(self, instance):
        message = self.input.text
        try:
            server_ip = '192.168.1.5'  # Replace with the server's IP
            port = 12345
            s = socket.socket()
            s.connect((server_ip, port))
            s.send(message.encode())
            s.close()
        except Exception as e:
            print("Error:", e)

class MyApp(App):
    def build(self):
        return NetworkSender()

if __name__ == '__main__':
    MyApp().run()
