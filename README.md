
# Discord Embed Generator

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## About the Project

**Discord Embed Generator** is a desktop application built with Python and PyQt6 that allows you to create fully customized Discord embeds in a visual and intuitive way.

With a clean and user-friendly interface, you can preview changes in real time, making it easy to design rich and attractive messages for your Discord servers.

This project is open-source and intended for community use. The official releases contain the stable versions ready for use.

---

## Key Features

- **Real-Time Preview**  
  Instantly see how your embed will look on Discord as you edit it.

- **Color Picker**  
  Choose custom colors for embed elements using an intuitive color selector.

- **Flexible Export Options**  
  Export embeds in formats compatible with:
  - `discord.py`
  - `discord.js`
  - Raw JSON

- **Dynamic Field Management**  
  Add, remove, and organize embed fields dynamically.

- **Modern UI**  
  Clean and responsive interface for a smooth user experience.

---

## Requirements

Before running the project, make sure you have:

- **Python 3.10 or higher**
- **pip** (Python package manager)

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/renegadothedev/Discord-Embed-Generator.git
cd Discord-Embed-Generator


### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

* **Linux / macOS**

```bash
source venv/bin/activate
```

* **Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

Once launched:

* Enter title, description, and other embed properties
* Preview changes in real time
* Customize colors and media
* Dynamically manage fields
* Export the embed in your desired format

---

## Project Structure

```
Discord-Embed-Generator/
├── main.py                 # Application entry point
├── README.md               # Project documentation
├── logic/
│   ├── __init__.py
│   └── exporter.py         # Export logic for multiple formats
├── ui/
│   ├── __init__.py
│   ├── components.py       # UI components
│   ├── main_window.py      # Main application window
│   └── styles.py           # UI styles and themes
└── utils/
    ├── __init__.py
    └── helpers.py          # Utility helper functions
```

---

## Screenshot

![Discord Embed Generator Screenshot](https://via.placeholder.com/800x600.png?text=Add+your+screenshot+here)

> Replace the image above with an actual screenshot of your application.

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch:

```bash
git checkout -b feature/your-feature
```

3. Commit your changes:

```bash
git commit -m "Add your feature"
```

4. Push to your branch:

```bash
git push origin feature/your-feature
```

5. Open a Pull Request

---

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

```

