from __future__ import annotations

import json
import re
import textwrap
from typing import Any, Optional

from loguru import logger

VarType = int | list['VarType'] | dict[str, 'VarType'] | str


class RegexBuilder:
    def __init__(self):
        self.counter = 0

    def new_capture_group(self, inner_regex: str) -> tuple[str, str]:
        self.counter += 1
        group_name = f'group_{self.counter}'
        return f'(?P<{group_name}>{inner_regex})', group_name


class MatchItem:
    def __init__(self, template: str | None, _regex_builder: RegexBuilder):
        self.template = template
        self.match_regex = ''
        self.group_name: str | None = None

    def extract(self, match: re.Match) -> dict[str, VarType]:
        raise NotImplementedError

    def parse(self, input_string: str) -> dict[str, VarType]:
        regex = r'^\s*' + self.match_regex + r'\s*$'
        m = re.match(regex, input_string, re.DOTALL)
        if not m:
            msg = (
                'Input string does not match template!\n\n'
                f'Template:\n{self.template}\n\n'
                f'Template regex:\n{regex}\n\n'
                f'Input string:\n{input_string}\n'
            )
            raise ValueError(msg)
        return self.extract(m)


class LiteralMatchItem(MatchItem):
    def __init__(self, content: str, regex_builder: RegexBuilder):
        super().__init__(None, regex_builder)
        # TODO: Handle edge cases (ie. \\ at end of line)
        self.match_regex = re.sub(
            r'(?:\\\n)+',
            '\\\n+',
            re.escape(content).replace(r'\ ', r'\s+').replace('\\n', '\\\n'),
        )
        self.group_name = None

    def extract(self, match: re.Match) -> dict[str, VarType]:
        return {}


class VariableMatchItem(MatchItem):
    template_regex = r'\{\{(?P<var_name>\w+)(?::(?P<type>\w+))?\}\}'
    inner_regexes = {'int': r'\d+', 'list': r'.*?', 'str': r'.*?'}

    def __init__(self, template_match: re.Match, regex_builder: RegexBuilder):
        super().__init__(template_match.string, regex_builder)
        self.var_name = template_match.group('var_name')
        self.var_type = template_match.group('type') or 'str'
        regex = self.inner_regexes[self.var_type]
        self.match_regex, self.group_name = regex_builder.new_capture_group(regex)

    def extract(self, match: re.Match) -> dict[str, VarType]:
        assert self.group_name
        value = match.group(self.group_name)
        parsed_value = self._parse(value)
        new_vars = {self.var_name: parsed_value}
        if isinstance(parsed_value, list):
            new_vars[self.var_name + '.str'] = value
        return new_vars

    def _parse(self, value: str) -> VarType:
        if self.var_type == 'int':
            return int(value)
        if self.var_type == 'list':
            # Handles numbered bullets (e.g., 1. item), dash bullets (e.g., - item),
            # asterisk bullets (e.g., * item), and plus bullets (e.g., + item).
            bullet_pattern = re.compile(r'^\s*(\d+\.|[-\*\+])\s*(.*)$', re.M)
            matches = bullet_pattern.findall(value)

            if matches:
                # Extract the actual content (second group) from the matches
                return [match[1].strip() for match in matches]
            # Fallback to split by newline if no pattern is matched
            return [item.strip() for item in value.split('\n') if item.strip()]
        if self.var_type == 'str':
            return value
        raise AssertionError


class ListMatchItem(MatchItem):
    template_regex = (
        r'\[\[:(?P<list_name>\w+):\]\](?P<template_content>.*?)\[\[:\2:\]\]'
    )

    def __init__(self, template_match: re.Match, regex_builder: RegexBuilder):
        super().__init__(template_match.string, regex_builder)
        self.var_name = template_match.group('list_name')
        template_content = template_match.group('template_content')
        self.item_template = TemplateMatchItem(template_content, regex_builder)
        self.template_suffix = '\n*' if template_content.endswith('\n') else ''
        regex, self.group_name = regex_builder.new_capture_group(
            f'(?:{self.item_template.match_regex}{self.template_suffix})+'
        )
        self.match_regex = regex

    def remove_named_groups(self, pattern: str) -> str:
        return re.sub(r'\(\?P<[^>]+>', '(?:', pattern)

    def extract(self, match: re.Match) -> dict[str, VarType]:
        assert self.group_name
        items = []
        original_text = match.group(self.group_name)

        pattern = self.item_template.match_regex
        lookahead_pattern = self.remove_named_groups(pattern) + self.template_suffix
        combined_pattern = f'({pattern}{self.template_suffix})(?=(?:{lookahead_pattern}|$))'

        pos = 0
        while pos < len(original_text):
            item_match = re.search(combined_pattern, original_text[pos:], re.DOTALL)
            if item_match is None:
                break

            items.append(self.item_template.extract(item_match))
            pos += item_match.end(1)

        return {self.var_name: items, self.var_name + '.str': original_text}


class TemplateMatchItem(MatchItem):
    def __init__(self, template: str, regex_builder: Optional[RegexBuilder] = None):
        regex_builder = regex_builder or RegexBuilder()
        template = textwrap.dedent(template).strip()
        super().__init__(template, regex_builder)
        unified_pattern = '|'.join(
            f'(?P<{cls.__name__}>{cls.template_regex})'
            for cls in [ListMatchItem, VariableMatchItem]
        )
        self.children: list[MatchItem] = []
        last_pos = 0
        for match in re.finditer(unified_pattern, template, re.DOTALL):
            if match.start() != last_pos:
                literal = LiteralMatchItem(
                    template[last_pos : match.start()], regex_builder
                )
                self.children.append(literal)

            for cls in [ListMatchItem, VariableMatchItem]:
                if match.group(cls.__name__):
                    child = cls(match, regex_builder)
                    self.children.append(child)
                    break
            last_pos = match.end()
        if last_pos != len(template):
            literal = LiteralMatchItem(template[last_pos:], regex_builder)
            self.children.append(literal)

        combined_regex = ''.join([child.match_regex for child in self.children])
        self.match_regex, self.group_name = regex_builder.new_capture_group(
            combined_regex
        )

    def extract(self, match: re.Match) -> dict[str, VarType]:
        result = {'.str': match.group()}
        for child in self.children:
            if child.group_name is not None and match.group(child.group_name):
                result.update(child.parse(match.group(child.group_name)))
        return result

    def parse(self, input_string: str) -> dict[str, VarType]:
        return super().parse(textwrap.dedent(input_string))

    def get_from_cache(self, cache: dict[str, VarType]) -> dict[str, VarType] | None:
        var_names = [
            x.var_name
            for x in self.children
            if isinstance(x, VariableMatchItem | ListMatchItem)
        ]
        if all(x in cache for x in var_names):
            return {x: cache[x] for x in var_names}
        return None


def parse_template(template: str, input_string: str) -> dict[str, VarType]:
    return TemplateMatchItem(template).parse(input_string)


class MissingVariableError(Exception):
    def __init__(self, template: str, variables: dict[str, Any], missing_var: str):
        message = (
            'Missing variable in template serialization.\n\n'
            "Template:\n```\n{}\n```\n\nVariables:\n```\n{}\n```\n\nMissing Variable: '{}'\n".format(
                template, json.dumps(variables, indent=4), missing_var
            )
        )
        super().__init__(message)


def serialize_template(template: str, variables: dict[str, VarType]) -> str:
    def format_var(match: re.Match) -> str:
        var_name: str = match.group(1).split(':')[0].strip()
        if var_name + '.str' in variables:
            return str(variables[var_name + '.str'])
        if var_name not in variables:
            raise MissingVariableError(template, variables, var_name)
        if not isinstance(variables[var_name], int | str):
            logger.warning(
                'Formatting for list type not implemented ("{}" variable)', var_name
            )
        return str(variables[var_name])

    return re.sub(r'{{(.*?)}}', format_var, template)


def extract_data_vars(data: VarType) -> VarType:
    if isinstance(data, dict):
        filtered_data = {}
        for key, value in data.items():
            if not key.endswith('.str'):
                filtered_data[key] = extract_data_vars(value)
        return filtered_data
    if isinstance(data, list):
        return [extract_data_vars(item) for item in data]
    return data
