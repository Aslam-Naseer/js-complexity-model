import gradio as gr
import logging
import queue
import threading
import time

from examples import SIMPLE_CASE, MODERATE_CASE, COMPLEX_CASE, DEFAULT_CODE_SNIPPET
from utils.ansi_to_html import ansi_to_html
from utils.get_label import get_complexity_label
from agents.orchestrator import ComplexityOrchestrator

from dotenv import load_dotenv
load_dotenv()


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)


class ComplexityApp:
    def __init__(self):
        self.orchestrator = ComplexityOrchestrator()

    def run_analysis(self, code_snippet):
        """
        The Generator Function.
        This handles the Threading and Streaming logic.
        """

        # A. Setup Queues
        log_queue = queue.Queue()
        result_queue = queue.Queue()

        # B. Setup Logging Interception
        handler = QueueHandler(log_queue)
        handler.setFormatter(logging.Formatter('%(message)s'))

        # Attach to root logger so we catch ALL agent logs
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)

        # C. Define the Worker (The heavy lifting)
        def worker():
            try:
                results = self.orchestrator.process_file(code_snippet)
                result_queue.put(("success", results))
            except Exception as e:
                # Catch unexpected crashes
                logging.error(f"CRITICAL SYSTEM FAILURE: {e}")
                result_queue.put(("error", str(e)))
            finally:
                # Cleanup: remove handler so we don't duplicate logs later
                root_logger.removeHandler(handler)

        # D. Start the Thread
        t = threading.Thread(target=worker)
        t.start()

        # E. Streaming Loop (The Main Event)
        logs_accumulated = ""

        # While thread is working OR there are still logs left to print
        while t.is_alive() or not log_queue.empty():

            # Drain the queue (fetch all new logs that happened in the last 0.1s)
            while not log_queue.empty():
                try:
                    msg = log_queue.get_nowait()
                    html_msg = f"<div style='font-family: monospace; margin-bottom: 2px; white-space: pre-wrap;'>{ansi_to_html(msg) or '<br>'}</div>"
                    logs_accumulated += html_msg
                except queue.Empty:
                    break

            # Yield updates to UI (Logs = Updated, Table = None)
            yield logs_accumulated, None

            # Wait a tiny bit to be nice to the CPU
            time.sleep(0.1)

        # F. Thread Finished - Get Final Result
        status, final_data = result_queue.get()

        if status == "success":
            # Format for Dataframe: [[Func, Score], [Func, Score]]
            table_data = [[item['function'], item['complexity'], get_complexity_label(item['complexity'])]
                          for item in final_data]

            yield logs_accumulated, table_data
        else:
            # Show error in log, leave table empty
            yield logs_accumulated, None


app_logic = ComplexityApp()


example_map = {
    "Simple case": SIMPLE_CASE,
    "Moderate case": MODERATE_CASE,
    "Complex case": COMPLEX_CASE,
    "Test All cases": DEFAULT_CODE_SNIPPET
}


def load_example(choice):
    return example_map.get(choice, "")


with gr.Blocks(title="Complexity Analyzer") as ui:
    gr.Markdown("## JS Complexity Analysis Model")

    with gr.Column(scale=1):
        with gr.Group():
            code_input = gr.Code(language="javascript",
                                 label="Source Code", lines=24, max_lines=24)
            dropdown = gr.Dropdown(
                choices=list(example_map.keys()),
                label="",
                value="Test All cases",
                filterable=False
            )

            btn_run = gr.Button("Analyze", variant="primary")

        result_table = gr.Dataframe(
            headers=["Function Name", "Complexity Score", "Label"],
            datatype=["str", "number", "str"],
        )

        logs_output = gr.HTML(
            label="Real-time Execution Logs", elem_id="logs")

    dropdown.change(load_example, inputs=dropdown, outputs=code_input)
    ui.load(lambda: DEFAULT_CODE_SNIPPET, outputs=code_input)
    btn_run.click(
        fn=app_logic.run_analysis,
        inputs=[code_input],
        outputs=[logs_output, result_table]
    )


CSS = """
.gradio-container {
  max-width: 100% !important;
  padding: 10px 12% !important;
}
"""


if __name__ == "__main__":
    ui.launch(theme=gr.themes.Monochrome(), css=CSS)  # type: ignore
