# jelly_detector
This solution uses methods implemented in OpenCV.

## Usage
```
python3 main.py --help

usage: main.py [-h] [--input INPUT] [--output OUTPUT] [--show_bb SHOW_BB]

Code for detection of different types of jellies

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      Path to folder with input images
  --output OUTPUT    Path to output file
  --show_bb SHOW_BB  'n' to turn off showing images
```
## Example usage
```bash
python3 main.py --input ./images --output output.json 
```