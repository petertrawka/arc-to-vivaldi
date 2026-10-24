# Arc → Vivaldi migration kit

Arc is in maintenance mode, and Vivaldi is the closest thing to it that's still being built. This kit is what I wish I'd had when I moved: a calm, Arc-like look for Vivaldi, a tool that brings your Arc Spaces over, and the traps I hit along the way so you don't.

> Tested on **Vivaldi 8.2 on macOS** (October 2026). Most of it should work on Windows and Linux too; the title-bar tweak is macOS only.

_Screenshots and a short GIF are coming soon._

## What's in it

| | What it does |
|---|---|
| `css/` | Seven small style tweaks. Each one works on its own, so take only what you like |
| `themes/` | 14 "Nordic" themes: warm charcoal and warm paper, with six muted accents (Sage, Fjord, Clay, Sand, Heather, Moss) in dark and light |
| `tools/arc_to_bookmarks.py` | Turns your Arc Spaces into one bookmarks file, one folder per Space, that Vivaldi can import |

It builds on [**Awesome-Vivaldi**](https://github.com/PaRr0tBoY/Awesome-Vivaldi) by PaRr0tBoY. I started from that pack and added these tweaks on top. Go give it a star.

## What moves over from Arc, and what doesn't

| Arc | In Vivaldi |
|---|---|
| Passwords, history, extensions (main profile) | ✅ Vivaldi's built-in Arc import |
| Passwords from your *other* Arc profiles | ⚠️ The importer fails on these. See [Traps](#migration-traps) |
| Spaces and their folders | ⚠️ Not imported. Use `tools/arc_to_bookmarks.py`, then open each folder in its own Workspace |
| Favorites (the icon grid) | ⚠️ Become a bookmarks folder. Web Panels are a good home for the 4-6 you use most |
| Logins (cookies) | ❌ You sign in again once per site |
| Extensions you built yourself | ❌ Load them again with **Load unpacked** |
| Extension settings and keys | ❌ Don't carry over; enter them again |
| Boosts, Little Arc, Space colours | ❌ No equivalent |

## Install the look (about 15 minutes)

1. **Allow style changes.** Open `vivaldi://experiments` and turn on **Allow CSS modifications**. Restart Vivaldi.
2. **Make a folder** for your style files, for example `~/Documents/vivaldi-css`.
3. **Add the Awesome-Vivaldi files.** Download [Awesome-Vivaldi](https://github.com/PaRr0tBoY/Awesome-Vivaldi), open `Vivaldi8.0Stable/CSS/`, and copy these into your folder:
   `PeekTabbar.css`, `AdaptiveBF.css`, `BetterAnimation.css`, `RemoveClutter.css`, `Quietify.css`, `VividQC.css`, `DownloadPanel.css`, `Extensions.css`, `LineBreak.css`.
   Only the style files: the pack's script mods don't load on Vivaldi 8.2.
4. **Add the calm tweaks.** Copy everything from this repo's `css/` folder into the same folder.
5. **Point Vivaldi at it.** Settings → Appearance → **Custom UI Modifications** → Select Folder.
6. **Import a theme.** Settings → Themes → **Import Theme…**, pick a dark and a light one from `themes/`, then set **Theme Schedule → Operating System** to use them.
7. **Change the settings** in the checklist below, then restart Vivaldi.

### The tweaks

| File | What it does |
|---|---|
| `calm-tabs.css` | No coloured fill or glow on tabs. The active tab gets a faint grey tint, like Linear |
| `calm-top-area.css` | Above the tabs: just the Workspace name and the address field. Extension icons, back and reload fade in when you hover |
| `calm-folded-column.css` | When the tab column folds, it shows clean centred icons, no half-cut names |
| `calm-stacks.css` | No outlines around tab stacks. The number on the right still tells you it's a stack |
| `calm-address-bar.css` | Quieter suggestion list. The address field grows in place when you click it, instead of jumping |
| `calm-peek-tabbar-override.css` | Tunes Awesome-Vivaldi's slide-out tab bar: stack names stay readable (45/55 split), faster slide |
| `calm-titlebar-macos.css` | *macOS, experimental.* Removes the full-width title strip; only the window buttons stay, in the corner |

**Undo any tweak:** delete its file and restart Vivaldi.

### Settings checklist

Vivaldi can't save these into a file, so set them by hand:

- **Tabs** → Tab Bar Position: **Left** · Tab Stacking: **Two-Level** · New Tab Position: **As Last Tab**
- **Tabs** → Tab Stack Options: **Open Tabs in Current Tab Stack** off
- **Tabs** → Pinned Tabs: **Don't Close Pinned Tabs**, and **Allow Closing in Pinned Stacks** off (see Traps)
- **Tabs** → Tab Options: **Show Popup Thumbnails** off, **Show Tab Thumbnails** off
- **Appearance** → UI Auto-hide: on, with Tab Bar, Panel and Bookmarks Bar ticked · Status Bar: **Status Info Overlay**
- **General** → Startup: **Last Session**, **Lazy Load Restored Tabs** on (tabs load when you click them, like Arc)
- **Keyboard** → give **⌘T** to Quick Commands (clear it from New Tab first): you get Arc's "type first, tab later" box
- **Keyboard** → give **⌘S** to Tab Bar (clear it from Save Page As first): shows and hides the sidebar, like Arc
- **Quick Commands** → **Open Links in New Tab** on
- **Search** → add YouTube with nickname `yt` and URL `https://www.youtube.com/results?search_query=%s`. Then `⌘T` → `yt lofi` works like Arc's tab-to-search

## Bring your Spaces over

```bash
python3 tools/arc_to_bookmarks.py ~/Desktop/arc-spaces.html
```

It only *reads* Arc's sidebar file and prints how many links each Space has. Then:

1. Vivaldi → File → **Import from Applications or Bookmark Files** → **Bookmarks HTML File** → pick `arc-spaces.html`.
2. For each Space, create a **Workspace** with the same name.
3. In that Workspace, right-click a folder in **Bookmarks → Imported → Arc Spaces** → **Open in New Tab**. Vivaldi only opens links directly inside the folder you click, so open each sub-folder separately.
4. Select the tabs (click the first, shift-click the last) → right-click → **Stack Tabs** → right-click the stack → **Rename**. Now it behaves like an Arc folder.
5. Right-click the stack → **Pin Tab Stack** so it stays put.

## Migration traps

**⌘W can delete your pinned tabs.** In Arc, ⌘W on a pinned tab just put it away. In Vivaldi, with "Allow Closing in Pinned Stacks" on, ⌘W removes tabs from your stacks for good. Keep it **off**. If it already happened, press **⇧⌘T** repeatedly to bring tabs back.

**Passwords from other Arc profiles.** The Arc importer handles your main profile only. Picking another profile or folder fails with "Login Data file not found". What works: in Arc, switch to a Space that uses that profile, open `arc://password-manager/settings`, **Download file**, then in Vivaldi open `vivaldi://password-manager/settings` → **Import**. Delete the CSV afterwards, because it holds your passwords in plain text.

**New tabs come out pinned.** A tab you open while you're inside a pinned stack inherits the pin. No setting changes this; it's how Vivaldi works. Right-click → unpin, or open new tabs from a normal tab.

**Tabs open inside your stacks.** Turn off **Open Tabs in Current Tab Stack** and set **New Tab Position** to **As Last Tab**.

**Every tab reloads on start.** Turn on **Lazy Load Restored Tabs** (General → Startup).

**SharePoint and OneDrive links turn into "Home - OneDrive".** If you open them before signing in, Microsoft redirects them and the real address is lost. Sign in once, then reopen them from the imported bookmarks.

**Your own extensions.** `vivaldi://extensions` → **Developer mode** → **Load unpacked**. Their saved settings and keys stay in Arc, so enter them again. Shortcuts live under `vivaldi://extensions` → ☰ → **Keyboard shortcuts**.

**Netflix works**, but at a lower maximum resolution than in Safari, which is true of any Chrome-based browser on a Mac.

## Credits and licence

- Built on [Awesome-Vivaldi](https://github.com/PaRr0tBoY/Awesome-Vivaldi) by PaRr0tBoY (GPL-3.0). Its files aren't included here; download them from the original repo.
- The tweaks, themes and script in this repo are MIT-licensed. See [LICENSE](LICENSE).

If something breaks after a Vivaldi update, open an issue and say which Vivaldi version you're on.
