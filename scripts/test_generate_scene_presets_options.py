import re
import unittest
from pathlib import Path

from generate_scene_presets_options import (
    BEGIN_MARKER,
    END_MARKER,
    build_options,
    render_options_yaml,
    splice_generated_block,
)


class BuildOptionsTests(unittest.TestCase):
    def test_orders_by_category_declaration_order_preserving_position_within_category(self):
        data = {
            "categories": [
                {"id": "cat-party", "name": "Party vibes"},
                {"id": "cat-cozy", "name": "Cozy"},
            ],
            "presets": [
                {"id": "id-rio", "categoryId": "cat-party", "name": "Rio"},
                {"id": "id-warm", "categoryId": "cat-cozy", "name": "Warm embrace"},
                {"id": "id-miami", "categoryId": "cat-party", "name": "Miami"},
            ],
        }

        options = build_options(data)

        self.assertEqual(
            options,
            [
                {"label": "Party vibes — Rio", "value": "id-rio"},
                {"label": "Party vibes — Miami", "value": "id-miami"},
                {"label": "Cozy — Warm embrace", "value": "id-warm"},
            ],
        )

    def test_unknown_category_falls_back_to_other(self):
        data = {
            "categories": [],
            "presets": [{"id": "id-x", "categoryId": "missing", "name": "X"}],
        }

        options = build_options(data)

        self.assertEqual(options, [{"label": "Other — X", "value": "id-x"}])


class RenderOptionsYamlTests(unittest.TestCase):
    def test_renders_quoted_label_value_pairs_at_given_indent(self):
        options = [
            {"label": 'Cozy — "Warm" embrace', "value": "abc-123"},
            {"label": "Party vibes — Miami", "value": "def-456"},
        ]

        rendered = render_options_yaml(options, indent=4)

        self.assertEqual(
            rendered,
            '    - label: "Cozy — \\"Warm\\" embrace"\n'
            '      value: "abc-123"\n'
            '    - label: "Party vibes — Miami"\n'
            '      value: "def-456"',
        )


class SpliceGeneratedBlockTests(unittest.TestCase):
    def test_replaces_content_between_markers_preserving_indent(self):
        file_text = (
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            "      - label: \"stale\"\n"
            "        value: \"stale-id\"\n"
            "      # END generated scene_presets options\n"
            "after\n"
        )
        options = [{"label": "Cozy — Warm embrace", "value": "id-warm"}]

        result = splice_generated_block(file_text, options)

        self.assertEqual(
            result,
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            '      - label: "Cozy — Warm embrace"\n'
            '        value: "id-warm"\n'
            "      # END generated scene_presets options\n"
            "after\n",
        )

    def test_handles_empty_body_between_adjacent_markers(self):
        # This is the state Task 2 hits on the first run: the markers are
        # scaffolded in with nothing between them yet.
        file_text = (
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            "      # END generated scene_presets options\n"
            "after\n"
        )
        options = [{"label": "Cozy — Warm embrace", "value": "id-warm"}]

        result = splice_generated_block(file_text, options)

        self.assertEqual(
            result,
            "before\n"
            "    options:\n"
            "      # BEGIN generated scene_presets options\n"
            '      - label: "Cozy — Warm embrace"\n'
            '        value: "id-warm"\n'
            "      # END generated scene_presets options\n"
            "after\n",
        )

    def test_missing_markers_raises_value_error(self):
        with self.assertRaises(ValueError):
            splice_generated_block("no markers here", [])


class GeneratedBlocksStayInSyncTests(unittest.TestCase):
    def test_rom001_and_rdm002_generated_blocks_are_identical(self):
        repo_root = Path(__file__).resolve().parent.parent
        rom001 = (
            repo_root / "controllers" / "hue_smart_button_rom001" / "hue_smart_button_rom001.yaml"
        ).read_text()
        rdm002 = (
            repo_root / "controllers" / "hue_tap_dial_rdm002" / "hue_tap_dial_rdm002.yaml"
        ).read_text()

        def extract_block(text):
            match = re.search(
                re.escape(BEGIN_MARKER) + r"\n(.*?)\n[ \t]*" + re.escape(END_MARKER),
                text,
                re.DOTALL,
            )
            self.assertIsNotNone(match, "markers not found")
            return match.group(1)

        self.assertEqual(extract_block(rom001), extract_block(rdm002))


if __name__ == "__main__":
    unittest.main()
