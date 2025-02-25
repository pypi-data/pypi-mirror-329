# Hike ChangeLog

## v0.5.0

**Released: 2025-02-25**

- Added an application command for jumping to the markdown document viewer.
  ([#39](https://github.com/davep/hike/pull/39))
- Added `document` as a command that the command line understands.
  ([#39](https://github.com/davep/hike/pull/39))

## v0.4.0

**Released: 2025-02-19**

- Added `changelog` as a command that the command line understands.
  ([#33](https://github.com/davep/hike/pull/33))
- Added `readme` as a command that the command line understands.
  ([#33](https://github.com/davep/hike/pull/33))
- Fixed failing when opening a document-relative local non-markdown file
  from a click. ([#34](https://github.com/davep/hike/pull/34))

## v0.3.0

**Released: 2025-02-18**

- Added the ability to save a copy of the currently-viewed document.
  ([#15](https://github.com/davep/hike/pull/15))
- Made `chdir` a lot less fussy about the path given.
  ([#18](https://github.com/davep/hike/pull/18))
- Added `quit` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `dir` and `ls` as aliases for `chdir`.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `contents` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `bookmarks` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `history` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `local` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Added `help` as a command that the command line understands.
  ([#24](https://github.com/davep/hike/pull/24))
- Changed command line completion so that if history is empty, known
  commands are suggested. ([#29](https://github.com/davep/hike/pull/29))

## v0.2.0

**Released: 2025-02-16**

- The bookmark search command palette now sorts the bookmarks.
  ([#2](https://github.com/davep/hike/pull/2))
- The suggester for the command line now prefers newer history entries over
  older. ([#3](https://github.com/davep/hike/pull/3))
- Added the ability to move the command line to the top of the screen.
  ([#5](https://github.com/davep/hike/pull/5))
- Added the ability to copy the current location to the clipboard.
  ([#9](https://github.com/davep/hike/pull/9))
- Added the ability to copy the currently-viewed Markdown to the clipboard.
  ([#9](https://github.com/davep/hike/pull/9))
- Added the ability to edit a Markdown document if it's in the local
  filesystem. ([#10](https://github.com/davep/hike/pull/10))
- Pinned Textual to v1.0.0 for now as it broke `OptionList`.

## v0.1.0

**Released: 2025-02-14**

- Initial release.

## v0.0.1

**Released: 2025-02-07**

- Initial placeholder package to test that the name is available in PyPI.

[//]: # (ChangeLog.md ends here)
