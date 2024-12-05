# GreasePencil
A couple of Grease Pencil scripts 

## GP Keyframe Tools
**Compatibility**: Blender 4.3+
This script adds a couple of little tools for Grease Pencil animators
### N-panel
In the 3Dview's N-panel under the Grease Pencil tab, you'll find a panel called Grease Pencil Keyframes.
- **Keyframe Count**: add blank keyframes to the selected Grease Pencil layer
- **Spacing**: specify how far apart your keyframes will be spaced
- **Start from Playhead**: Position the playhead where you want your new blank keyframes to start from. Otherwise, blank keyframes will initially be added at frame 1, or appended to the end of the current sequence of keyframes.
- **Add Keyframes** button. Once you've entered the things, ***be sure to select the layer you want the keyframes added to***, then hit this button.

### GP Timeline Toolbar
A couple of buttons and a timecode readout on the Dope Sheet's Grease Pencil toolbar:
- **+5**: this button adds 5 blanks on twos ***to the selected GP layer***
- **+10**: this button adds 10 blanks on ones ***to the selected GP layer***
- **Time**: timecode in seconds and frames

# Installation
1. Click the big green **<>CODE** button above, and choose *Download ZIP*.
2. Save and Extract the .zip somewhere on your local drive.
3. In Blender, go to *Edit > Preferences > Add-ons* tab
- Top-right dropdown arrow icon (Add-ons Settings), choose > *Install from disk..*
- Browse to where you saved the above `.zip` and wriggle into: *GreasePencil-main > gp_ap_timeline_tools >* `gp_ap_timeline_blanks_<version>.zip`
- Click Install and you're done!
