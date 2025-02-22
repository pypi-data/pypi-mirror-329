# Changelog

All notable changes to this project will be documented in this file.

## 0.0.3 - 2025-02-22

### 🐛 Bug Fixes

- Ci test remove 3.13

## 0.0.2 - 2025-02-22

### 🚀 Features

- *(PDF XML IL)* Preliminary basic process of running through PDF -> XML IL -> PDF
- *(PDF XML IL)* Changed approach to use IL for translation assistance. Added initial information to IL.
- *(PDF XML IL)* Initial implementation of parsing + restore.
- *(paragraph)* Preliminary paragraph recognition based on OCR layout
- *(paragraph_finder)* Identify and remove the spaces generated during PDF line breaks
- *(paragraph_finder)* Introduce pdfLine abstraction
- *(pdf translate)* Initial completion of the entire process, but with some issues:
- *(typesetting)* Implement greedy typesetting algorithm and make typesetting an independent step
- *(typesetting)* Add dot alignment in the table of contents
- *(cli)* Better CLI argument (backend implementation pending)
- *(cli)* Add font argument (backend implementation pending)
- *(typesetting)* Implement expanding paragraph box to the right
- *(typesetting)* Limit right expansion to 90% of page cropbox
- *(cli)* Implement most of the CLI argument backend (except for specified page translation)
- *(high_level)* Speed up by parsing only necessary pages
- *(parse)* Better space handling and the first half of rich text
- *(formulas)* When the absolute value of the formula offset is less than 0.1, set it to 0.
- *(il_translator)* Rich Text & Formula Placeholder Translation
- *(utils)* Get_paragraph_length_except and get_paragraph_unicode functions
- *(rich text)* Initial implementation of rich text with mixed formula layout
- *(typesetting)* Implement Algorithm 1
- *(typesetting)* Basic implementation of algorithms 2 and 3
- *(typesetting2)* Add hung punctuation support
- *(doclayout)* Add CPUExecutionProvider to model providers
- *(translation)* Add Bing translator support
- *(translation)* Add translation time logging
- *(main)* Add source-han-serif-cn font and update default font
- *(paragraph_finder)* Add and reorder layout types
- *(typesetting2)* Add and refactor character handling methods
- *(styles_and_formulas)* Add cid check in is_formulas_char
- *(typesetting2)* Add is_space property and enhance space handling
- *(translation)* Supports basic font mapping based on bold and serif presence.
- *(fonts)* Map italic font to kai
- *(typesetting)* Add first line indent support and improve font mapping
- *(typesetting)* Add additional closing punctuation marks
- *(pyproject)* Make the program compatible with more versions of python
- *(midend)* Add formula height ignore logic and improve layout handling
- *(styles_and_formulas)* Add regex check for specific characters
- *(styles_and_formulas)* Add translatable formulas processing
- *(styles_and_formulas)* Add support for splitting formulas by comma
- *(styles_and_formulas)* Add formula merging and improve comma splitting
- *(il_translator)* Add style comparison functions
- *(typesetting)* Add additional punctuation marks to list
- *(translation_config)* Add split short lines functionality
- *(translation)* Add import for TranslationConfig
- *(il)* Change ncolor and scolor to [string]
- *(translation)* Add progress monitoring and rich logging
- *(progress_monitor)* Add time elapsed column
- *(fontmap)* Add progress monitoring and stage name for font mapping
- *(translator)* Add font mapping and enhance style checks
- *(pdfinterp)* Add passthrough per char for SC and sc
- *(dependency)* Add uv.lock to git
- *(translator)* Optimize thread executor configuration for better QPS management
- *(ci)* Run codeql in all push
- *(main)* Add RPC doclayout support and improve document layout model initialization
- *(main cli)* Add logging statements for translation results
- *(fontmap)* Optimize font insertion and xref handling
- *(fontmap)* Enhanced progress bar for adding fonts
- *(typesetting)* Adjust line spacing and scaling logic
- *(progress_monitor)* Add progress change callback support
- *(async)* Add AsyncCallback for asynchronous iteration
- *(async)* Implement async translation workflow
- *(cancel-handling)* Add raise_if_cancelled checks across modules
- *(high_level)* Propagate translation errors
- *(document_il)* Add PDFRectangle element to schema and code
- *(document_il)* Add debug_info attribute to multiple elements
- *(document_il)* Commented debug logging in passthrough per-char instruction processing
- *(translation)* Add no-style-placeholder option for PDF translation
- *(translation)* Improve rich text translation handling
- *(translation)* Add compatibility enhancement options for PDF translation
- *(progress_monitor)* Add report interval configuration and threading lock
- Add minimum text length translation parameter
- Add gui

### 🐛 Bug Fixes

- *(il_translator)* Fix pbar
- *(high_level)* Add missed font argument to Typesetting
- *(pdf parse)* Fixed arxiv watermark font size parsing issue
- *(formulas)* Fixed the formula judgment conditions
- *(il_translator)* Add placeholder handling in PdfParagraphComposition
- *(doclayout)* Remove local_files_only flag in hf_hub_download
- *(high_level)* Correct logger info string formatting
- *(typesetting2)* Handle ValueError in CJK UNIFIED IDEOGRAPH check
- *(typesetting)* Add "、" to the hung punctuation list
- *(fontmap)* Enhance exception message for missing font
- *(pdf)* Fix the text overlap issue caused by xobject nesting.
- *(il_translator)* Add xobject font mapping in translation
- *(typesetting)* Improve font mapping and xobject handling
- Handle None progress_change_callback gracefully
- *(logging)* Improve error message formatting in RPC request handling
- *(progress_monitor)* Ensure cancel event is set on exit
- *(core)* Improve cancellation and error handling
- *(high_level)* Remove redundant log message
- *(pdfinterp)* Keep the color space effective after processing xobject.
- *(typesetting)* Correct library name in translated document
- *(rpc_doclayout)* Increase HTTP request timeout and enable redirect following
- Python lint
- Temporarily disable CoreML execution provider
- Adjust max_batch_size for CoreML execution provider
- Remove docs build

### 🚜 Refactor

- *(typesetting)* Refactor text rendering methods
- *(parse)* Skip most of the original parsing process of pdf2zh to improve parsing speed & reduce memory usage
- *(doclayout)* Add OS detection for provider selection
- *(xml_converter)* Add utf-8 encoding for file operations
- *(il_translator)* Add logging and debug conditionals
- *(doclayout)* Improve model download and code formatting
- *(typesetting2)* Adjust minimum line spacing and add scale reset logic
- *(typesetting2)* Improve code readability and consistency
- *(styles_and_formulas)* Update x_offset handling
- *(typesetting2)* Update bounding box calculation for new_formula
- *(typesetting2)* Improve condition checks and comments
- *(main)* Update argument parser configuration
- *(typesetting2)* Improve unit handling and line height calculation
- *(typesetting)* Remove old typesetting file
- *(main)* Disable httpx logger
- *(translator)* Improve logging and code readability
- *(layout_helper)* Add comment explaining unicode character handling
- *(paragraph_finder)* Uncomment and activate independent paragraph processing
- *(styles_and_formulas)* Improve formula splitting by commas
- *(layout_helper)* Improve new line detection and formatting
- *(styles_and_formulas)* Simplify and optimize formula character processing
- *(main)* Update condition for disabling and propagating
- *(paragraph_finder)* Improve xy_mode handling and add special character support
- *(main)* Add critical logging level for openai
- *(styles_and_formulas)* Update is_translatable_formula regex
- *(main)* Enhance logging configuration
- *(styles_and_formulas)* Update bracket and special character handling
- *(layout_helper)* Add cid for formula vertical line
- *(styles_and_formulas)* Improve formula character detection
- *(styles_and_formulas)* Update variable names and logic for formula handling
- *(fontmap)* Adjust serif check for specific font issues
- *(styles_and_formulas)* Enhance formulas font validation
- *(styles_and_formulas)* Improve code readability and maintainability
- *(typesetting)* Update translation library URL format
- *(il_translator)* Enhance placeholder pattern handling and removal
- *(typesetting)* Update translation library URL
- *(il_translator)* Update translate_paragraph method call
- *(typesetting)* Adjust scale and line spacing parameters
- *(paragraph_finder)* Remove unused clean_xobject_char function
- *(rpc_doclayout)* Handle image input as list and optimize prediction logic
- *(layout_parser)* Increase batch size for page processing
- *(rpc_doclayout)* Remove debug logging
- *(fontmap)* Optimize font resource handling
- *(fontmap)* Enhance char_lengths with lru_cache
- *(translate)* Extract and consolidate translation stages
- *(translation_config)* Enhance working directory handling
- *(high_level)* Update pdf creation path
- *(layout_parser)* Reduce batch size for page processing

### 📚 Documentation

- *(pyproject)* Add issues url to project metadata
- *(README)* Update installation and background sections
- *(README)* Update installation and run instructions
- *(README)* Add contribution guidelines
- *(README)* Update how to contribute section
- *(README)* Update yadt command examples
- *(README)* Add note on poor capitalization support
- *(README)* Add multi-letter corner mark issue to known issues
- *(readme)* Add preview gif
- *(README)* Add banner image and update alt text
- *(images)* Update banner image
- *(implementation details)* Format
- *(images)* Update preview gif
- *(README)* Update project name and references to babeldoc
- *(README)* Update star history link
- *(README)* Update project name to BabelDOC
- *(README)* Update star history chart repository
- *(README)* Add OpenAI API configuration tips
- :zap: update doc
- :fire: update issue template
- Add contributor reward guidelines for BabelDOC project
- Update README.md with Immersive Translation sponsor link
- *(contributor_reward)* Clarify monthly contribution guidelines
- *(contributor_reward)* Add verification rule for PR contributor rewards
- Configure Sphinx documentation settings
- Update ReadTheDocs documentation requirements
- Expand documentation structure for BabelDOC project
- Refactor contributor documentation structure
- Enhance documentation landing page
- Update documentation index files for Sphinx and Markdown
- Update Implementation Details documentation
- Simplify documentation index file
- Configure MyST Markdown extensions for Sphinx documentation
- Enhance MyST Markdown parser configuration
- Add GitHub-style alert mapping for MyST admonitions
- Refactor contributor reward documentation structure
- Add Unicode reference for East Asian text spacing

### ⚡ Performance

- *(styles_and_formulas)* Optimize isspace check and corner mark detection
- *(fontmap)* Optimize font creation and assignment process

### ⚙️ Miscellaneous Tasks

- *(publish)* Add workflow for publishing to TestPyPI and GitHub Release
- *(publish)* Update testpypi package name
- *(publish)* Update workflow to trigger on release
- *(pyproject)* Bump version to 0.0.1a2
- *(publish)* Update workflow to trigger on tag push
- *(pyproject)* Bump version to 0.0.1a4
- *(publish)* Add workflow for publishing to PyPI and TestPyPI
- *(ci)* Remove redundant publish-to-testpypi workflow
- *(pyproject)* Bump version to 0.0.1a7
- *(pyproject)* Bump version to 0.0.1a8
- *(pyproject)* Bump version to 0.0.1a9
- *(docvision)* Move docvision README to new directory
- *(pyproject)* Bump version to 0.0.1a10
- *(pyproject)* Bump version and update python requirement
- *(pyproject)* Bump version to 0.0.1a13
- *(pyproject)* Bump version to 0.0.1a14
- *(pyproject)* Bump version and update httpx dependency to match ollama dependency
- *(pyproject)* Bump version to 0.0.1a16
- *(test)* Setup github actions workflow for python testing
- *(pyproject)* Bump version to 0.0.1a20
- *(pyproject)* Bump version to 0.0.1a22
- *(pyproject)* Bump version to 0.0.1a23
- *(pyproject)* Bump version to 0.0.1a25
- *(pyproject)* Bump version to 0.0.1a26
- *(pyproject)* Bump version to 0.0.1a27
- *(pyproject.toml)* Bump version to 0.0.1a28
- *(pdf)* Remove unnecessary test file
- *(test.yml)* Update test file path
- *(uv.lock)* Update Python version requirements and dependencies
- *(labeler)* Update labeler configuration and workflow
- *(version)* Bump version to 0.1.1
- *(version)* Bump version to 0.1.2
- *(project)* Bump version to 0.1.3 and update readme
- *(version)* Bump version to 0.1.4
- *(pdf_creator)* Format
- Update Ruff linting configuration
- *(test)* Update test commands to use babeldoc
- *(babeldoc)* Bump version to 0.1.6.rc0
- *(version)* Update version to 0.1.6
- *(babeldoc)* Bump version to 0.1.7
- *(ci)* Update PyPI publish workflow for BabelDOC
- Bump version to 0.1.8
- Update ReadTheDocs configuration
- Update project dependencies and documentation resources
- Upgrade GitHub Actions workflow for documentation deployment
- Remove .readthedocs
- Configure GitHub Actions bot credentials for documentation workflow
- Bump version to 0.1.10
- Clean up
- Publish to pypi

### Fix

- *(il_translator)* Add support for inheriting xobj fonts

### Refactor

- *(layout)* Move layout parser to a separate class

### Refactoring

- *(progress)* Move rich and tqdm progress bar to main.py

### Build

- Add dependency

### Cleanup

- *(pdf_creator)* Remove legacy font embedding func

### Deps

- *(pyproject)* Add toml dependency

### High_level

- Temporarily disable translation and subsequent steps for easier debugging.

### I18n

- *(stages)* Translate stage names to English

### Remove

- *(docs)* Delete dpml.rng file

<!-- generated by git-cliff -->
