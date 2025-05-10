from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import socket


class NetworkSender(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Show device IP
        self.client_ip = self.get_ip()
        self.ip_label = Label(text=f"Your IP: {self.client_ip}")
        self.add_widget(self.ip_label)

        # Server IP input
        self.server_ip_input = TextInput(hint_text="Enter Server IP", multiline=False)
        self.add_widget(self.server_ip_input)

        # Message input
        self.message_input = TextInput(hint_text="Type your message here", multiline=False)
        self.add_widget(self.message_input)

        # Send button
        send_button = Button(text="Send")
        send_button.bind(on_press=self.send_message)
        self.add_widget(send_button)

        # Close button
        close_button = Button(text="Close")
        close_button.bind(on_press=self.close_app)
        self.add_widget(close_button)

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"

    def send_message(self, instance):
        message = self.message_input.text
        server_ip = self.server_ip_input.text.strip()
        port = 12345  # Make sure this matches your server

        if not server_ip:
            print("Server IP not set.")
            return

        try:
            s = socket.socket()
            s.connect((server_ip, port))
            s.send(message.encode())
            s.close()
            print("Message sent.")
        except Exception as e:
            print("Error:", e)

    def close_app(self, instance):
        App.get_running_app().stop()


class MyApp(App):
    def build(self):
        return NetworkSender()


if __name__ == '__main__':
    MyApp().run()
