(function () {
    const styleId = "dropdown-theme-overrides";
    const darkBg = "#111827";
    const darkHover = "#374151";
    const lightText = "#f9fafb";
    const borderColor = "#374151";

    function injectStyles() {
        let styleTag = document.getElementById(styleId);
        if (!styleTag) {
            styleTag = document.createElement("style");
            styleTag.id = styleId;
            document.head.appendChild(styleTag);
        }

        styleTag.textContent = `
            .Select-control,
            .Select-menu-outer,
            .Select-menu,
            .Select-option,
            .Select-placeholder,
            .Select-input > input,
            .Select-value,
            .Select-value-label,
            .Select--single > .Select-control .Select-value,
            .Select--multi .Select-value,
            .Select-option-label,
            .Select div,
            .Select span {
                background: #111827 !important;
                color: #f9fafb !important;
            }

            .Select-control,
            .Select.is-open > .Select-control,
            .Select.is-focused > .Select-control,
            .Select.has-value.Select--single > .Select-control {
                background: #111827 !important;
                border: 1px solid #374151 !important;
                box-shadow: none !important;
            }

            .Select-menu-outer,
            .Select-menu {
                background: #111827 !important;
                border: 1px solid #374151 !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35) !important;
            }

            .Select-option,
            .Select-option *,
            .VirtualizedSelectOption,
            .VirtualizedSelectOption * {
                background: #111827 !important;
                color: #f9fafb !important;
            }

            .Select-option.is-focused,
            .Select-option.is-focused *,
            .VirtualizedSelectFocusedOption,
            .VirtualizedSelectFocusedOption * {
                background: #374151 !important;
                color: #ffffff !important;
            }
        `;
    }

    function applyInlineDropdownTheme(root = document) {
        const dashSliderTrack = root.querySelectorAll(".dash-slider-track");
        dashSliderTrack.forEach((el) => {
            el.style.setProperty("background", "#1f2937", "important");
            el.style.setProperty("border-radius", "999px", "important");
            el.style.setProperty("height", "6px", "important");
        });

        const dashSliderRange = root.querySelectorAll(".dash-slider-range");
        dashSliderRange.forEach((el) => {
            el.style.setProperty("background", "#60a5fa", "important");
            el.style.setProperty("border-radius", "999px", "important");
        });

        const dashSliderThumb = root.querySelectorAll(".dash-slider-thumb");
        dashSliderThumb.forEach((el) => {
            el.style.setProperty("background", "#0b0f19", "important");
            el.style.setProperty("border", "2px solid #93c5fd", "important");
            el.style.setProperty("box-shadow", "0 0 0 2px rgba(96, 165, 250, 0.15)", "important");
        });

        const dashSliderMarks = root.querySelectorAll(
            ".dash-slider-mark, .dash-slider-mark-outside-selection"
        );
        dashSliderMarks.forEach((el) => {
            el.style.setProperty("color", "#cbd5e1", "important");
            el.style.setProperty("font-weight", "500", "important");
        });

        const dashSliderDots = root.querySelectorAll(
            ".dash-slider-dot, .dash-slider-dot-outside-selection"
        );
        dashSliderDots.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("border", "1px solid #6b7280", "important");
            el.style.setProperty("border-radius", "999px", "important");
        });

        const dashSliderTooltips = root.querySelectorAll(
            ".dash-slider-tooltip, .dash-slider-tooltip > div"
        );
        dashSliderTooltips.forEach((el) => {
            el.style.setProperty("background", "transparent", "important");
            el.style.setProperty("color", lightText, "important");
        });

        const dashSliderTooltipContent = root.querySelectorAll(".dash-slider-tooltip > div");
        dashSliderTooltipContent.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("border", "1px solid #374151", "important");
            el.style.setProperty("border-radius", "8px", "important");
            el.style.setProperty("box-shadow", "0 8px 24px rgba(0, 0, 0, 0.35)", "important");
            el.style.setProperty("padding", "4px 8px", "important");
            el.style.setProperty("font-weight", "600", "important");
            el.style.setProperty("line-height", "1.2", "important");
        });

        const dashSliderTooltipWrappers = root.querySelectorAll(".dash-slider-tooltip");
        dashSliderTooltipWrappers.forEach((el) => {
            el.style.setProperty("border", "none", "important");
            el.style.setProperty("box-shadow", "none", "important");
            el.style.setProperty("outline", "none", "important");
            el.style.setProperty("padding", "0", "important");
        });

        const sliderNumberInputs = root.querySelectorAll(
            ".dash-range-slider-input, .dash-input-container.dash-range-slider-input, .dash-slider-container input[type='number']"
        );
        sliderNumberInputs.forEach((el) => {
            el.style.setProperty("display", "none", "important");
        });

        const dashDropdowns = root.querySelectorAll(".dash-dropdown");
        dashDropdowns.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("color", lightText, "important");
            el.style.setProperty("border", `1px solid ${borderColor}`, "important");
            el.style.setProperty("box-shadow", "none", "important");
        });

        const dashContent = root.querySelectorAll(
            ".dash-dropdown-content, .dash-dropdown-options, .dash-dropdown-option, .dash-dropdown-search-container, .dash-dropdown-search"
        );
        dashContent.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("color", lightText, "important");
        });

        const dashHighlighted = root.querySelectorAll(
            ".dash-dropdown-option[data-highlighted]"
        );
        dashHighlighted.forEach((el) => {
            el.style.setProperty("background", darkHover, "important");
            el.style.setProperty("color", "#ffffff", "important");
        });

        const dashText = root.querySelectorAll(
            ".dash-dropdown-value, .dash-dropdown-placeholder, .dash-dropdown-value-count, .dash-dropdown-trigger-icon, .dash-dropdown-clear"
        );
        dashText.forEach((el) => {
            el.style.setProperty("color", lightText, "important");
            el.style.setProperty("fill", lightText, "important");
        });

        const controls = root.querySelectorAll(".Select-control");
        controls.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("color", lightText, "important");
            el.style.setProperty("border", `1px solid ${borderColor}`, "important");
            el.style.setProperty("box-shadow", "none", "important");
        });

        const menus = root.querySelectorAll(".Select-menu-outer, .Select-menu");
        menus.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("color", lightText, "important");
            el.style.setProperty("border", `1px solid ${borderColor}`, "important");
            el.style.setProperty("box-shadow", "0 8px 24px rgba(0, 0, 0, 0.35)", "important");
        });

        const options = root.querySelectorAll(".Select-option, .VirtualizedSelectOption");
        options.forEach((el) => {
            el.style.setProperty("background", darkBg, "important");
            el.style.setProperty("color", lightText, "important");
        });

        const focusedOptions = root.querySelectorAll(
            ".Select-option.is-focused, .VirtualizedSelectFocusedOption"
        );
        focusedOptions.forEach((el) => {
            el.style.setProperty("background", darkHover, "important");
            el.style.setProperty("color", "#ffffff", "important");
        });

        const textNodes = root.querySelectorAll(
            ".Select-placeholder, .Select-value-label, .Select-input input, .Select-option *, .VirtualizedSelectOption *"
        );
        textNodes.forEach((el) => {
            el.style.setProperty("color", lightText, "important");
        });

        const arrows = root.querySelectorAll(".Select-arrow, .Select-arrow-zone, .Select-clear-zone");
        arrows.forEach((el) => {
            el.style.setProperty("color", lightText, "important");
            el.style.setProperty("border-top-color", lightText, "important");
        });
    }

    function watchDropdowns() {
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                if (mutation.type === "childList") {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {
                            applyInlineDropdownTheme(node);
                        }
                    });
                }

                if (mutation.type === "attributes" && mutation.target.nodeType === 1) {
                    applyInlineDropdownTheme(mutation.target);
                }
            }
        });

        observer.observe(document.documentElement, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ["class"]
        });
    }

    injectStyles();
    applyInlineDropdownTheme();
    watchDropdowns();

    window.addEventListener("load", function () {
        injectStyles();
        applyInlineDropdownTheme();
    });

    document.addEventListener("DOMContentLoaded", function () {
        injectStyles();
        applyInlineDropdownTheme();
    });
})();
