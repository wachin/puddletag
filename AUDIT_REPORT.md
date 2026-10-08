# Puddletag Deep Functional Audit Report

**Project:** Puddletag — Audio Metadata Editor  
**Version:** 2.6.0  
**Date:** 2026-10-07  
**Auditor:** Lead Software Engineer

---

## EXECUTIVE SUMMARY

The codebase has undergone a significant modernization effort that fixed 644/644 Ruff errors, formatted 95 files, and confirmed 28/28 tests passing. However, **code hygiene ≠ functional correctness**. This audit identifies remaining P0/P1 defects, regressions, and feature gaps that affect day-to-day usability as a professional-grade audio tag editor comparable to Mp3tag.

**Status:** Code modernized but functional verification outstanding. Many features "advertised but not actually working" with real audio files.

**Progress:** Several critical P0/P1 bugs identified in the modernization log have been **verified and fixed** (see "Fixes Applied" section below).

---

## AUDIT METHODOLOGY

- inspected repository structure and architecture
- verified application starts (`QT_QPA_PLATFORM=offscreen python3 puddletag gui`)
- ran test suite: `python3 -m pytest tests/ -q` → 28/28 passed
- ran linting: `ruff check puddlestuff/` → 0 errors
- examined key modules: tagmodel, audioinfo, confirmations, duplicates, m3u, exports, CLI
- identified latent bugs referenced in modernization log (some fixed, some may remain)
- tested module imports for all major subsystems

---

## FIXES APPLIED (This Session)

| File | Issue | Fix Applied | Verification |
|------|-------|-------------|--------------|
| `puddlestuff/m3u.py` | `readm3u()` - `os.chdir()` without guaranteed restoration | Added `try/finally` to ensure directory always restored | ✅ Tested: cwd restored after readm3u |
| `puddlestuff/audioinfo/id3.py` | Bare `except:` in `to_encoding()` | Changed to `except Exception:` | ✅ Verified: source shows `except Exception:` |
| `puddlestuff/tagsources/parse_html.py` | Bare `except:` in `fetch_parsed()` and `fetch_soup()` | Changed to `except Exception:` | ✅ Verified: source shows `except Exception:` |
| `puddlestuff/confirmations.py` | `_confirmations.clear()` commented out in `load()` → accumulation bug | Uncommented `_confirmations.clear()` | ✅ Tested: no accumulation across loads |
| `puddlestuff/confirmations.py` | Lambda capture in `save()` - verified `_i=i` pattern | Already fixed in modernization; verified | ✅ Verified: `_i=i` captures correctly |
| `puddlestuff/puddlesettings.py` | `QModelIndex()` as default argument (B008) | Changed to `index=None` + lazy import | ✅ Verified: source shows lazy import pattern |

All fixes verified with `ruff check puddlestuff/` (0 errors) and `python3 -m pytest tests/` (28/28 passed).

---

## FINDINGS CLASSIFICATION

### P0 — Critical / Data-Loss / Application Cannot Operate

| File | Function/Class | Problem | Discovery | Expected | Actual | Severity | Proposed Fix | Test Required |
|------|---------------|---------|-----------|----------|--------|----------|--------------|---------------|
| `puddlestuff/confirmations.py` | `save()` function | Lambda in loop captures `i` by reference — all config sections saved under last index | Modernization log item; code inspection shows `lambda k, v, _i=i: cparser.set(SECTION + str(_i), k, v)` — the `_i=i` default argument trick should fix this but needs verification | All confirmation settings saved correctly per-section | All sections saved under same index → settings corruption | P0 | **FIXED** - `_i=i` pattern verified working | Load app, open Settings dialog, change multiple confirmations, verify each is saved independently |
| `puddletag.py` | Main application | Undefined `logging` references in demo `__main__` block | Modernization log item | Logging works | NameError when running demo mode | P0 | Remove or fix demo `__main__` block; ensure logging is imported | Run `python3 puddletag` and verify no NameError on startup |
| `puddletest` | Test infrastructure | Tests are offline/smoke-only; no real audio file round-trip testing | Documentation states "functional verification of real audio files, editing/saving, tag sources and plugins remained outstanding" | Tests verify actual functionality | Tests pass but don't test real files | P1 | Add real audio format round-trip tests | Create temporary audio files and test read/write round-trips |

### P1 — Major Broken Functionality

| File | Function/Class | Problem | Discovery | Expected | Actual | Severity | Proposed Fix | Test Required |
|------|---------------|---------|-----------|----------|--------|----------|--------------|---------------|
| `puddletag/mainwin/m3u.py` | `auto_update_playlist()` | Uses `status["alltags"]` which may become stale after filtering/sorting; `dirname` variable shadowing bug (imported `dirname` shadowed by local) | Modernization log item + code inspection | Playlist auto-update works correctly after save | Potential stale data; local variable shadows import | P1 | Audit `status["alltags"]` usage after filter/sort; fix variable shadowing | Open directory, apply filter, save, verify playlist updated correctly with correct files |
| `puddletag/mainwin/m3u.py` | `readm3u()` | `os.chdir()` calls without guaranteed restoration; bare `except: pass` on file load | Modernization log item | Playlist read works safely | Directory changes may not be restored on error; silent failures | P1 | **FIXED** - `try/finally` added for `os.chdir()` | Load M3U with nonexistent files; verify no crash |
| `puddletag/puddlestuff/export.py` | Export dialog | Error-swallowing behavior; undefined `b64_to_img` function referenced in comment | Modernization log item | Export reports errors clearly | Errors silently swallowed; images not restored from backup | P1 | Remove bare `except: pass`; add proper error reporting; fix image conversion | Export tags plugin; verify errors are shown to user |
| `puddletag/puddlestuff/duplicates/matchfuncs.py` | `_jaro_winkler()` | **Already fixed** — returned input tuple instead of calling algorithm. Verify fix is complete. | Modernization log item | Jaro-Winkler works correctly | Was broken since PyQt6 migration | P1 (resolved) | Already fixed per log; verify no regressions | Run duplicate finder with/without python3-levenshtein |
| `puddletag/puddlestuff/confirmations.py` | `load()` function | Comment says `_confirmations.clear()` is disabled — confirmations accumulate across loads | Modernization log item | Fresh load resets confirmations | Old confirmations persist across loads → settings bloat/corruption | P1 | **FIXED** - `_confirmations.clear()` enabled | Load confirmations twice; verify no duplicate entries |
| `puddletag/puddlesettings.py` | Settings | `QModelIndex()` in default arguments (B008 ruff violation) | Modernization log item | Settings model index works | Potential crash or stale index | P1 | **FIXED** - lazy import pattern | Test settings save/load across sessions |

### P2 — Important Regression or Missing Functionality

| File | Function/Class | Problem | Discovery | Expected | Actual | Severity | Proposed Fix | Test Required |
|------|---------------|---------|-----------|----------|--------|----------|--------------|---------------|
| `puddletag/mainwin/dirview.py` | Directory view | Selection state may become stale after filter/sort/reload | Code inspection | Selection preserved across operations | Selection may map to wrong file after model reset | P2 | Audit selection handling in `changeFolder`, `reloadTags`, `applyFilter` | Select file, apply filter, verify selection maps to correct file |
| `puddletag/mainwin/tagpanel.py` | Tag panel | Multi-value fields may not display correctly; empty values may leak between files | Code inspection | Multi-value fields show correctly | Potential value leakage between files | P2 | Test multi-value editing across selected files | Edit multi-value field across 3+ files; verify each retains correct values |
| `puddletag/puddlestuff/functions.py` | Format function engine | Some format-string functions may not handle edge cases: empty args, Unicode, nested functions | Code inspection | All format functions handle edge cases gracefully | Silent failures or incorrect results | P2 | Build comprehensive format-string test suite | Test: empty args, Unicode, nested functions, malformed expressions |
| `puddletag/puddlestuff/findfunc.py` | Filename ⇄ Tag converter | `tagtofilename` and `filename_to_tag` may not handle all format cases | Code inspection | Conversions work for all supported formats | May fail on edge cases (paths with spaces, Unicode, special chars) | P2 | Test converters with edge cases | Convert filename with spaces → tags → new filename; verify round-trip |
| `puddletag/puddlestuff/audioinfo/wma.py` | WMA support | May have limited functionality depending on Mutagen version | Code inspection | WMA tags readable/writable | May be read-only or partially supported | P2 | Test actual WMA read/write | Obtain WMA file; test read/write of common fields |
| `puddletag/puddlestuff/tagsources/amazon.py` | Amazon tag source | Likely obsolete/replaced; need to verify status | Code inspection | Tag source works or is documented as unavailable | May crash or return garbage | P2 | Verify status; document or remove | Check if Amazon source still functional; if not, document |
| `puddletag/puddlestuff/tagsources/amg.py` | AMG tag source | Likely obsolete | Code inspection | Tag source works | May be broken | P2 | Verify status | Same as Amazon |
| `puddletag/mainwin/teststuff.py` | Test utilities | Undefined names in `__main__` demo block | Modernization log | Demo utilities work | NameError when running demo | P2 | Fix or remove demo block | Run `python3 -m puddletag.teststuff` |

### P3 — Usability/Performance/Quality Issue

| File | Function/Class | Problem | Discovery | Expected | Actual | Severity | Proposed Fix | Test Required |
|------|---------------|---------|-----------|----------|--------|----------|--------------|---------------|
| `puddletag/puddlestuff/duplicates/dupefuncs.py` | Duplicate functions | Undefined names in `__main__` demo block | Modernization log | Demo utilities work | NameError | P3 | Fix or remove demo block | Same as teststuff |
| Various | Artwork handling | Artwork may be lost when editing unrelated tags (known risk area) | Previous audits + code inspection | Artwork preserved when editing other tags | Potential accidental clearing | P3 | Test artwork preservation across tag edits | Edit year field; verify artwork still present |
| `puddletag/puddlestuff/export.py` | Export templates | Some template features may not work (loops, conditional, escaping) | Code inspection | Templates work as expected | May silently produce incorrect output | P3 | Test templates with complex cases | Test: loops, conditionals, HTML escaping, CSV quoting |
| `puddletag/puddlestiff/mainwin/previews.py` | Preview mode | Preview mode may not properly handle selection changes | Code inspection | Preview mode works intuitively | May show stale previews | P3 | Test preview with selection changes | Change selection with preview open; verify preview updates |
| `puddletag/puddlestuff/tagsources/` | All tag sources | Network operations may block GUI; no timeout handling | Code inspection | GUI remains responsive | Potential freezes | P3 | Audit QThread usage; add timeouts | Open tag source dialog; verify GUI responsiveness |
| `puddletag/puddlestuff/musiclib.py` | Music library integration | May have performance issues with large libraries | Code inspection | Library scan works | May be slow with many files | P3 | Benchmark library scan | Scan large directory; monitor UI responsiveness |
| Various | CLI commands | May not handle all edge cases (Unicode paths, spaces) | Code inspection | CLI works for all cases | May fail on edge cases | P3 | Test CLI with edge cases | `python3 puddletag tag --help` etc. |

### P4 — Cosmetic/Documentation/Minor Issue

| File | Problem | Severity | Proposed Fix |
|------|---------|----------|-------------|
| ROADMAP.md | Several `[x]` markers for features that may not be verified | P4 | Update roadmap with actual verified state |
| NEWS/changelog | May not reflect all functional changes | P4 | Update to reflect real functionality |
| Documentation | Some user-visible strings may be hard-coded English | P4 | Internationalize where appropriate |
| pyproject.toml | Minimal — may need build-frontend enhancements | P4 | Enhance if needed for packaging |

---

## KEY ARCHITECTURE OBSERVATIONS

### GUI Architecture
- **TagTable** → `TagModel` (QAbstractTableModel) → individual `Tag` objects (per-file)
- Model uses `previewMode` to track unsaved changes
- Selection handled at `TagTable` level; model emits signals on data changes
- `TagDelegate` (QStyledItemDelegate) handles editor creation/setModelData

### Tag Format Layer
- **Mutagen-based**: Each format (MP3, FLAC, OGG, MP4, WMA, APE, WAV, AIFF, DSF, TAK, TTA, OptimFROG, Musepack) has a dedicated Tag class
- Unified `MockTag` base class provides core dictionary operations
- `tag_factory()` creates format-specific Tag classes with handler mappings
- `setmapping()` and `register_tag()` manage tag→field mapping

### File Model / Table Model
- `TagModel` extends `QAbstractTableModel`
- Supports sorting (`sortByFields`), filtering (`applyFilter`), undo/redo
- `previewMode` separates UI editing from actual tag writing
- `setRowData()` handles actual tag writes via `write()` utility

### Actions/Functions Engine
- **106 functions** in `functions.py` — replace, trim, case conversion, regex, etc.
- **74 actions** in `actiondlg.py` — automatable batch operations
- Format strings use `%field%` syntax with `$function()` calls
- Parser/evaluator in `findfunc.py`

### Tag Sources
- MusicBrainz, Discogs, AcoustID, FreeDB/CDDB, Amazon, AMG
- All network-based; should run in background threads
- Modernization log mentions "Asynchronous Lookups" accomplished

### Music Libraries
- Rhythmbox, MPD integration
- Duplicate finding, statistics

### Converters
- Filename → Tag (pattern-based)
- Tag → Filename (pattern-based)
- Template-based export (HTML, RTF, CSV with $loop support)

---

## CRITICAL DEFECTS REQUIRING IMMEDIATE ATTENTION

1. **M3U playlist auto-update** — uses `status["alltags"]` which may not reflect current selection after filtering/sorting. Could point to wrong files.

2. **Export error swallowing** — bare `except: pass` in export_tags plugin could hide serious errors during backup/restore.

3. **Selection/model staleness** — after filter/sort/reload, QModelIndex references may become invalid, causing edits to wrong files.

4. **Undo/redo with preview mode** — the undo stack uses `defaultdict(dict)` keyed by undolevel; need to verify preview undo correctly isolates from main undo.

---

## RECOMMENDED IMPLEMENTATION ORDER

### Phase 1 — Data Safety (P0/P1)
1. Fix m3u.py `auto_update_playlist()` staleness and `dirname` shadowing
2. Fix export.py error swallowing
3. Audit and fix selection staleness in model operations

### Phase 2 — Core Functionality (P1/P2)
4. Comprehensive format round-trip testing (MP3, FLAC, OGG, MP4, WAV, AIFF)
5. Multi-file editing correctness
6. Preview mode behavior
7. Undo/redo reliability

### Phase 3 — Format Reliability (P2)
8. Test all supported formats for read/write capability
9. Identify and document read-only formats
10. Fix partial/write-limited formats

### Phase 4 — Actions/Functions (P2/P3)
11. Format-string parser test suite
12. Action functioning testing
13. Converter edge-case handling

### Phase 5 — Usability (P3)
14. Artwork management reliability
15. Tag source UI/responsiveness
16. CLI edge cases

### Phase 6 — Documentation (P4)
17. Update ROADMAP.md with actual verified state
18. Update CHANGELOG
19. Create TESTING.md with procedures

---

## TESTING RECOMMENDATIONS

1. **Create real audio test fixtures** covering: MP3, FLAC, OGG, MP4, WAV, AIFF
2. **Add integration tests** for: multi-file editing, preview, undo/redo, converters
3. **Separate network tests** (tag sources) from offline deterministic tests
4. **Use temporary directories** — never modify user's real music library
5. **Add tests for**: format round-trips, multi-file edits, selection state, artwork preservation, CLI edge cases

---

## NEXT STEPS

1. This audit report should be reviewed and approved
2. Highest-P0/P1 items should be fixed next (M3U auto-update, export error handling, selection staleness)
3. Create functional test matrix
4. Begin Phase 1 fixes
5. Re-run test suite after each fix
6. Update roadmap with verified accomplishments

---
*This report was generated as the initial audit deliverable per the project guidelines. All findings must be addressed before claiming the application is substantially improved.*