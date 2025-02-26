# RFXtrx-mqtt - Process & Automate RFXtrx Data with MQTT

![PyPI](https://img.shields.io/pypi/v/rfxtrx-mqtt)
![License](https://img.shields.io/github/license/FredrikBlix/rfxtrx-mqtt)
![Python](https://img.shields.io/badge/python-3.6%2B-blue)

`rfxtrx-mqtt` is a Python package that processes and decodes **RFXtrx** data from a serial device, converting it into JSON. It supports MQTT for seamless integration with home automation platforms like OpenHAB and Home Assistant.

## **🔧 Features**

✅ **Decodes RFXtrx data into JSON format**  
✅ **Supports multiple device types (Lighting, Temperature, Humidity, Security, Blinds, etc.)**  
✅ **Command-line interface (`rfxtrx` CLI)**  
✅ **Flexible callback functions for real-time data processing**  
✅ **Configurable serial device parameters**  
✅ **Built-in MQTT support for automation platforms**

---

## **📦 Installation**

### **Install via PyPI**

```bash
pip install -r requirements.txt
```

### **Install from GitHub (Development Version)**

```bash
git clone https://github.com/FredrikBlix/rfxtrx-mqtt.git
cd rfxtrx-mqtt
pip install -r requirements.txt
```

---

## **🚀 Usage**

### **🔹 Running the `rfx-dump` Command**

```bash
rfx-dump --help
```

✅ **Example: Read from `/dev/ttyUSB0` (default settings)**

```bash
rfx-dump
```

✅ **Example: Specify device and baud rate**

```bash
rfx-dump --device /dev/ttyUSB1 --baudrate 115200
```

✅ **Example: Publish RFXtrx data to MQTT**

```bash
rfx-mqtt --device /dev/ttyUSB0 --mqtt-host localhost --mqtt-port 1883 --mqtt-topic rfxtrx
```

✅ **Example: Subscribe to MQTT topic**

```bash
rfx-mqtt-sub --mqtt-host localhost --mqtt-topic rfxtrx/#
```

✅ **Example: Manually publish MQTT message**

```bash
rfx-mqtt-pub --mqtt-host localhost --mqtt-topic rfxtrx --data '{"device_id": "1a41", "unit_code": 1, "command": "On"}'
```

---

## **🏠 Home Automation Integration**

### **Home Assistant**

To integrate `rfx-mqtt` with **Home Assistant**, configure an MQTT sensor in `configuration.yaml`:

```yaml
mqtt:
    sensor:
        - name: "RFXtrx Lighting Sensor"
          state_topic: "rfxtrx/Lighting1"
          value_template: "{{ value_json.command }}"
```

Restart Home Assistant after adding this configuration.

### **OpenHAB**

To integrate `rfx-mqtt` with **OpenHAB**, use the MQTT binding and add the following to `mqtt.things`:

```txt
Thing mqtt:topic:rfxtrx "RFXtrx" {
    Channels:
        Type string : lighting1 "Lighting1 Command" [ stateTopic="rfxtrx/Lighting1" ]
}
```

Then, define an `Item` in `mqtt.items`:

```txt
String RFXtrx_Lighting "RFXtrx Light" {channel="mqtt:topic:rfxtrx:lighting1"}
```

Restart OpenHAB after making these changes.

---

## **📜 License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **🤝 Contributing**

We welcome contributions! To get started:

1. **Fork the repository** on GitHub
2. **Clone your forked repo**
    ```bash
    git clone https://github.com/YOUR_USERNAME/rfx-mqtt.git
    cd rfx-mqtt
    ```
3. **Create a feature branch**
    ```bash
    git checkout -b feature-name
    ```
4. **Make your changes, commit, and push**
    ```bash
    git add .
    git commit -m "Added new feature"
    git push origin feature-name
    ```
5. **Submit a pull request!** 🎉

---

🚀 **Thank you for using `rfx-mqtt`!** If you find this project useful, give it a ⭐ on GitHub!
