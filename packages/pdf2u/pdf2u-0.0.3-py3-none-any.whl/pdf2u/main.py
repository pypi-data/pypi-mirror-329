import asyncio
import logging
from enum import Enum
from pathlib import Path
from typing import Any

import tqdm  # type: ignore
import typer
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

import pdf2u.high_level
from pdf2u.const import get_cache_file_path
from pdf2u.document_il.translator.translator import (
    BaseTranslator,
    BingTranslator,
    GoogleTranslator,
    OpenAITranslator,
    set_translate_rate_limiter,
)
from pdf2u.io import load_json
from pdf2u.translation_config import TranslationConfig

# Initialize typer app
pdf2u.high_level.init()
app = typer.Typer(help="PDF translation tool")

# Setup logging
logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
logger = logging.getLogger(__name__)

# Disable noisy loggers
NOISY_LOGGERS = ["httpx", "openai", "httpcore", "http11", "peewee"]

for logger_name in NOISY_LOGGERS:
    log = logging.getLogger(logger_name)
    log.setLevel("CRITICAL")
    log.propagate = False


class TranslationService(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    BING = "bing"


def create_progress_handler(translation_config: TranslationConfig):  # type: ignore
    """Create a progress handler function based on the configuration."""
    if translation_config.use_rich_pbar:
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        )
        translate_task_id = progress.add_task("translate", total=100)
        stage_tasks = {}

        def progress_handler(event: dict[str, Any]) -> None:
            if event["type"] == "progress_start":
                stage_tasks[event["stage"]] = progress.add_task(
                    f"{event['stage']}", total=event.get("stage_total", 100)
                )
            elif event["type"] == "progress_update":
                stage = event["stage"]
                if stage in stage_tasks:
                    progress.update(
                        stage_tasks[stage],
                        completed=event["stage_current"],
                        total=event["stage_total"],
                        description=f"{event['stage']} ({event['stage_current']}/{event['stage_total']})",
                        refresh=True,
                    )
                progress.update(
                    translate_task_id, completed=event["overall_progress"], refresh=True
                )
            elif event["type"] == "progress_end":
                stage = event["stage"]
                if stage in stage_tasks:
                    progress.update(
                        stage_tasks[stage],
                        completed=event["stage_total"],
                        total=event["stage_total"],
                        description=f"{event['stage']} (Complete)",
                        refresh=True,
                    )
                    progress.update(
                        translate_task_id,
                        completed=event["overall_progress"],
                        refresh=True,
                    )
                progress.refresh()

        return progress, progress_handler
    else:
        pbar = tqdm.tqdm(total=100, desc="translate")

        def progress_handler(event: dict[str, Any]) -> None:
            if event["type"] == "progress_update":
                pbar.update(event["overall_progress"] - pbar.n)
                pbar.set_description(
                    f"{event['stage']} ({event['stage_current']}/{event['stage_total']})"
                )
            elif event["type"] == "progress_end":
                pbar.set_description(f"{event['stage']} (Complete)")
                pbar.refresh()

        return pbar, progress_handler


async def process_file(config: TranslationConfig, debug: bool) -> None:
    """Process a single PDF file."""
    progress_context, progress_handler = create_progress_handler(config)

    with progress_context:
        async for event in pdf2u.high_level.async_translate(config):
            progress_handler(event)
            if debug:
                logger.debug(event)
            if event["type"] == "finish":
                result = event["translate_result"]
                logger.info("Translation Result:")
                logger.info(f"  Original PDF: {result.original_pdf_path}")
                logger.info(f"  Time Cost: {result.total_seconds:.2f}s")
                logger.info(f"  Mono PDF: {result.mono_pdf_path or 'None'}")
                logger.info(f"  Dual PDF: {result.dual_pdf_path or 'None'}")
                break


@app.command()
def version() -> None:
    """Print the version of pdf2u."""
    typer.echo(pdf2u.__version__)


@app.command()
def translate(
    files: list[Path] = typer.Option(
        ..., "--files", "-f", help="PDF files to translate"
    ),
    config_file: Path | None = typer.Option(
        None, "--config", "-c", help="Path to JSON config file"
    ),
    service: TranslationService = typer.Option(
        None, "--service", "-s", help="Translation service to use"
    ),
    openai_api_key: str | None = typer.Option(
        None, "--openai-api-key", "-k", help="OpenAI API key"
    ),
    openai_model: str = typer.Option(
        "gpt-4-mini", "--openai-model", "-m", help="OpenAI model name"
    ),
    openai_base_url: str | None = typer.Option(
        None, "--openai-base-url", "-b", help="OpenAI API base URL"
    ),
    lang_in: str = typer.Option("en", "--lang-in", "-li", help="Source language"),
    lang_out: str = typer.Option("zh", "--lang-out", "-lo", help="Target language"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output directory"),
    pages: str | None = typer.Option(
        None, "--pages", "-p", help="Pages to translate (e.g. '1,2,1-,-3,3-5')"
    ),
    qps: int = typer.Option(4, "--qps", "-q", help="QPS limit for translation"),
    min_text_length: int = typer.Option(
        5, "--min-text-length", help="Minimum text length to translate"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging"),
    ignore_cache: bool = typer.Option(
        False, "--ignore-cache", "-ic", help="Ignore translation cache"
    ),
    no_dual: bool = typer.Option(False, "--no-dual", help="Don't output bilingual PDF"),
    no_mono: bool = typer.Option(
        False, "--no-mono", help="Don't output monolingual PDF"
    ),
    skip_clean: bool = typer.Option(False, "--skip-clean", help="Skip PDF cleaning"),
    enhance_compatibility: bool = typer.Option(
        False, "--enhance-compatibility", help="Enable all compatibility enhancements"
    ),
    rpc_doclayout: str | None = typer.Option(
        None, "--rpc-doclayout", help="RPC service host for document layout"
    ),
) -> None:
    """Translate PDF files using various translation services."""
    if isinstance(config_file, Path):
        if not config_file.exists():
            typer.echo(f"Error: Config file not found: {config_file}")
            raise typer.Exit(1)
        conf = load_json(config_file)
        service = conf.get("service", service)
        openai_api_key = conf.get("openai_api_key", openai_api_key)
        openai_model = conf.get("openai_model", openai_model)
        openai_base_url = conf.get("openai_base_url", openai_base_url)
        lang_in = conf.get("lang_in", lang_in)
        lang_out = conf.get("lang_out", lang_out)
        output = Path(conf.get("output", output)) if conf.get("output") else output
        pages = conf.get("pages", pages)
        qps = conf.get("qps", qps)
        min_text_length = conf.get("min_text_length", min_text_length)
        debug = conf.get("debug", debug)
        ignore_cache = conf.get("ignore_cache", ignore_cache)
        no_dual = conf.get("no_dual", no_dual)
        no_mono = conf.get("no_mono", no_mono)
        skip_clean = conf.get("skip_clean", skip_clean)
        enhance_compatibility = conf.get("enhance_compatibility", enhance_compatibility)
        rpc_doclayout = conf.get("rpc_doclayout", rpc_doclayout)

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate translation service
    if not service:
        typer.echo("Error: Must specify a translation service (--service)")
        raise typer.Exit(1)

    # Validate OpenAI settings
    if service == TranslationService.OPENAI and not openai_api_key:
        typer.echo("Error: OpenAI API key required when using OpenAI service")
        raise typer.Exit(1)

    # Initialize translator
    translator: BaseTranslator
    if service == TranslationService.OPENAI:
        translator = OpenAITranslator(
            lang_in=lang_in,
            lang_out=lang_out,
            model=openai_model,
            base_url=openai_base_url,
            api_key=openai_api_key,
            ignore_cache=ignore_cache,
        )
    elif service == TranslationService.BING:
        translator = BingTranslator(
            lang_in=lang_in, lang_out=lang_out, ignore_cache=ignore_cache
        )
    else:  # Google
        translator = GoogleTranslator(
            lang_in=lang_in, lang_out=lang_out, ignore_cache=ignore_cache
        )

    # Set translation rate limit
    set_translate_rate_limiter(qps)

    # Initialize document layout model
    doc_layout_model: DocLayoutModel
    if rpc_doclayout:
        from pdf2u.docvision.rpc_doclayout import RpcDocLayoutModel

        doc_layout_model = RpcDocLayoutModel(host=rpc_doclayout)
    else:
        from pdf2u.docvision.doclayout import DocLayoutModel

        doc_layout_model = DocLayoutModel.load_onnx()

    # Validate files
    for file in files:
        if not file.exists():
            typer.echo(f"Error: File does not exist: {file}")
            raise typer.Exit(1)
        if not file.suffix == ".pdf":
            typer.echo(f"Error: Not a PDF file: {file}")
            raise typer.Exit(1)

    # Get and validate font
    font_path = get_cache_file_path("source-han-serif-cn.ttf")
    if font_path:
        if not Path(font_path).exists():
            typer.echo(f"Error: Font file not found: {font_path}")
            raise typer.Exit(1)
        if not str(font_path).endswith(".ttf"):
            typer.echo(f"Error: Not a TTF font file: {font_path}")
            raise typer.Exit(1)

    # Create output directory if needed
    if output:
        output.mkdir(parents=True, exist_ok=True)

    # Process each file
    for file in files:
        config = TranslationConfig(
            input_file=str(file),
            font=font_path.as_posix() if font_path else None,
            pages=pages,
            output_dir=str(output) if output else None,
            translator=translator,
            debug=debug,
            lang_in=lang_in,
            lang_out=lang_out,
            no_dual=no_dual,
            no_mono=no_mono,
            qps=qps,
            doc_layout_model=doc_layout_model,
            skip_clean=skip_clean,
            enhance_compatibility=enhance_compatibility,
            min_text_length=min_text_length,
        )

        # Run async process_file in event loop
        asyncio.run(process_file(config, debug))


if __name__ == "__main__":
    app()
