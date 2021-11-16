from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import (
    RenderContext,
    RenderTreeNode,
)
from mdformat.renderer.typing import Render
from mdit_py_plugins.footnote import footnote_plugin


def make_render_children(separator: str) -> Render:
    def render_children(
        node: RenderTreeNode,
        context: RenderContext,
    ) -> str:
        return separator.join(child.render(context) for child in node.children)

    return render_children


def render_footnote(node: RenderTreeNode, context: RenderContext) -> str:
    """Render the footnotes body."""
    tight_list = all(
        child.type != "paragraph" or child.hidden for child in node.children
    )
    label = node.meta.get("label", node.meta.get("id"))
    marker = f"[^{label}]: "
    indent_width = len(marker)
    context.env["indent_width"] += indent_width
    try:
        text = make_render_children("\n\n")(node, context)
        lines = text.splitlines()
        if not lines:
            return ":"
        indented_lines = [f"{marker}{lines[0]}"] + [
            f"{' '*indent_width}{line}" if line else "" for line in lines[1:]
        ]
        indented_lines = ("" if tight_list else "\n") + "\n".join(indented_lines)
        next_sibling = node.next_sibling
        return indented_lines + (
            "" if (next_sibling and next_sibling.type == "footnote") else ""
        )
    finally:
        context.env["indent_width"] -= indent_width


def render_footnote_ref(node: RenderTreeNode, context: RenderContext) -> str:
    ref_label = node.meta.get("label")
    return f"[^{ref_label}]"


def render_footnote_inline(node: RenderTreeNode, context: RenderContext) -> str:
    id = node.meta.get("id")
    return f"[^{id}]"


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the parser, e.g. by adding a plugin: `mdit.use(myplugin)`"""
    mdit.use(footnote_plugin)


RENDERERS: Mapping[str, Render] = {
    "footnote_ref": render_footnote_ref,
    "footnote_inline": render_footnote_inline,
    "footnote_block": make_render_children(""),
    "footnote": render_footnote,
}
