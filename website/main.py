import json
import subprocess

subprocess.run('npm run build', shell=True)

print(json.dumps({'result': 'hello'}))

