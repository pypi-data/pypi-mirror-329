from pathlib import Path

import pytest
from typer.testing import CliRunner

from pdf2u.main import app as cli_app


def test_translate_google_cli(pdf_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-q", "50", "-f", pdf_path]
    )
    assert result.exit_code == 0


def test_config_file(pdf_path: Path, config_path_google: Path) -> None:
    """Test configuration file"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-c", config_path_google, "-f", pdf_path]
    )
    assert result.exit_code == 0


def test_cli_version() -> None:
    """Test version command"""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["version"])
    assert result.exit_code == 0


def test_cli_help() -> None:
    """Test help command"""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0
    assert "Translate PDF files" in result.output


def test_missing_service() -> None:
    """Test error when service is not specified"""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["translate", "-f", "dummy.pdf"])
    assert result.exit_code == 1
    assert "Must specify a translation service" in result.output


def test_invalid_service() -> None:
    """Test error with invalid service"""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["translate", "-s", "invalid", "-f", "dummy.pdf"])
    assert result.exit_code != 0
    assert "Invalid value for" in result.output


def test_missing_openai_key() -> None:
    """Test error when OpenAI key is missing"""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["translate", "-s", "openai", "-f", "dummy.pdf"])
    assert result.exit_code == 1
    assert "OpenAI API key required" in result.output


def test_invalid_file_path() -> None:
    """Test error with non-existent file"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", "nonexistent.pdf"]
    )
    assert result.exit_code == 1
    assert "File does not exist" in result.output


def test_invalid_file_type() -> None:
    """Test error with non-PDF file"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a text file
        Path("test.txt").write_text("test")
        result = runner.invoke(cli_app, ["translate", "-s", "google", "-f", "test.txt"])
        assert result.exit_code == 1
        assert "Not a PDF file" in result.output


def test_language_options(pdf_path: Path) -> None:
    """Test language options"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app,
        [
            "translate",
            "-s",
            "google",
            "-f",
            str(pdf_path),
            "--lang-in",
            "fr",
            "--lang-out",
            "en",
        ],
    )
    assert result.exit_code == 0


def test_qps_option(pdf_path: Path) -> None:
    """Test QPS option"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", str(pdf_path), "-q", "100"]
    )
    assert result.exit_code == 0


def test_pages_option(pdf_path: Path) -> None:
    """Test pages option"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", str(pdf_path), "-p", "1-3,5"]
    )
    assert result.exit_code == 0


def test_multiple_files(pdf_path: Path) -> None:
    """Test multiple file inputs"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", str(pdf_path), "-f", str(pdf_path)]
    )
    assert result.exit_code == 0


def test_debug_option(pdf_path: Path) -> None:
    """Test debug option"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", str(pdf_path), "--debug"]
    )
    assert result.exit_code == 0


def test_config_override(pdf_path: Path, config_path_google: Path) -> None:
    """Test command line options override config file"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app,
        [
            "translate",
            "-c",
            str(config_path_google),
            "-f",
            str(pdf_path),
            "-q",
            "100",  # Override QPS from config
        ],
    )
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "option",
    [
        "--no-dual",
        "--no-mono",
        "--skip-clean",
        "--enhance-compatibility",
        "--ignore-cache",
    ],
)
def test_boolean_options(pdf_path: Path, option: str) -> None:
    """Test various boolean options"""
    runner = CliRunner()
    result = runner.invoke(
        cli_app, ["translate", "-s", "google", "-f", str(pdf_path), option]
    )
    assert result.exit_code == 0
