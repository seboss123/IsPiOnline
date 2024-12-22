# Pi Temperature Monitor

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![Paramiko](https://img.shields.io/badge/Paramiko-SSH-green.svg)](http://www.paramiko.org/)

A real-time Raspberry Pi monitoring application that tracks temperature and online status with a graphical interface.

## 📊 Features
- Real-time temperature monitoring with graphical display
- SSH connection status indicators
- Interactive temperature vs time graph
- Auto-refresh every second
- Clean Tkinter GUI interface

## 🛠️ Requirements
- Python 3.x
- Tkinter (usually comes with Python)
- Paramiko
- Matplotlib
- Raspberry Pi with SSH enabled

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pi-monitor.git
   cd pi-monitor
   ```
2. Install dependencies:
   ```bash
   pip install paramiko matplotlib
   ```

## ⚙️ Configuration
1. Create a `config.ini` file in the project root:
   ```ini
   [SSH]
   hostname = your_pi_ip
   username = your_username
   password = your_password  # Or use SSH key authentication
   ```

## 🚀 Usage
Run the application:
```bash
python IsPiOnline.py
```

## 📱 Interface
- **Status Indicator:** Real-time online/offline status of your Pi
- **Temperature Display:** Current CPU temperature reading
- **Graph:** Dynamic temperature plotting over time
- **Auto-refresh:** Updates every second automatically

## 🔍 How It Works
The application:
1. Establishes an SSH connection to your Raspberry Pi
2. Retrieves temperature using `vcgencmd measure_temp`
3. Updates the GUI with connection status and temperature
4. Plots the temperature data on a real-time graph using matplotlib

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Security Best Practices
- Use SSH key authentication instead of passwords
- Store sensitive credentials in environment variables
- Implement proper error handling and logging
- Regularly update dependencies
- Use a `.gitignore` file to exclude sensitive data

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ for Raspberry Pi enthusiasts