# Julius Cipher - Python Edition
A simple program use to Encipher/Decipher text to/from Caesar Cipher or Vigenere Cipher.
And yes, there are more versions of this program from other programming languages.

## Installation
<ol type="1">
  <li>
    Install Python 3.x from <a href="https://www.python.org/downloads/">here</a>. (Ignore if you already have Python 3.x installed)
  </li>
  <li>
    Open terminal, run:
    
```
pip install julius_cipher
```
  </li>
</ol>

## Usage
<ol type="1">
  <li>
    Open terminal, run:

```
caesar
```
  </li>
  <li>
    Alternatively, in a Python file (*.py), you can do:
    
```python
from julius_cipher import main
main()
```
To use the program.
  </li>
  <li>
    Similarly, you can do:
    
```python
from julius_cipher import Caesar
```
Or:
```python
from julius_cipher import Vigenere
```
To use the ciphering functions.
  </li>
</ol>

## Changelog
Version 4.0: Added support for Vigenere Cipher.

## Requirement(s)
1. Python 3.x
2. Ziz's Utilities.

## Note(s)
1. While the input from file mode support pretty much any file type, anything other than plain text files (*.txt,...) could cause the program to freeze up (e.g *.exe,...) so avoid inputting those.

## License
This project is licensed under the GNU General Public License 3.0, check [LICENSE](LICENSE) for more details.