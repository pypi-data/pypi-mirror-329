import os
import argparse
from dotenv import load_dotenv
import time
from zmp_notion_exporter import NotionPageExporter, extract_notion_page_id
import threading
import sys

load_dotenv()


class ProgressIndicator:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\n")
        sys.stdout.flush()

    def _animate(self):
        while self.running:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.1)


def parse_args():
    parser = argparse.ArgumentParser(description="Notion Page Export Tool")

    parser.add_argument(
        "--notion-token",
        help="Notion API Token. You can set it by NOTION_TOKEN environment variable.",
        default=os.environ.get("NOTION_TOKEN", ""),
    )
    parser.add_argument(
        "--root-page-id",
        help="Root page ID to start export. You can set it by ROOT_PAGE_ID environment variable.",
        default=os.environ.get("ROOT_PAGE_ID", ""),
    )
    parser.add_argument(
        "--output-dir",
        help="Directory path for export results. You can set it by OUTPUT_DIR environment variable.",
        default=os.environ.get("OUTPUT_DIR", ""),
    )
    parser.add_argument(
        "--include-subpages", help="Include subpages in the export", default=True
    )
    parser.add_argument(
        "--file-type",
        help="File type for export(default: mdx). support: md, mdx, html",
        default="mdx",
    )

    return parser.parse_args()


def run():
    args = parse_args()

    notion_token = args.notion_token
    if not notion_token:
        print("NOTION_TOKEN is not set.")
        return

    root_page_id = args.root_page_id
    if not root_page_id:
        print("ROOT_PAGE_ID is not set.")
        return

    output_dir = args.output_dir
    if not output_dir:
        print("OUTPUT_DIR is not set.")
        return

    include_subpages = args.include_subpages
    file_type = args.file_type

    print(">>> Starting Notion export with following parameters")
    print("--------------------------------------------------------")
    print(f"@ --notion-token: {notion_token[:5]}...{notion_token[-5:]}")
    print(f"@ --root-page-id: {root_page_id}")
    print(f"@ --output-dir: {output_dir}")
    print(f"@ --include-subpages: {include_subpages}")
    print(f"@ --file-type: {file_type}")
    print("--------------------------------------------------------")

    start_time = time.time()
    progress = ProgressIndicator()
    progress.start()

    try:
        exporter = NotionPageExporter(
            notion_token=notion_token,
            root_page_id=extract_notion_page_id(root_page_id),
            root_output_dir=output_dir,
        )

        if file_type == "md":
            exporter.markdown(include_subpages=include_subpages)
        elif file_type == "mdx":
            exporter.markdownx(include_subpages=include_subpages)
        elif file_type == "html":
            exporter.html(include_subpages=include_subpages)
    finally:
        progress.stop()

    docs_node, static_image_node = exporter.get_output_nodes()
    docs_node.print_pretty(include_leaf_node=True)
    static_image_node.print_pretty(include_leaf_node=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f">>> Export completed successfully in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    run()
