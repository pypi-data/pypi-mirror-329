import json
import re
from pathlib import Path
from typing import Any, Mapping

import click
import pydash
from caseconverter import titlecase

from nrp_devtools.config import OARepoConfig

default_builtin_primitive_types: dict[str, str | None] = {
    "multilingual": "IMultilingual",
    "vocabulary_item": "IVocabularyItem",
    "taxonomy_item": "ITaxonomyItem",
}

default_builtin_complex_types: dict[str, str | None] = {}


class ComponentGenerator:
    def __init__(
        self,
        target_dir: Path,
        builtin_primitive_types: Mapping[str, str | None],
        builtin_complex_types: Mapping[str, str | None],
    ):
        self.components_by_name: set[str] = set()
        self.components_by_hash: dict[str, str] = {}
        self.target_dir = target_dir
        self.builtin_primitive_types = {
            **(builtin_primitive_types or {}),
            **default_builtin_primitive_types,
        }
        self.builtin_complex_types = {
            **(builtin_complex_types or {}),
            **default_builtin_complex_types,
        }

    def generate_component(self, name: str, definition: Any, path: list[str]):
        print(f"Generating component {name} {path}")
        output: list[str] = [
            "{# def d, level%s #}" % ("=0" if not path else ""),
        ]
        # split components to primitive and complex
        primitive_fields, complex_fields = pydash.partition(
            definition["children"].items(), lambda x: self.is_primitive(x[1])
        )
        output += self.generate_primitive_fields_table(primitive_fields)
        output += self.generate_complex_fields_tables(complex_fields, path + [name])

        output_string = "\n".join(output)

        component_name = self.generate_component_name(name, definition, path)

        if output_string in self.components_by_hash:
            return self.components_by_hash[output_string]
        self.components_by_hash[output_string] = component_name

        (self.target_dir / f"{component_name}.jinja").write_text(output_string)
        return component_name

    def is_primitive(self, data: Any) -> bool:
        if data["detail"] == "array":
            return self.is_primitive(data["child"])
        if data["detail"] in self.builtin_primitive_types:
            return True
        if data["detail"] in self.builtin_complex_types:
            return False
        return "children" not in data

    def generate_primitive_fields_table(self, fields: list[tuple[str, Any]]):
        output: list[str] = [
            "<ITable>",
        ]
        for key, value in fields:
            if not is_array(value):
                if value["detail"] is False:
                    pass
                component = self.builtin_primitive_types.get(value["detail"])
                if component:
                    output += ["  <ITableField d={d.%s} level={level}>" % key]
                    output += ["      <%s d={d.%s} />" % (component, key)]
                    output += ["  </ITableField>"]
                else:
                    output += ["  <ITableField d={d.%s} level={level}/>" % key]
            else:
                if value["child"]["detail"] is False:
                    continue
                component = self.builtin_primitive_types.get(
                    value["child"]["detail"] + "[]"
                )
                output += ["  <ITableField d={d.%s} level={level}>" % key]
                if component:
                    output += ["      <%s d={d.%s} />" % (component, key)]
                else:
                    output += ["    <ITableArrayValue d={d.%s} />" % key]
                output += ["  </ITableField>"]
        output += ["</ITable>"]
        return output

    def generate_complex_fields_tables(
        self, fields: list[tuple[str, Any]], path: list[str]
    ):
        output: list[str] = []
        for key, value in fields:
            if not is_array(value):
                if value["detail"] is False:
                    continue
                component_name = self.generate_component(key, value, path)
                output += ["<ITableSection d={d.%s} level={level} >" % key]
                output += ["  <%s d={d.%s} />" % (component_name, key)]
                output += ["</ITableSection>"]
            else:
                if value["child"]["detail"] is False:
                    continue
                component_name = self.generate_component(key, value["child"], path)
                output += ["{%% for item in array(d.%s) %%}" % key]
                output += ["  <ITableSection d={item} level={level} >"]
                output += ["    <%s d={item} />" % component_name]
                output += ["  </ITableSection>"]
                output += ["{% endfor %}"]
        return output

    def generate_component_name(self, name: str, definition: Any, path: list[str]):
        if name == "metadata" and not self.components_by_name:
            return "DetailMetadata"
        parts = titlecase(name).split(" ")
        name = "".join([*parts[:-1], plural_to_singular(parts[-1]).capitalize()])

        if name in self.components_by_name:
            for pth in reversed(path):
                name = titlecase(pth).replace(" ", "") + name
                if name not in self.components_by_name:
                    break
            else:
                name = re.sub("[0-9]*$", "", name)
                for idx in range(1, 100):
                    new_name = f"{name}{idx}"
                    if new_name not in self.components_by_name:
                        name = new_name
                        break
                else:
                    raise ValueError(f"Too many components with the same name {name}")

        self.components_by_name.add(name)
        return name


def create_detail_page(
    config: OARepoConfig,
    model_name: str,
    builtin_primitive_types: Mapping[str, str | None],
    builtin_complex_types: Mapping[str, str | None],
):
    ui_file = config.repository_dir / model_name / "models" / "ui.json"
    if not ui_file.exists():
        click.secho(
            f"UI file {ui_file} not found, please run ./nrp model compile {model_name}",
            fg="red",
            err=True,
        )
        raise click.Abort()

    ui_data = json.loads(ui_file.read_text())
    metadata = ui_data["children"]["metadata"]

    target_dir = (
        config.repository_dir
        / "ui"
        / model_name
        / "templates"
        / "semantic-ui"
        / model_name
    )

    generator = ComponentGenerator(
        target_dir, builtin_primitive_types, builtin_complex_types
    )
    generator.generate_component("metadata", metadata, [])


def is_array(data: Any):
    return "child" in data


def plural_to_singular(word: str):
    # Common irregular plural to singular mappings
    irregular_plurals = {
        "children": "child",
        "men": "man",
        "women": "woman",
        "mice": "mouse",
        "geese": "goose",
        "teeth": "tooth",
        "feet": "foot",
        "people": "person",
        "leaves": "leaf",
        "knives": "knife",
        "wives": "wife",
        "lives": "life",
        "elves": "elf",
        "halves": "half",
        "shelves": "shelf",
        "wolves": "wolf",
        "calves": "calf",
    }

    if word.lower() in irregular_plurals:
        return irregular_plurals[word.lower()]

    if word.endswith("ies"):
        return word[:-3] + "y"

    if word.endswith("ves"):
        return word[:-3] + "f"

    if word.endswith("les"):
        return word[:-1]

    if word.endswith("ces"):
        return word[:-1]

    if word.endswith("es"):
        return word[:-2]

    if word.endswith("s"):
        return word[:-1]

    # If no rules apply, return the word as-is (assume it's already singular)
    return word


if __name__ == "__main__":
    import click

    @click.command()
    @click.argument("ui_file")
    @click.argument("output_dir")
    def main(ui_file: str, output_dir: str):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        ComponentGenerator(output_path, {}, {}).generate_component(
            "metadata",
            json.loads(Path(ui_file).read_text())["children"]["metadata"],
            [],
        )

    main()
