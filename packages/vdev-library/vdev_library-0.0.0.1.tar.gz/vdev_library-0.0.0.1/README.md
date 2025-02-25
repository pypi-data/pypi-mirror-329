# VDEV library

vdev_library  is a Small Python library to support python project development

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vdev_library.

```bash
pip install vdev_library
```

## Usage

```python
from vdev_library import find_vietnamese_phone_numbers #FUNCTION get all vietnam mobile phone from text string
from vdev_library import vdev_set_log  # function set log file /logs/info /logs/debug /logs/warning  /logs/error  vdev_set_log(type_log, filename, message, class_name)
# returns 'func find_vietnamese_phone_numbers'
print(find_vietnamese_phone_numbers("My phone number is +84987654321 and my friend's number is 0987654321."))

vdev_set_log("INFO", "info_log ", "Success ", __name__)
vdev_set_log("ERROR", "error_log ", "Success ", __name__)
vdev_set_log("WARNING", "warning_log ", "Success ", __name__)
vdev_set_log("DEBUG", "debug_log ", "Success ", __name__)
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)