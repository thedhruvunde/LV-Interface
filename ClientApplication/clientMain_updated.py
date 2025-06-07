from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import socket

class NetworkSender(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.s = None
        self.connected = False

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

        # Connect button
        connect_button = Button(text="Connect")
        connect_button.bind(on_press=self.connect_dev)
        self.add_widget(connect_button)

        # Send button
        send_button = Button(text="Send")
        send_button.bind(on_press=self.send_message)
        self.add_widget(send_button)

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unavailable"

    def connect_dev(self, instance):
        if self.connected:
            return
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.server_ip_input.text, 12345))  # Replace with your server port
            self.connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print("Connection failed:", e)

    def send_message(self, instance):
        if self.connected and self.s:
            try:
                msg = self.message_input.text
                self.s.sendall(msg.encode())
                self.message_input.text = ""
            except Exception as e:
                print("Send failed:", e)

    def receive_messages(self):
        while self.connected:
            try:
                data = self.s.recv(1024)
                if data:
                    print("Server:", data.decode())
                else:
                    break
            except:
                break

class MyApp(App):
    def build(self):
        return NetworkSender()


if __name__ == '__main__':
    MyApp().run()
