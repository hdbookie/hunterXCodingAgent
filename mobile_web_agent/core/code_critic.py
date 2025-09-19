"""Code quality evaluation and critique system for the Mobile Web Agent."""

import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Represents a code quality issue."""
    type: str  # "style", "security", "performance", "maintainability", "best_practice"
    severity: str  # "low", "medium", "high", "critical"
    line_number: Optional[int]
    message: str
    suggestion: str
    category: str


class CodeCritic:
    """Analyzes code quality and provides improvement suggestions."""

    def __init__(self):
        self.style_rules = self._init_style_rules()
        self.security_patterns = self._init_security_patterns()
        self.performance_patterns = self._init_performance_patterns()

    def critique_code(self, code: str, file_path: str = "") -> Dict[str, Any]:
        """Analyze code and return structured feedback."""
        issues = []

        # Parse code for AST analysis
        try:
            tree = ast.parse(code)
            issues.extend(self._analyze_ast(tree))
        except SyntaxError as e:
            issues.append(CodeIssue(
                type="syntax",
                severity="critical",
                line_number=e.lineno,
                message=f"Syntax error: {e.msg}",
                suggestion="Fix syntax error before proceeding",
                category="syntax"
            ))

        # Analyze line by line
        lines = code.split('\n')
        issues.extend(self._analyze_lines(lines))

        # Analyze file structure
        if file_path:
            issues.extend(self._analyze_file_structure(file_path, code))

        return self._format_critique_response(issues, code)

    def _analyze_ast(self, tree: ast.AST) -> List[CodeIssue]:
        """Analyze Abstract Syntax Tree for code quality issues."""
        issues = []

        for node in ast.walk(tree):
            # Check for long functions
            if isinstance(node, ast.FunctionDef):
                if self._count_lines_in_function(node) > 50:
                    issues.append(CodeIssue(
                        type="maintainability",
                        severity="medium",
                        line_number=node.lineno,
                        message=f"Function '{node.name}' is too long ({self._count_lines_in_function(node)} lines)",
                        suggestion="Consider breaking this function into smaller, more focused functions",
                        category="function_length"
                    ))

            # Check for too many parameters
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 7:
                    issues.append(CodeIssue(
                        type="maintainability",
                        severity="medium",
                        line_number=node.lineno,
                        message=f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                        suggestion="Consider using a configuration object or reducing parameters",
                        category="parameter_count"
                    ))

            # Check for nested complexity
            if isinstance(node, (ast.For, ast.While, ast.If)):
                depth = self._calculate_nesting_depth(node)
                if depth > 4:
                    issues.append(CodeIssue(
                        type="maintainability",
                        severity="high",
                        line_number=node.lineno,
                        message=f"High nesting depth ({depth} levels)",
                        suggestion="Extract nested logic into separate functions",
                        category="complexity"
                    ))

        return issues

    def _analyze_lines(self, lines: List[str]) -> List[CodeIssue]:
        """Analyze code line by line for patterns."""
        issues = []

        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()

            # Check line length
            if len(line) > 120:
                issues.append(CodeIssue(
                    type="style",
                    severity="low",
                    line_number=i,
                    message=f"Line too long ({len(line)} characters)",
                    suggestion="Break long lines for better readability",
                    category="line_length"
                ))

            # Check for hardcoded credentials (security)
            if self._contains_hardcoded_secrets(line_stripped):
                issues.append(CodeIssue(
                    type="security",
                    severity="critical",
                    line_number=i,
                    message="Potential hardcoded credential detected",
                    suggestion="Use environment variables or secure configuration",
                    category="secrets"
                ))

            # Check for SQL injection patterns
            if re.search(r'execute\s*\([^)]*[\'"].*\+.*[\'"][^)]*\)', line_stripped, re.IGNORECASE):
                issues.append(CodeIssue(
                    type="security",
                    severity="high",
                    line_number=i,
                    message="Potential SQL injection vulnerability",
                    suggestion="Use parameterized queries or ORM",
                    category="sql_injection"
                ))

            # Check for print statements in production code
            if re.search(r'\bprint\s*\(', line_stripped) and 'debug' not in line_stripped.lower():
                issues.append(CodeIssue(
                    type="best_practice",
                    severity="medium",
                    line_number=i,
                    message="Print statement found",
                    suggestion="Use proper logging instead of print statements",
                    category="logging"
                ))

        return issues

    def _analyze_file_structure(self, file_path: str, code: str) -> List[CodeIssue]:
        """Analyze file-level structure and conventions."""
        issues = []

        # Check for missing docstrings
        if not code.strip().startswith('"""') and not code.strip().startswith("'''"):
            issues.append(CodeIssue(
                type="best_practice",
                severity="medium",
                line_number=1,
                message="Missing module docstring",
                suggestion="Add a module-level docstring describing the file's purpose",
                category="documentation"
            ))

        # Check import organization
        lines = code.split('\n')
        import_lines = [i for i, line in enumerate(lines) if line.strip().startswith(('import ', 'from '))]

        if import_lines:
            # Check for imports after code
            first_non_import = next((i for i, line in enumerate(lines)
                                   if line.strip() and not line.strip().startswith(('import ', 'from ', '#', '"""', "'''"))
                                   and not line.strip() == ''), None)

            if first_non_import and any(i > first_non_import for i in import_lines):
                issues.append(CodeIssue(
                    type="style",
                    severity="medium",
                    line_number=import_lines[-1] + 1,
                    message="Imports should be at the top of the file",
                    suggestion="Move all imports to the beginning of the file",
                    category="import_order"
                ))

        return issues

    def _format_critique_response(self, issues: List[CodeIssue], code: str) -> Dict[str, Any]:
        """Format the critique response with structured feedback."""
        # Group issues by category
        issues_by_category = {}
        for issue in issues:
            if issue.category not in issues_by_category:
                issues_by_category[issue.category] = []
            issues_by_category[issue.category].append(issue)

        # Calculate overall score
        score = self._calculate_quality_score(issues)

        # Generate summary
        critical_count = len([i for i in issues if i.severity == "critical"])
        high_count = len([i for i in issues if i.severity == "high"])
        medium_count = len([i for i in issues if i.severity == "medium"])
        low_count = len([i for i in issues if i.severity == "low"])

        return {
            "quality_score": score,
            "total_issues": len(issues),
            "severity_breakdown": {
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "issues_by_category": {
                category: [
                    {
                        "type": issue.type,
                        "severity": issue.severity,
                        "line": issue.line_number,
                        "message": issue.message,
                        "suggestion": issue.suggestion
                    }
                    for issue in category_issues
                ]
                for category, category_issues in issues_by_category.items()
            },
            "recommendations": self._generate_recommendations(issues),
            "overall_assessment": self._generate_overall_assessment(score, issues)
        }

    def _calculate_quality_score(self, issues: List[CodeIssue]) -> float:
        """Calculate a quality score from 0-100 based on issues."""
        if not issues:
            return 100.0

        severity_weights = {
            "critical": -25,
            "high": -10,
            "medium": -5,
            "low": -2
        }

        total_deduction = sum(severity_weights.get(issue.severity, 0) for issue in issues)
        score = max(0, 100 + total_deduction)
        return round(score, 1)

    def _generate_recommendations(self, issues: List[CodeIssue]) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []

        critical_issues = [i for i in issues if i.severity == "critical"]
        high_issues = [i for i in issues if i.severity == "high"]

        if critical_issues:
            recommendations.append("🔴 CRITICAL: Address security vulnerabilities and syntax errors immediately")

        if high_issues:
            recommendations.append("🟡 HIGH: Reduce code complexity and fix major maintainability issues")

        # Category-specific recommendations
        categories = set(issue.category for issue in issues)

        if "security" in categories:
            recommendations.append("🔒 Security: Review and fix all security-related issues")

        if "complexity" in categories:
            recommendations.append("🔧 Refactoring: Break down complex functions for better maintainability")

        if "documentation" in categories:
            recommendations.append("📝 Documentation: Add missing docstrings and comments")

        return recommendations

    def _generate_overall_assessment(self, score: float, issues: List[CodeIssue]) -> str:
        """Generate an overall code quality assessment."""
        if score >= 90:
            return "Excellent code quality with minimal issues"
        elif score >= 75:
            return "Good code quality with some minor improvements needed"
        elif score >= 60:
            return "Acceptable code quality but requires attention to several issues"
        elif score >= 40:
            return "Poor code quality requiring significant improvements"
        else:
            return "Critical code quality issues requiring immediate attention"

    def _count_lines_in_function(self, node: ast.FunctionDef) -> int:
        """Count the number of lines in a function."""
        if hasattr(node, 'end_lineno'):
            return node.end_lineno - node.lineno
        return 0

    def _calculate_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        """Calculate the maximum nesting depth of control structures."""
        max_depth = depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.With, ast.Try)):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)

        return max_depth

    def _contains_hardcoded_secrets(self, line: str) -> bool:
        """Check if line contains potential hardcoded secrets."""
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'["\'][A-Za-z0-9+/]{20,}["\']',  # Base64-like strings
        ]

        for pattern in secret_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def _init_style_rules(self) -> Dict[str, Any]:
        """Initialize style checking rules."""
        return {
            "max_line_length": 120,
            "max_function_length": 50,
            "max_parameters": 7,
            "require_docstrings": True
        }

    def _init_security_patterns(self) -> List[str]:
        """Initialize security vulnerability patterns."""
        return [
            r'eval\s*\(',
            r'exec\s*\(',
            r'os\.system\s*\(',
            r'subprocess\.call\s*\(',
        ]

    def _init_performance_patterns(self) -> List[str]:
        """Initialize performance anti-patterns."""
        return [
            r'\.append\s*\([^)]*\)\s*in\s+.*for.*in',  # List comprehension opportunity
            r'time\.sleep\s*\(\s*[0-9]+\s*\)',  # Long sleeps
        ]