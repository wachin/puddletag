# Translation Testing

This guide explains how to test the bundled puddletag translations from a source checkout.

## Debian Tools

Install the translation tools from Debian repositories:

```bash
sudo apt install linguist-qt6 pyqt6-dev-tools
```

On Debian, the Qt 6 Linguist tools may live under `/usr/lib/qt6/bin/`:

```bash
/usr/lib/qt6/bin/linguist
/usr/lib/qt6/bin/lrelease
/usr/lib/qt6/bin/lupdate
pylupdate6
```

If you use them often, add aliases in your shell:

```bash
alias linguist-qt6=/usr/lib/qt6/bin/linguist
alias lrelease-qt6=/usr/lib/qt6/bin/lrelease
alias lupdate-qt6=/usr/lib/qt6/bin/lupdate
```

## Existing Translation Files

Translation sources and compiled catalogs are stored in:

```text
puddlestuff/translations/
```

Each language normally has two files:

- `puddletag_LANG.ts`: editable source file for Qt Linguist.
- `puddletag_LANG.qm`: compiled translation catalog used by puddletag.

List the available compiled catalogs:

```bash
find puddlestuff/translations -name 'puddletag_*.qm' | sort
```

## Quick Runtime Test

Launch puddletag with a specific compiled catalog:

```bash
./puddletag gui --langfile puddlestuff/translations/puddletag_es_ES.qm
```

Replace `puddletag_es_ES.qm` with any other `.qm` file to test another language.

Expected behavior:

- The terminal prints the selected locale, for example `Locale: es_ES`.
- Menus and dialogs should appear translated where that catalog has translated strings.
- Untranslated or outdated strings may still appear in English.

## Test Every Bundled Language

Use this shell loop to launch each bundled translation one at a time:

```bash
for qm in puddlestuff/translations/puddletag_*.qm; do
    echo "Testing $qm"
    ./puddletag gui --langfile "$qm"
done
```

Close puddletag after each launch to continue to the next language.

## Automatic Locale Test

To test automatic language selection, set locale variables before launching:

```bash
LANG=es_EC.UTF-8 LC_ALL= ./puddletag
```

For Spanish regional locales such as `es_EC`, puddletag should fall back to the bundled `es_ES` catalog and print:

```text
Locale: es_ES
```

If `LC_ALL=C.UTF-8` is set by the shell or test environment, puddletag now also checks `LANG`, `LC_MESSAGES`, and `LANGUAGE` as fallbacks.

## Editing And Releasing A Translation

Open a `.ts` file in Qt Linguist:

```bash
/usr/lib/qt6/bin/linguist puddlestuff/translations/puddletag_es_ES.ts
```

After editing, compile the `.qm` catalog either from Qt Linguist with `File -> Release`, or from the terminal:

```bash
/usr/lib/qt6/bin/lrelease puddlestuff/translations/puddletag_es_ES.ts
```

Then test the generated `.qm` file:

```bash
./puddletag gui --langfile puddlestuff/translations/puddletag_es_ES.qm
```

## Updating Translation Source Strings

When application strings change, update the `.ts` files with:

```bash
python3 update_translation.py es_ES
```

`update_translation.py` uses `pylupdate6`, provided by the Debian `pyqt6-dev-tools` package.

After updating, review the `.ts` file in Qt Linguist, release a new `.qm`, and rerun the runtime checks above.
