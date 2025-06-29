function setupMonacoEditor({ selector = "editor", language = "cpp", theme = "one-dark-pro", onReady }) {
    const setup = () => {
        // Load and apply custom theme if provided
        fetch(`/static/monaco-themes/${theme}.json`)
            .then(res => res.json())
            .then(themeData => {
                monaco.editor.defineTheme(theme, themeData);
                monaco.editor.setTheme(theme);

                const editor = monaco.editor.create(document.getElementById(selector), {
                    value: "",
                    language: language === "cpp" ? "cpp" : language,
                    theme: theme,
                    automaticLayout: true,
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    scrollbar: {
                        verticalScrollbarSize: 4,
                        horizontalScrollbarSize: 4,
                        useShadows: false,
                    },
                });

                if (typeof onReady === "function") {
                    onReady(editor, monaco);
                }
            });
    };

    if (window.monaco && typeof monaco.editor !== "undefined") {
        // ✅ Monaco is already available
        setup();
    } else {
        // 🌀 Monaco not loaded yet — load using AMD loader
        if (!window._monacoLoading) {
            window._monacoLoading = true;
            require.config({
                paths: {
                    vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.34.1/min/vs"
                }
            });
            require(["vs/editor/editor.main"], setup);
        } else {
            // If loading is already in progress, wait for it
            const checkReady = setInterval(() => {
                if (window.monaco && typeof monaco.editor !== "undefined") {
                    clearInterval(checkReady);
                    setup();
                }
            }, 100);
        }
    }
}
  