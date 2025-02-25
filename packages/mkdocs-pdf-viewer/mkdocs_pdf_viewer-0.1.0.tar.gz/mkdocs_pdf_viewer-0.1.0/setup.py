from setuptools import setup, find_packages

setup(
    name="mkdocs-pdf-viewer",
    version="0.1.0",
    description="A MkDocs plugin to open PDFs in a modal.",
    author="Niclas Heinz",
    author_email="your.email@example.com",
    url="https://github.com/niclasheinz/mkdocs-pdf-viewer",
    packages=find_packages(),
    install_requires=[
        "mkdocs-material>=9.0.0",
    ],
    entry_points={
        "mkdocs.plugins": [
            "pdf_viewer = mkdocs_pdf_viewer.plugin:PDFViewerPlugin",
        ]
    },
)
