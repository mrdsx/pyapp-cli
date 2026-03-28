from InquirerPy.separator import Separator

from .schemas import Framework


class LibrariesGenerator:
    def get_libraries_choices(
        self, framework: Framework | None
    ) -> list[str | Separator]:
        return [
            *self._get_web_servers(framework),
            *self._get_db_drivers(framework),
            *self._get_orms(framework),
            *self._get_misc_libs(framework),
            *self._get_formatters_and_linters(),
        ]

    def _get_web_servers(self, framework: Framework | None) -> list[str | Separator]:
        if framework is None:
            return []
        return ["gunicorn", "uvicorn", Separator()]

    def _get_db_drivers(self, framework: Framework | None) -> list[str | Separator]:
        if framework == "django":
            return []
        return [
            "aiosqlite",
            "psycopg",
            "asyncpg",
            "mysql-connector-python",
            "pymongo",
            Separator(),
        ]

    def _get_orms(self, framework: Framework | None) -> list[str | Separator]:
        base_orms: list[str | Separator] = [
            "firebase-admin",
            "supabase",
        ]

        if framework != "django":
            base_orms = ["sqlalchemy", "sqlmodel", "tortoise-orm", *base_orms]

        return [*base_orms, Separator()]

    def _get_misc_libs(self, framework: Framework | None) -> list[str | Separator]:
        base_misc_libs: list[str | Separator] = [
            "pytest",
            "pytest-asyncio",
        ]

        if framework == "django":
            base_misc_libs.extend(["pytest-django"])

        if framework != "django":
            base_misc_libs = ["pydantic-settings", *base_misc_libs]
        if framework != "fastapi" and framework != "django":
            base_misc_libs = ["pydantic", *base_misc_libs]

        return [*base_misc_libs, Separator()]

    def _get_formatters_and_linters(
        self,
    ) -> list[str | Separator]:
        return [
            "ruff",
            "black",
            "flake8",
            "pylint",
        ]
