import queue
import threading
import gradio as gr
import time
import random

# ============================================================================
# SIMULATED HEAVY WORK (replaces your actual orchestrator)
# ============================================================================


def simulate_heavy_processing():
    """
    Simulates what your ComplexityOrchestrator.process_file() does.
    Each step takes time and produces logs.
    """
    steps = [
        ("🔧 Initializing LLM model...", 2),
        ("🧠 Loading neural network...", 2),
        ("📝 Parsing JavaScript code...", 1.5),
        ("🔍 Analyzing function: calculateTotal()", 2),
        ("🔍 Analyzing function: validateInput()", 2),
        ("🔍 Analyzing function: processData()", 1.5),
        ("📊 Computing complexity scores...", 2),
        ("✅ Analysis complete!", 1),
    ]

    logs = []
    for step_msg, duration in steps:
        logs.append(step_msg)
        time.sleep(duration)  # Simulate heavy work

    # Return fake results
    results = [
        ["calculateTotal()", 8, "12:45"],
        ["validateInput()", 3, "47:89"],
        ["processData()", 12, "91:156"],
    ]

    return logs, results


# ============================================================================
# VERSION 1: WITHOUT THREADING (Will freeze UI) ❌
# ============================================================================

def run_without_threading(code_input):
    """
    This tries to use yield, but since process_file() blocks,
    yields never execute until the very end.
    """
    yield "<div style='color:orange'>⏳ Starting analysis (NO THREADING)...</div>", None

    # This line BLOCKS for ~14 seconds!
    # While this runs, the yield above doesn't help - UI is frozen
    logs, results = simulate_heavy_processing()

    # These yields only execute AFTER processing completes
    logs_html = "<div style='color:orange'>⏳ Starting analysis (NO THREADING)...</div>"
    for log in logs:
        logs_html += f"<div style='color:green'>{log}</div>"

    logs_html += "<div style='color:red;font-weight:bold'>⚠️ Notice: All logs appeared at once!</div>"

    # Only now does the UI update (after 14 seconds of being frozen)
    yield logs_html, results


# ============================================================================
# VERSION 2: WITH THREADING (Streams beautifully) ✅
# ============================================================================


def run_with_threading(code_input):
    """
    This uses threading + queue to stream logs in real-time.
    """
    log_queue = queue.Queue()
    result_queue = queue.Queue()

    # Worker that runs in background
    def worker():
        steps = [
            ("🔧 Initializing LLM model...", 2),
            ("🧠 Loading neural network...", 2),
            ("📝 Parsing JavaScript code...", 1.5),
            ("🔍 Analyzing function: calculateTotal()", 2),
            ("🔍 Analyzing function: validateInput()", 2),
            ("🔍 Analyzing function: processData()", 1.5),
            ("📊 Computing complexity scores...", 2),
            ("✅ Analysis complete!", 1),
        ]

        for step_msg, duration in steps:
            log_queue.put(step_msg)  # Send to main thread
            time.sleep(duration)  # Simulate work

        # Send final results
        results = [
            ["calculateTotal()", 8, "12:45"],
            ["validateInput()", 3, "47:89"],
            ["processData()", 12, "91:156"],
        ]
        result_queue.put(results)

    # Start worker thread
    thread = threading.Thread(target=worker)
    thread.start()

    # Stream logs while worker runs
    logs_html = "<div style='color:blue;font-weight:bold'>🚀 Streaming logs in REAL-TIME:</div>"

    while thread.is_alive() or not log_queue.empty():
        # Check for new logs
        while not log_queue.empty():
            msg = log_queue.get_nowait()
            logs_html += f"<div style='color:green'>{msg}</div>"

        # Yield to update UI immediately!
        yield logs_html, None
        time.sleep(0.1)  # Small pause

    # Get final results
    results = result_queue.get()
    logs_html += "<div style='color:blue;font-weight:bold'>✨ Logs streamed smoothly!</div>"

    yield logs_html, results


# ============================================================================
# VERSION 3: HYBRID - Yield without threading but with manual breaks 🤔
# ============================================================================

def run_with_manual_yields(code_input):
    """
    This shows that yield CAN work without threading,
    BUT you need to structure your code to yield frequently.
    This is impractical for real heavy operations.
    """
    logs_html = "<div style='color:purple;font-weight:bold'>🔄 Manual yielding (no threading):</div>"

    steps = [
        ("🔧 Initializing LLM model...", 2),
        ("🧠 Loading neural network...", 2),
        ("📝 Parsing JavaScript code...", 1.5),
        ("🔍 Analyzing function: calculateTotal()", 2),
        ("🔍 Analyzing function: validateInput()", 2),
        ("🔍 Analyzing function: processData()", 1.5),
        ("📊 Computing complexity scores...", 2),
        ("✅ Analysis complete!", 1),
    ]

    # Manually yield after each step
    for step_msg, duration in steps:
        logs_html += f"<div style='color:purple'>{step_msg}</div>"
        yield logs_html, None  # Update UI
        time.sleep(duration)  # Simulate work

    results = [
        ["calculateTotal()", 8, "12:45"],
        ["validateInput()", 3, "47:89"],
        ["processData()", 12, "91:156"],
    ]

    logs_html += "<div style='color:purple;font-weight:bold'>⚠️ This works, but requires restructuring ALL your code!</div>"
    yield logs_html, results


# ============================================================================
# GRADIO INTERFACE
# ============================================================================

with gr.Blocks(title="Threading vs Non-Threading Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🧪 Threading Comparison Experiment
    
    **Try all three approaches and observe the differences:**
    
    1. **❌ Without Threading**: UI will FREEZE for ~14 seconds, then all logs appear at once
    2. **✅ With Threading**: Logs stream smoothly in real-time
    3. **🤔 Manual Yields**: Works but impractical for real-world use
    
    **Pro tip**: Try clicking other buttons while processing to test responsiveness!
    """)

    with gr.Row():
        code_input = gr.Code(
            language="javascript",
            label="Paste any code (not used, just for demo)",
            value="function example() {\n  return 'test';\n}",
            lines=5
        )

    gr.Markdown("---")

    # ========== VERSION 1: NO THREADING ==========
    gr.Markdown("## ❌ Version 1: WITHOUT Threading")
    with gr.Row():
        with gr.Column():
            btn1 = gr.Button(
                "🐌 Run WITHOUT Threading (Will Freeze!)", variant="stop")
        with gr.Column():
            logs1 = gr.HTML(value="<div style='color:gray'>Waiting...</div>")
            table1 = gr.Dataframe(
                headers=["Function", "Complexity", "Lines"], label="Results")

    gr.Markdown("---")

    # ========== VERSION 2: WITH THREADING ==========
    gr.Markdown("## ✅ Version 2: WITH Threading (Best Approach)")
    with gr.Row():
        with gr.Column():
            btn2 = gr.Button("🚀 Run WITH Threading (Smooth!)",
                             variant="primary")
        with gr.Column():
            logs2 = gr.HTML(value="<div style='color:gray'>Waiting...</div>")
            table2 = gr.Dataframe(
                headers=["Function", "Complexity", "Lines"], label="Results")

    gr.Markdown("---")

    # ========== VERSION 3: MANUAL YIELDS ==========
    gr.Markdown("## 🤔 Version 3: Manual Yields (Impractical)")
    with gr.Row():
        with gr.Column():
            btn3 = gr.Button("🔄 Run with Manual Yields", variant="secondary")
        with gr.Column():
            logs3 = gr.HTML(value="<div style='color:gray'>Waiting...</div>")
            table3 = gr.Dataframe(
                headers=["Function", "Complexity", "Lines"], label="Results")

    gr.Markdown("---")
    gr.Markdown("""
    ### 📊 Expected Results:
    
    | Approach | UI Responsive? | Logs Stream? | User Experience |
    |----------|----------------|--------------|-----------------|
    | ❌ No Threading | **Frozen** | No | Looks crashed |
    | ✅ Threading | **Yes** | **Yes** | Professional |
    | 🤔 Manual Yields | **Yes** | **Yes** | Works but messy |
    
    **The Threading Advantage**: Your actual `ComplexityOrchestrator.process_file()` is a black box 
    that takes minutes. You can't easily insert yields inside it, so threading is the ONLY practical solution!
    """)

    # Connect buttons
    btn1.click(fn=run_without_threading, inputs=[
               code_input], outputs=[logs1, table1])
    btn2.click(fn=run_with_threading, inputs=[
               code_input], outputs=[logs2, table2])
    btn3.click(fn=run_with_manual_yields, inputs=[
               code_input], outputs=[logs3, table3])

if __name__ == "__main__":
    demo.launch()
