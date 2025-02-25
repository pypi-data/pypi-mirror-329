import re
import logging
import javalang
from dr_source.core.detectors.base import BaseDetector

logger = logging.getLogger(__name__)


class XXEDetector(BaseDetector):
    REGEX_PATTERNS = [
        re.compile(
            r'(?i)<!DOCTYPE\s+[^>]+(SYSTEM|PUBLIC)\s+["\'][^"\']+["\']', re.DOTALL
        ),
    ]

    def detect(self, file_object):
        results = []
        logger.debug(
            "Regex scanning file '%s' for XXE vulnerabilities.", file_object.path
        )
        for regex in self.REGEX_PATTERNS:
            for match in regex.finditer(file_object.content):
                line = file_object.content.count("\n", 0, match.start()) + 1
                logger.debug(
                    "XXE vulnerability (regex) found in '%s' at line %s: %s",
                    file_object.path,
                    line,
                    match.group(),
                )
                results.append(
                    {
                        "file": file_object.path,
                        "vuln_type": "XXE (regex)",
                        "match": match.group(),
                        "line": line,
                    }
                )
        return results

    def detect_ast_from_tree(self, file_object, ast_tree):
        logger.debug(
            "AST-based detection for XXE is not implemented; falling back to regex."
        )
        return []
