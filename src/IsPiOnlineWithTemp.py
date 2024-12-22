import tkinter as tk
from tkinter import font, messagebox
import threading
import paramiko
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import configparser
import os

class IsPiOnlineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title("Is Pi Online?")
        self.geometry("600x400")  # Adjust window size to fit the graph
        self.resizable(False, False)

        self.pi_status_label = tk.Label(self, text="Checking...", font=font.Font(family="Helvetica", size=24), fg="black")
        self.pi_status_label.pack()

        self.pi_temp_label = tk.Label(self, text="", font=font.Font(family="Helvetica", size=18), fg="black")
        self.pi_temp_label.pack()

        self.temperatures = []
        self.timestamps = []

        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.timestamps, self.temperatures, 'r-')
        self.ax.set_title("Raspberry Pi Temperature Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature (°C)")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()

        self.config = self.load_config()
        if not self.config:
            messagebox.showerror("Error", "Missing or invalid config.ini file")
            self.destroy()
            return
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add window close handler
        self.check_pi_status()

    def on_closing(self):
        """Handle window closing event"""
        self.running = False
        # Wait for any pending operations to complete
        self.after(100, self._destroy)
    
    def _destroy(self):
        """Clean up and destroy the window"""
        self.quit()
        self.destroy()

    def load_config(self):
        config = configparser.ConfigParser()
        try:
            if not os.path.exists('config.ini'):
                self.create_default_config()
            config.read('config.ini')
            required = ['hostname', 'username', 'password']
            if not all(key in config['SSH'] for key in required):
                return None
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    def create_default_config(self):
        config = configparser.ConfigParser()
        config['SSH'] = {
            'hostname': 'raspberrypi.local',
            'port': '22',
            'username': 'your_username',
            'password': 'your_password'
        }
        with open('config.ini', 'w') as f:
            config.write(f)

    def check_pi_status(self):
        if not self.running:
            return
        # Run the SSH connection in a separate thread
        threading.Thread(target=self.ssh_pi).start()
        
        # Schedule the next check only if the application is still running
        if self.running:
            self.after(1000, self.check_pi_status)

    def update_gui(self, status, temp_output=None, color=None):
        """Thread-safe GUI updates"""
        if not self.running:
            return
        self.after(0, lambda: self._do_update(status, temp_output, color))

    def _do_update(self, status, temp_output, color):
        """Perform actual GUI updates"""
        if not self.running:
            return
        self.pi_status_label.config(text=status, fg=color if color else "black")
        if temp_output:
            self.pi_temp_label.config(text=f"Temp: {temp_output}")
            self.update_graph(temp_output)

    def ssh_pi(self):
        if not self.running:
            return
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            client.connect(
                self.config['SSH']['hostname'],
                port=int(self.config['SSH'].get('port', 22)),
                username=self.config['SSH']['username'],
                password=self.config['SSH']['password']
            )
            
            stdin, stdout, stderr = client.exec_command("vcgencmd measure_temp")
            temp_output = stdout.read().decode().strip()
            client.close()
            
            self.update_gui("Pi is online!", temp_output, "green")
        except Exception as e:
            self.update_gui("Pi is offline!", color="red")
            print(f"Connection error: {e}")

    def update_graph(self, temp_output):
        if not self.running:
            return
        try:
            temp_value = float(temp_output.split('=')[1].split("'")[0])
            self.temperatures.append(temp_value)
            self.timestamps.append(datetime.datetime.now().timestamp())  # Convert to timestamp

            self.ax.clear()
            self.ax.plot(self.timestamps, self.temperatures, 'r-')
            self.ax.set_title("Raspberry Pi Temperature Over Time")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Temperature (°C)")
            self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: datetime.datetime.fromtimestamp(x).strftime("%H:%M:%S")))
            self.ax.relim()
            self.ax.autoscale_view()

            self.figure.autofmt_xdate()
            self.canvas.draw()
        except Exception as e:
            print(f"Graph update error: {e}")

if __name__ == "__main__":
    app = IsPiOnlineApp()
    app.mainloop()