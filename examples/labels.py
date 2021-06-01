import json
measurements = json.loads(open(r'EXCH-BUG_300844331_JSON.txt').read()[1:-1])['reports'][0]['measurements']
coordinates = map(lambda m: (m['location']['coordinates'][1], m['location']['coordinates'][0]), measurements)

from jinja2 import Template
t = Template(open('labels.html', "r").read())
outputText = t.render(coordinates = coordinates)
file('output.html', 'w').write(outputText)
