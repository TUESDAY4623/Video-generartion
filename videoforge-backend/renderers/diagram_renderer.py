"""Dynamic Diagram, Flowchart, and Visual Architecture Renderer for VideoForge.

Purpose:
--------
Transforms high-level semantic script concepts into crisp, modern, 1080p visual scenes.
Supports:
1. Mermaid.js Flowcharts, Architecture & Sequence Diagrams.
2. Animated Step-by-Step Pipeline Flows.
3. Feature & Technology Comparison Grids.
4. Syntax-highlighted Code Walkthroughs with active line focus.
5. Glassmorphic Concept Cards with Glowing Neon Accents.

File Role:
----------
Visual Asset & Scene Rendering Engine
"""

from __future__ import annotations

import html
import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VisualSceneSpec:
    """Specification for a dynamically rendered visual scene."""
    scene_id: str
    visual_type: str  # 'diagram', 'process_flow', 'comparison', 'code_walkthrough', 'concept_card'
    title: str
    subtitle: Optional[str] = None
    diagram_code: Optional[str] = None  # Mermaid syntax or node-edge spec
    steps: List[Dict[str, str]] = field(default_factory=list)
    comparison_items: List[Dict[str, Any]] = field(default_factory=list)
    code_snippet: Optional[str] = None
    code_language: str = "python"
    highlight_lines: List[int] = field(default_factory=list)
    key_points: List[str] = field(default_factory=list)
    accent_color: str = "#7c83ff"
    icon: str = "cpu"


class DiagramRenderer:
    """Renders dynamic semantic visual scenes into standalone 1080p HTML/SVG visuals."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("./rendered_scenes")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_scene_html(self, spec: VisualSceneSpec) -> str:
        """Generate self-contained 1920x1080 HTML with embedded animations and styling."""
        content_html = ""

        if spec.visual_type == "diagram":
            content_html = self._render_mermaid_diagram(spec)
        elif spec.visual_type == "process_flow":
            content_html = self._render_process_flow(spec)
        elif spec.visual_type == "comparison":
            content_html = self._render_comparison(spec)
        elif spec.visual_type == "code_walkthrough":
            content_html = self._render_code_block(spec)
        else:
            content_html = self._render_concept_card(spec)

        return self._wrap_in_cinematic_template(spec, content_html)

    def _render_mermaid_diagram(self, spec: VisualSceneSpec) -> str:
        """Render a Mermaid.js diagram container."""
        mermaid_code = spec.diagram_code or "graph LR\n  A[Input] --> B[Process] --> C[Output]"
        # Clean mermaid code
        clean_code = html.escape(mermaid_code.strip())
        return f"""
        <div class="diagram-wrapper">
            <div class="mermaid">
{clean_code}
            </div>
        </div>
        """

    def _render_process_flow(self, spec: VisualSceneSpec) -> str:
        """Render horizontal / multi-step animated process flow."""
        steps_html = []
        for idx, step in enumerate(spec.steps):
            num = idx + 1
            stitle = html.escape(step.get("title", f"Step {num}"))
            sdesc = html.escape(step.get("desc", ""))
            sicon = step.get("icon", "arrow-right")
            
            steps_html.append(f"""
            <div class="step-card" style="animation-delay: {idx * 0.25}s">
                <div class="step-badge">{num}</div>
                <div class="step-title">{stitle}</div>
                <div class="step-desc">{sdesc}</div>
            </div>
            """)

        steps_joined = "".join(steps_html)
        return f"""
        <div class="process-flow-container">
            {steps_joined}
        </div>
        """

    def _render_comparison(self, spec: VisualSceneSpec) -> str:
        """Render side-by-side comparison cards."""
        cards_html = []
        for idx, item in enumerate(spec.comparison_items):
            title = html.escape(item.get("title", f"Option {idx+1}"))
            subtitle = html.escape(item.get("subtitle", ""))
            points = item.get("points", [])
            points_li = "".join([f"<li><span class='check-icon'>✓</span> {html.escape(p)}</li>" for p in points])
            is_winner = item.get("highlight", False)
            winner_class = "card-highlight" if is_winner else ""

            cards_html.append(f"""
            <div class="comparison-card {winner_class}" style="animation-delay: {idx * 0.2}s">
                <h3 class="comparison-title">{title}</h3>
                <p class="comparison-sub">{subtitle}</p>
                <ul class="comparison-list">
                    {points_li}
                </ul>
            </div>
            """)

        return f"""
        <div class="comparison-grid">
            {"".join(cards_html)}
        </div>
        """

    def _render_code_block(self, spec: VisualSceneSpec) -> str:
        """Render syntax-styled code block with animated line highlight focus."""
        code_lines = (spec.code_snippet or "# Code demonstration").strip().split("\n")
        lines_html = []
        for idx, line in enumerate(code_lines, start=1):
            is_highlighted = idx in spec.highlight_lines
            hl_class = "line-active" if is_highlighted else ""
            escaped_line = html.escape(line) or "&nbsp;"
            lines_html.append(f"""
            <div class="code-line {hl_class}">
                <span class="line-num">{idx:02d}</span>
                <span class="line-content">{escaped_line}</span>
            </div>
            """)

        return f"""
        <div class="code-editor-container">
            <div class="code-editor-header">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
                <span class="editor-title">{spec.code_language.upper()} Walkthrough</span>
            </div>
            <div class="code-body">
                {"".join(lines_html)}
            </div>
        </div>
        """

    def _render_concept_card(self, spec: VisualSceneSpec) -> str:
        """Render primary topic concept card with glowing bullet points."""
        points_html = []
        for idx, pt in enumerate(spec.key_points):
            points_html.append(f"""
            <div class="concept-point" style="animation-delay: {0.3 + (idx * 0.15)}s">
                <span class="point-glow-dot"></span>
                <span class="point-text">{html.escape(pt)}</span>
            </div>
            """)

        return f"""
        <div class="concept-container">
            <div class="concept-glass-card">
                <div class="concept-points-list">
                    {"".join(points_html)}
                </div>
            </div>
        </div>
        """

    def _wrap_in_cinematic_template(self, spec: VisualSceneSpec, inner_content: str) -> str:
        """Wraps inner content in a 1920x1080 cinematic styling container."""
        title = html.escape(spec.title or "")
        subtitle = html.escape(spec.subtitle or "")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;600;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({{
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {{
            darkMode: true,
            background: '#0a0a20',
            primaryColor: '{spec.accent_color}',
            primaryTextColor: '#ffffff',
            primaryBorderColor: '{spec.accent_color}',
            lineColor: '#00d4aa',
            secondaryColor: '#1a1a4e',
            tertiaryColor: '#101030'
        }}
    }});
</script>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        width: 1920px;
        height: 1080px;
        background: #050514;
        background-image: radial-gradient(ellipse at 50% 0%, #1a1a4e 0%, #0a0a1a 60%, #050514 100%);
        color: #e4e4f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        overflow: hidden;
        position: relative;
        display: flex;
        flex-direction: column;
        justifyContent: space-between;
        padding: 70px 100px;
    }}
    
    /* Background Grid & Ambient Glow */
    .ambient-glow {{
        position: absolute;
        top: -150px;
        left: 50%;
        transform: translateX(-50%);
        width: 800px;
        height: 400px;
        background: radial-gradient(circle, {spec.accent_color}33 0%, transparent 70%);
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
    }}

    /* Header */
    .header-container {{
        position: relative;
        z-index: 10;
        animation: fadeInDown 0.8s ease-out both;
    }}
    .scene-title {{
        font-size: 54px;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #ffffff 40%, #a4b0be 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }}
    .scene-subtitle {{
        font-size: 24px;
        color: #8888aa;
        margin-top: 10px;
        font-weight: 400;
    }}

    /* Content Stage */
    .stage-container {{
        position: relative;
        z-index: 10;
        flex: 1;
        display: flex;
        align-items: center;
        justifyContent: center;
        margin: 40px 0;
    }}

    /* Diagram Styles */
    .diagram-wrapper {{
        background: rgba(15, 15, 40, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 50px 70px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
        transform: scale(1.15);
    }}
    .mermaid {{
        font-size: 20px;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Process Flow Styles */
    .process-flow-container {{
        display: flex;
        gap: 32px;
        width: 100%;
        justify-content: center;
    }}
    .step-card {{
        flex: 1;
        max-width: 380px;
        background: rgba(15, 15, 40, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 36px 30px;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    .step-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: {spec.accent_color};
        color: white;
        font-weight: 800;
        font-size: 22px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px {spec.accent_color}88;
    }}
    .step-title {{
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }}
    .step-desc {{
        font-size: 18px;
        color: #9aa0a6;
        line-height: 1.6;
    }}

    /* Comparison Grid */
    .comparison-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 40px;
        width: 100%;
        max-width: 1500px;
    }}
    .comparison-card {{
        background: rgba(15, 15, 40, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.4);
        animation: scaleIn 0.8s ease both;
    }}
    .card-highlight {{
        border: 2px solid {spec.accent_color};
        box-shadow: 0 0 50px {spec.accent_color}44, 0 15px 45px rgba(0,0,0,0.5);
    }}
    .comparison-title {{
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
    }}
    .comparison-sub {{
        font-size: 18px;
        color: #8888aa;
        margin-top: 6px;
        margin-bottom: 28px;
    }}
    .comparison-list {{
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}
    .comparison-list li {{
        font-size: 20px;
        color: #d1d5db;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .check-icon {{
        color: #00d4aa;
        font-weight: 900;
    }}

    /* Code Editor */
    .code-editor-container {{
        width: 100%;
        max-width: 1400px;
        background: #0a0a20;
        border: 1px solid {spec.accent_color}88;
        border-radius: 20px;
        box-shadow: 0 0 50px {spec.accent_color}33, 0 20px 60px rgba(0,0,0,0.6);
        overflow: hidden;
        animation: zoomIn 0.7s ease both;
    }}
    .code-editor-header {{
        background: #101030;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }}
    .dot {{ width: 14px; height: 14px; border-radius: 50%; display: inline-block; }}
    .red {{ background: #ff5f56; }}
    .yellow {{ background: #ffbd2e; }}
    .green {{ background: #27c93f; }}
    .editor-title {{
        margin-left: 16px;
        font-size: 16px;
        font-weight: 600;
        color: #8888aa;
        font-family: 'JetBrains Mono', monospace;
    }}
    .code-body {{
        padding: 30px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        line-height: 1.8;
    }}
    .code-line {{
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 4px 12px;
        border-radius: 8px;
    }}
    .line-num {{
        color: #555577;
        font-size: 18px;
        user-select: none;
        width: 32px;
    }}
    .line-content {{ color: #a6e3a1; }}
    .line-active {{
        background: {spec.accent_color}22;
        border-left: 4px solid {spec.accent_color};
        box-shadow: 0 0 20px {spec.accent_color}33;
    }}

    /* Concept Card */
    .concept-container {{
        width: 100%;
        max-width: 1400px;
    }}
    .concept-glass-card {{
        background: rgba(15, 15, 40, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 50px 60px;
        backdrop-filter: blur(25px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .concept-points-list {{
        display: flex;
        flex-direction: column;
        gap: 28px;
    }}
    .concept-point {{
        display: flex;
        align-items: center;
        gap: 24px;
        font-size: 28px;
        font-weight: 600;
        color: #ffffff;
        animation: fadeInLeft 0.6s ease both;
    }}
    .point-glow-dot {{
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: {spec.accent_color};
        box-shadow: 0 0 25px {spec.accent_color};
    }}

    /* Animations */
    @keyframes fadeInDown {{
        from {{ opacity: 0; transform: translateY(-30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes scaleIn {{
        from {{ opacity: 0; transform: scale(0.92); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes zoomIn {{
        from {{ opacity: 0; transform: scale(0.95); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes fadeInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
</style>
</head>
<body>
    <div class="ambient-glow"></div>
    <div class="header-container">
        <h1 class="scene-title">{title}</h1>
        {f'<p class="scene-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    
    <div class="stage-container">
        {inner_content}
    </div>
</body>
</html>
"""

    def save_scene_html(self, spec: VisualSceneSpec, output_filename: str) -> Path:
        """Render and save scene HTML to destination path."""
        html_code = self.render_scene_html(spec)
        out_path = self.output_dir / output_filename
        out_path.write_text(html_code, encoding="utf-8")
        logger.info("Saved dynamic scene visual: %s", out_path)
        return out_path
