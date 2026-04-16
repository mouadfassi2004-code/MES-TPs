class MethodRouter:
    def __init__(self):
        self._registry = {}

    def register(self, method_name: str, func):
        if method_name in self._registry:
            raise ValueError(f"Méthode déjà enregistrée : {method_name}")
        self._registry[method_name] = func

    def get(self, method_name: str):
        return self._registry.get(method_name)

    def dispatch(self, method_name: str, params: dict):
        func = self.get(method_name)
        if func is None:
            raise KeyError(method_name)
        return func(params)

    def list_methods(self):
        return list(self._registry.keys())