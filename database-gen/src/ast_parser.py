import ast
from _ast import stmt
from enum import Enum
from typing import List, Optional


class ManualBlockIndicator(str, Enum):
    IMPORTS_BEGIN = '>>> manual imports section:'
    IMPORTS_END = '^^^ manual imports section'
    CLASS_CODE_BEGINS = '>>> manual class code section:'
    CLASS_CODE_ENDS = '^^^ manual class code section'


class ASTParser:

    @staticmethod
    def find_or_create_section(statements: List[stmt],
                               begin_indicator: ManualBlockIndicator,
                               end_indicator: ManualBlockIndicator) -> List[stmt]:
        def find_indicator_index(indicator: ManualBlockIndicator) -> Optional[int]:
            for index, statement in enumerate(statements):
                if (isinstance(statement, ast.Expr) and
                        isinstance(statement.value, ast.Constant) and
                        statement.value.value == indicator):
                    return index
            return None

        begin_index = find_indicator_index(begin_indicator)
        end_index = find_indicator_index(end_indicator)
        if begin_index and end_index:
            return statements[begin_index: end_index + 1]
        return [
            ast.parse(f"'{begin_indicator}'").body[0],
            ast.parse(f"'{end_indicator}'").body[0]
        ]

    @staticmethod
    def get_or_create_manual_imports(module: Optional[ast.Module]) -> List[stmt]:
        return ASTParser.find_or_create_section(module.body if module else [],
                                                ManualBlockIndicator.IMPORTS_BEGIN,
                                                ManualBlockIndicator.IMPORTS_END)

    @staticmethod
    def get_or_create_manual_class_code(module: Optional[ast.Module]) -> List[stmt]:
        class_ = ASTParser._find_only_class(module)
        return ASTParser.find_or_create_section(class_.body if class_ else [],
                                                ManualBlockIndicator.CLASS_CODE_BEGINS,
                                                ManualBlockIndicator.CLASS_CODE_ENDS)

    @staticmethod
    def clone_class(class_: ast.ClassDef) -> ast.ClassDef:
        clone = ASTParser._find_only_class(ast.parse(ast.unparse(class_)))
        if not clone:
            raise RuntimeError()
        return clone

    @staticmethod
    def _find_only_class(module: Optional[ast.Module]) -> Optional[ast.ClassDef]:
        return next(
            filter(
                lambda statement: isinstance(statement, ast.ClassDef),
                module.body if module else []),
            None)

    #
    # def find_last_import_index(module: ast.Module) -> int:
    #     for index, statement in enumerate(module.body):
    #         if isinstance(statement, ast.Import) or isinstance(statement, ast.ImportFrom):
    #             continue
    #         return index - 1
    #     raise RuntimeError("Couldn't find a single import or nothing apart a single import...")
