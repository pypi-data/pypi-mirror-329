# BeautifulTerminal

**BeautifulTerminal** is a Python library that automatically beautifies terminal output by adding colors based on the content of the messages. This library improves the readability of your console applications and makes it easier to understand log outputs and messages. No additional setup is required after importing!

## Features

- **Automatic Colors**:
  - Errors are displayed in red.
  - Warnings are displayed in yellow.
  - Success messages are displayed in green.
  - Regular messages are displayed in white.

- **Easy Integration**:
  - Simply import the library, and it works immediately.

- **Customizable**:
  - You can easily change the color codes to suit your preferences.

## Installation

To install the library, use `pip`:

```bash
pip install beautifull-terminal
```

## Getting Started

After installation, you can quickly use the library in your Python scripts. Follow these simple steps:

1. **Import the library**:

```python
import beautifull_terminal
```

2. **Print messages**:

Use the `print` function as usual. The library automatically applies the appropriate colors based on the content of your messages.

## Usage

Here are some examples of how to use the library:

```python
import BeautifullTerminal

# Examples of using the library
print("This is a regular message.")  # Default color: White
print("Error: Something went wrong!")  # Error text in Red
print("Warning: Be careful!")  # Warning in Yellow
print("Success: Operation completed!")  # Success in Green
```

### Example Outputs

- Regular message: White
- Warning: Yellow
- Error: Red
- Success: Green

### Using the `color` Option

The `print` function in `BeautifulTerminal` supports an optional `color` parameter that lets you specify the color of the printed text directly. Example:

```python
import beautifull_terminal

print("This text is normal.")  # Default color: White
print("This text is red!", color="red")  # Text in Red
print("This text is yellow!", color="yellow")  # Text in Yellow
print("This text is green!", color="green")  # Text in Green
```

If you specify an invalid color, the default color is used. This gives you flexibility to customize the text to your liking.

## Customization

You can change the color codes in the library to modify the appearance of the outputs. This allows you to tailor the library to your preferred terminal design or personal preferences. Simply modify the `COLORS` dictionary in the `BeautifulTerminal` class.

## Disabling

If you need to temporarily disable color output, you can do so:

```python
import beautifull_terminal as bt
bt.disable()  # Temporarily disable color output
```

To re-enable color output:

```python
bt.enable()  # Re-enable color output
```

## Compatibility

The `BeautifulTerminal` library is compatible with any terminal that supports ANSI escape codes, which includes most modern terminal emulators. However, it may not work correctly on older systems or environments that do not support ANSI codes.

## Acknowledgments

- This library was inspired by the need for better readability of terminal outputs.
- Special thanks to the contributors and the open-source community for their continuous support and suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

## Contact

For questions or feedback, please reach out to us through the [GitHub repository](https://github.com/StarGames2025/beautifull_terminal).