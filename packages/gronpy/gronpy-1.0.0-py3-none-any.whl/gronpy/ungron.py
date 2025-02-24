import json

import js2py


def ungron(gron_input):
    js_str = js2py.eval_js(f"""{gron_input}JSON.stringify(json)""")
    return json.dumps(json.loads(js_str), ensure_ascii=False)
