# Endthon

Endthon is a Python variant that introduces explicit `end` statements to denote the closing of code blocks, similar to Ruby.

Inspired by [Bython](https://github.com/mathialo/bython), but `end` is nicer than `{}`.

## Installation

```
pip install -e .
```

## Usage

Write your python code with `end` statements. in `.epy` files.
```python
def open_door(guest)
    if guest == "James"
        print("No thank you.")
    else
        print("Come on in!")
    end
end
```
Run the file:
```bash
endthon open_door.epy
```