from pathlib import Path

import pytest


@pytest.fixture
def config_path_google() -> Path:
    config = Path(__file__).parent / "data" / "config.json"
    assert config.exists()
    return config


@pytest.fixture
def pdf_path() -> Path:
    pdf_p = Path(__file__).parent / "data" / "sample.pdf"
    assert pdf_p.exists()
    return pdf_p


@pytest.fixture
def multiple_pdfs(pdf_path: Path) -> list[Path]:
    """Create multiple test PDF files"""
    return [pdf_path] * 3
