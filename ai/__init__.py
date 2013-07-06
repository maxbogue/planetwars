ai_dict = {}

def planetwars_ai(name):
    def planetwars_ai_decorator(f):
        ai_dict[name] = f
        return f
    return planetwars_ai_decorator

import planetwars.ai.simple
