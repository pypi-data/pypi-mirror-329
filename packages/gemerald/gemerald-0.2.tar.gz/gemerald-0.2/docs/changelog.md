# Changelog

## 0.4

 - Plugins
 - Image auto compression
 - Atom feeds
 - EPUB

## v0.3

 - Raw snippets.
 - RSS.
 - Individualized static content for each format.
 - `Context.utils` now does not exist. Use `Context.dateGenerated` instead.
 - `Context` now has extra field called `url`. It is independent locator of a file.
 - `Context.href` moved to `Site.href`. From now everything format-dependent lives in a `Site`.
 - When iterating over siblings it only iterates over its `Context`s.
 - All context are immutable during templating.

## v0.2 [Done soon]

 - Code quality improvments
 - Bug fixes
 - Documentation apears

## v0.1 [Done]

 - Initial release
 - Alpha in working state, deployed at wilmhit.pw
 - Critical bug found in page siblings function
