"""Provides the main application commands for the command palette."""

##############################################################################
# Textual enhanced imports.
from textual_enhanced.commands import (
    ChangeTheme,
    Command,
    CommandHits,
    CommandsProvider,
    Help,
    Quit,
)

##############################################################################
# Local imports.
from ..commands import (
    Backward,
    BookmarkLocation,
    ChangeCommandLineLocation,
    ChangeNavigationSide,
    CopyLocationToClipboard,
    CopyMarkdownToClipboard,
    Edit,
    Forward,
    JumpToBookmarks,
    JumpToCommandLine,
    JumpToDocument,
    JumpToHistory,
    JumpToLocalBrowser,
    JumpToTableOfContents,
    Reload,
    SaveCopy,
    SearchBookmarks,
    ToggleNavigation,
)


##############################################################################
class MainCommands(CommandsProvider):
    """Provides some top-level commands for the application."""

    def _maybe(self, command: type[Command]) -> CommandHits:
        """Yield a command if it's application.

        Args:
            command: The type of the command to maybe yield.

        Yields:
            The command if it can be used right now.
        """
        if self.screen.check_action(command.action_name(), ()):
            yield command()

    def commands(self) -> CommandHits:
        """Provide the main application commands for the command palette.

        Yields:
            The commands for the command palette.
        """
        yield from self._maybe(Backward)
        yield from self._maybe(BookmarkLocation)
        yield ChangeCommandLineLocation()
        yield ChangeNavigationSide()
        yield ChangeTheme()
        yield from self._maybe(CopyLocationToClipboard)
        yield from self._maybe(CopyMarkdownToClipboard)
        yield from self._maybe(Edit)
        yield from self._maybe(Forward)
        yield Help()
        yield JumpToBookmarks()
        yield JumpToCommandLine()
        yield JumpToDocument()
        yield JumpToHistory()
        yield JumpToLocalBrowser()
        yield JumpToTableOfContents()
        yield Quit()
        yield from self._maybe(Reload)
        yield from self._maybe(SaveCopy)
        yield SearchBookmarks()
        yield ToggleNavigation()


### main.py ends here
