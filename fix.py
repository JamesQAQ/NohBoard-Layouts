import argparse
import json
from typing import Dict


PADDING = 12


def Main(args: argparse.Namespace):
  if args.layout:
    with open(args.layout, 'rb') as f:
      layout = json.loads(f.read().decode())

    min_x = 4096
    min_y = 4096
    max_x = 0
    max_y = 0
    for element in layout['Elements']:
      boundaries = [element['Location']] if 'Location' in element else []
      boundaries.extend(element.get('Boundaries', []))
      for boundary in boundaries:
        min_x = min(min_x, boundary['X'])
        min_y = min(min_y, boundary['Y'])
        max_x = max(max_x, boundary['X'])
        max_y = max(max_y, boundary['Y'])

    def update(location: Dict):
      location['X'] = location['X'] - min_x + PADDING
      location['Y'] = location['Y'] - min_y + PADDING

    layout['Width'] = max_x - min_x + 2 * PADDING
    layout['Height'] = max_y - min_y + 2 * PADDING
    for element in layout['Elements']:
      if 'Location' in element:
        update(element['Location'])
      if 'TextPosition' in element:
        update(element['TextPosition'])
      if 'Boundaries' in element:
        for boundary in element['Boundaries']:
          update(boundary)

    with open(args.layout, 'w') as f:
      f.write(json.dumps(layout, indent=2))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-l', '--layout', type=str)
  Main(parser.parse_args())
