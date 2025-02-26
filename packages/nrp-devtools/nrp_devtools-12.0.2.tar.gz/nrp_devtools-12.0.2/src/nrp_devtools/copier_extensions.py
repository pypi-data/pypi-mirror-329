import pycountry
from copier_templates_extensions import ContextHook
from jinja2 import Environment
from jinja2.ext import Extension


class NRPExtension(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.filters["to_language_name"] = self.to_language_name

    def to_language_name(self, language_code: str) -> str:
        language_code = language_code.lower().strip()
        language = pycountry.languages.get(alpha_2=language_code)
        if language:
            return language.name
        return f"Unknown {language_code}"


class ContextUpdater(ContextHook):
    update = False

    def hook(self, context):
        if context.get("repository_description", None):
            context["repository_description"] = context[
                "repository_description"
            ].strip()
        if "languages" in context and context["languages"]:
            # split on ',' or whitespaces
            context["languages"] = [
                x.strip()
                for x in context["languages"].replace(",", " ").split()
                if x.strip() and x.strip() != "en"
            ]
