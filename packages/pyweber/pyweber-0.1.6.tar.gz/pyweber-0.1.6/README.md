# PyWeber - A Lightweight Python Framework

<img src="https://pyweber.readthedocs.io/en/latest/images/pyweber.png" alt="PyWeber Logo">

[![PyPI version](https://img.shields.io/pypi/v/pyweber.svg)](https://pypi.org/project/pyweber/) [![Coverage Status](https://coveralls.io/repos/github/webtechmoz/pyweber/badge.svg?branch=main)](https://coveralls.io/github/webtechmoz/pyweber?branch=master) [![License](https://img.shields.io/pypi/l/pyweber.svg)](https://github.com/webtechmoz/pyweber/blob/main/LICENSE)

PyWeber is a lightweight Python framework designed for building and managing web applications with ease. It allows you to quickly create web projects, manage templates, static files, and run a web server, all with minimal configuration.

## Features

- **Create New Projects**: Easily create a new web project with a predefined structure.
- **Run Projects**: Run your project from the command line.
- **Manage Templates**: Automatically handle HTML templates for your web applications.
- **Handle Static Files**: Seamlessly manage CSS, JavaScript, and other static resources.
- **Live Reload**: Supports live reloading for faster development workflow.

## Installation

To install PyWeber, run the following command:
```bash
pip install pyweber
```

## Usage

### Create a New Project
To create a new PyWeber project, use the following command:
```bash
pyweber create-new <project_name>
```

### Running the Project
To run your PyWeber project, use the command:

```bash
pyweber run
```
This will start the project and you can begin developing your web application.

### Example
```python
import pyweber as pw

def main(app: pw.Router):
    app.add_route(route='/', template=pw.Template(template='🚀 Hello, world'))

if __name__ == '__main__':
    pw.run(target=main)
```

## Contributing
Feel free to contribute by opening issues or submitting pull requests. Your contributions are highly appreciated!

## License
PyWeber is licensed under the MIT License. See the LICENSE file for more details.

## Contacts
- Author: DevPythonMZ
- Email: zoidycine@gmail.com
- GitHub: https://github.com/webtechmoz/pyweber