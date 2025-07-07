// Utility: Easy element selectors
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ---------- Monaco Editor Setup ----------
function setupMonaco() {
    require.config({ paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs" } });

    require(["vs/editor/editor.main"], () => {
        const editor = monaco.editor.create($("#editor"), {
            value: "",
            language: "cpp",
            theme: "vs-dark",
            automaticLayout: true,
            minimap: { enabled: false },
            scrollbar: {
                verticalScrollbarSize: 4,   // Shrink vertical scroll width
                horizontalScrollbarSize: 4, // Shrink horizontal scroll height
                arrowSize: 4                // Shrink arrow buttons too
            },
        });

        const boilerplate = {
            java: `import java.util.*;\n\npublic class Main {\n  public static void main(String[] args) {\n    // Your code here\n\n\n  }\n}`,
            python: `def main():\n    # Your code here\n\n\n    pass\n\nif __name__ == "__main__":\n    main()`,
            cpp: `#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    // Your code here\n\n\n    return 0;\n}`,
            c: `#include <stdio.h>\n\nint main() {\n    // Your code here\n\n\n    return 0;\n}`
        };

        const langSel = $("#language");
        langSel.addEventListener("change", () => {
            const lang = langSel.value;
            editor.setValue(boilerplate[lang] || "");
            monaco.editor.setModelLanguage(editor.getModel(), lang === "cpp" ? "cpp" : lang);
        });
        langSel.dispatchEvent(new Event("change"));

        window.monacoEditor = editor;
    });
}

// ---------- AI Assist Dropdown ----------
function setupAIAssist() {
    const aiBtn = $("#aiAssistBtn");
    const menu = $("#aiAssistMenu");
    const dropdownItems = $$(".ai-option");
    const modal = $("#ai-response-modal");
    const modalBody = $("#ai-modal-body");

    aiBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        menu.classList.toggle("show");
    });

    document.addEventListener("click", (e) => {
        if (!e.target.closest(".ai-assist-dropdown")) {
            menu.classList.remove("show");
        }
    });

    dropdownItems.forEach(item => {
        item.addEventListener("click", async (e) => {
            e.preventDefault();
            menu.classList.remove("show");

            const action = item.dataset.action;
            const editor = window.monacoEditor;
            const code = editor ? editor.getValue() : "";

            const pd = $("#problem-data").dataset;
            const loadingText = {
                debugger: "🛠️ Analyzing your code for bugs...",
                hints: "💡 Thinking of beginner-friendly hints...",
                explain: "📖 Breaking it down step-by-step...",
                suggestions: "✨ Reviewing your code for improvements..."
            };

            modalBody.innerHTML = `<p>${loadingText[action] || "🤖 Thinking..."}</p>`;
            modal.classList.remove("hidden");

            const prompt = buildPrompt(action, pd, code);

            const response = await fetch(window.ai_assist_url || "/ai-assist/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                },
                body: JSON.stringify({ action, prompt, code })
            });

            const json = await response.json();
            if (json.result) {
                try {
                    modalBody.innerHTML = `<div class="markdown-body">${marked.parse(json.result)}</div>`;
                } catch {
                    modalBody.innerHTML = `<pre>${json.result}</pre>`;
                }
            } else {
                modalBody.innerHTML = `<p>⚠️ AI Error: ${json.error || "Unknown error."}</p>`;
            }
        });
    });

    window.closeAIModal = () => modal.classList.add("hidden");
}

function buildPrompt(action, pd, code) {
    if (action === "debugger") {
        return `
You are a code debugger. The user is solving this problem:

Title: ${pd.title}
Description: ${pd.description}
Input Format: ${pd.input}
Output Format: ${pd.output}
Constraints: ${pd.constraints}
Sample Input: ${pd.sampleInput}
Sample Output: ${pd.sampleOutput}

Below is their code:
${code}

Your task:
1. Identify logic, syntax, or runtime issues.
2. Suggest corrections, but do not rewrite the full code.
3. Limit to 300 words.
    `.trim();
    }

    if (action === "hints") {
        return `
You are a programming tutor. Provide 2–3 beginner-friendly hints.

Problem:
Title: ${pd.title}
Description: ${pd.description}
Input Format: ${pd.input}
Output Format: ${pd.output}
Constraints: ${pd.constraints}

Each hint must be under 30 words. Do not include the solution.
    `.trim();
    }

    if (action === "explain") {
        return `
You are a coding mentor. Explain this problem to a beginner.

Problem:
Title: ${pd.title}
Description: ${pd.description}
Input Format: ${pd.input}
Output Format: ${pd.output}
Constraints: ${pd.constraints}
Sample Input: ${pd.sampleInput}
Sample Output: ${pd.sampleOutput}

Use clear language. Explain step-by-step. Keep it under 300 words.
    `.trim();
    }

    if (action === "suggestions") {
        return `
You are a code reviewer. Analyze this solution.

Problem:
Title: ${pd.title}
Description: ${pd.description}
Input Format: ${pd.input}
Output Format: ${pd.output}

User's code:
${code}

List a maximum of 6 suggestions. Focus on logic, style, or edge cases. Keep it under 300 words.
    `.trim();
    }

    return "";
}

// ---------- Run Button Logic ----------
function setupRunButton() {
    $("#run-button").addEventListener("click", async () => {
        const editor = window.monacoEditor;
        const lang = $("#language").value;
        const code = editor.getValue();
        const input = $("#custom-input").value;

        const data = new FormData();
        data.append("code", code);
        data.append("language", lang);
        data.append("custom_input", input);

        const response = await fetch(window.run_code_url || "/run-code/", {
            method: "POST",
            headers: { "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value },
            body: data
        });

        const json = await response.json();
        $("#custom-output").value = json.output || json.error || json.details || "No response.";
        activateTab("output");
    });
}

// ---------- Tabs (Custom I/O) ----------
function setupTabs() {
    $$(".custom-io-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            $$(".custom-io-tab").forEach(t => t.classList.remove("active"));
            $$(".custom-io-panel").forEach(p => p.classList.remove("active"));
            tab.classList.add("active");
            $(`#${tab.dataset.tab}-panel`).classList.add("active");
        });
    });
}

function activateTab(tabName) {
    $$(".custom-io-tab").forEach(t => t.classList.remove("active"));
    $$(".custom-io-panel").forEach(p => p.classList.remove("active"));
    $(`.custom-io-tab[data-tab="${tabName}"]`).classList.add("active");
    $(`#${tabName}-panel`).classList.add("active");
}

// ---------- Resizer ----------
function setupResizer() {
    const resizer = $("#resizer");
    const leftPane = $(".left-pane");

    let isDragging = false;

    resizer.onmousedown = () => {
        isDragging = true;
        document.body.style.cursor = "ew-resize";
    };

    document.onmousemove = (e) => {
        if (!isDragging) return;
        const containerLeft = $(".split-container").offsetLeft;
        let newWidth = e.clientX - containerLeft;
        if (newWidth > 250 && newWidth < window.innerWidth * 0.7) {
            leftPane.style.width = newWidth + "px";
        }
    };

    document.onmouseup = () => {
        isDragging = false;
        document.body.style.cursor = "";
    };
}

// ---------- Form Submission ----------
function setupFormSubmit() {
    $("#submission-form").addEventListener("submit", () => {
        $("#hidden-code").value = window.monacoEditor.getValue();
    });
}

// ---------- Main ----------
document.addEventListener("DOMContentLoaded", () => {
    setupMonaco();
    setupAIAssist();
    setupRunButton();
    setupTabs();
    setupResizer();
    setupFormSubmit();
});
